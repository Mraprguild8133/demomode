import boto3
import asyncio
import os
import mimetypes
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional, Dict
from config import Config
from boto3.s3.transfer import TransferConfig

class WasabiHandler:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=f'https://s3.{Config.WASABI_REGION}.wasabisys.com',
            aws_access_key_id=Config.WASABI_ACCESS_KEY,
            aws_secret_access_key=Config.WASABI_SECRET_KEY,
            region_name=Config.WASABI_REGION
        )
        self.bucket = Config.WASABI_BUCKET
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        self.transfer_config = TransferConfig(
            multipart_threshold=8 * 1024 * 1024,
            max_concurrency=10,
            multipart_chunksize=8 * 1024 * 1024,
            use_threads=True
        )
    
    def _get_content_type(self, file_path: str) -> str:
        content_type, _ = mimetypes.guess_type(file_path)
        return content_type or 'application/octet-stream'
    
    async def upload_file(
        self,
        file_path: str,
        object_name: Optional[str] = None,
        progress_callback: Optional[Callable] = None
    ) -> str:
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        file_size = os.path.getsize(file_path)
        content_type = self._get_content_type(file_path)
        
        def upload_with_progress():
            uploaded = 0
            
            def callback(bytes_amount):
                nonlocal uploaded
                uploaded += bytes_amount
                if progress_callback:
                    progress_callback(uploaded, file_size)
            
            extra_args = {
                'ContentType': content_type,
            }
            
            if content_type.startswith('video/') or content_type.startswith('audio/'):
                extra_args['ContentDisposition'] = 'inline'
            
            self.s3_client.upload_file(
                file_path,
                self.bucket,
                object_name,
                Callback=callback,
                Config=self.transfer_config,
                ExtraArgs=extra_args
            )
            
            return object_name
        
        loop = asyncio.get_event_loop()
        object_key = await loop.run_in_executor(self.executor, upload_with_progress)
        
        return object_key
    
    async def download_file(
        self,
        object_name: str,
        file_path: str,
        progress_callback: Optional[Callable] = None
    ) -> str:
        response = await asyncio.get_event_loop().run_in_executor(
            self.executor,
            lambda: self.s3_client.head_object(Bucket=self.bucket, Key=object_name)
        )
        file_size = response['ContentLength']
        
        def download_with_progress():
            downloaded = 0
            
            def callback(bytes_amount):
                nonlocal downloaded
                downloaded += bytes_amount
                if progress_callback:
                    progress_callback(downloaded, file_size)
            
            self.s3_client.download_file(
                self.bucket,
                object_name,
                file_path,
                Callback=callback
            )
            
            return file_path
        
        loop = asyncio.get_event_loop()
        result_path = await loop.run_in_executor(self.executor, download_with_progress)
        
        return result_path
    
    def generate_download_link(self, object_name: str, expiration: Optional[int] = None, streaming: bool = False) -> str:
        if expiration is None:
            expiration = Config.LINK_EXPIRATION
        
        params = {'Bucket': self.bucket, 'Key': object_name}
        
        if streaming:
            params['ResponseContentDisposition'] = 'inline'
        
        url = self.s3_client.generate_presigned_url(
            'get_object',
            Params=params,
            ExpiresIn=expiration
        )
        
        return url
    
    def get_file_info(self, object_name: str) -> Dict:
        try:
            response = self.s3_client.head_object(Bucket=self.bucket, Key=object_name)
            return {
                'size': response.get('ContentLength', 0),
                'content_type': response.get('ContentType', 'application/octet-stream'),
                'last_modified': response.get('LastModified')
            }
        except Exception:
            return {}
    
    async def delete_file(self, object_name: str):
        await asyncio.get_event_loop().run_in_executor(
            self.executor,
            lambda: self.s3_client.delete_object(Bucket=self.bucket, Key=object_name)
        )
    
    def close(self):
        self.executor.shutdown(wait=True)
