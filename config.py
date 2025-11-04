import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    WASABI_ACCESS_KEY = os.getenv("WASABI_ACCESS_KEY")
    WASABI_SECRET_KEY = os.getenv("WASABI_SECRET_KEY")
    WASABI_BUCKET = os.getenv("WASABI_BUCKET")
    WASABI_REGION = os.getenv("WASABI_REGION", "us-east-1")
    
    LINK_EXPIRATION = int(os.getenv("LINK_EXPIRATION", "604800"))
    
    DOWNLOAD_DIR = "downloads"
    
    @classmethod
    def validate(cls):
        required = {
            "API_ID": cls.API_ID,
            "API_HASH": cls.API_HASH,
            "BOT_TOKEN": cls.BOT_TOKEN,
            "WASABI_ACCESS_KEY": cls.WASABI_ACCESS_KEY,
            "WASABI_SECRET_KEY": cls.WASABI_SECRET_KEY,
            "WASABI_BUCKET": cls.WASABI_BUCKET,
        }
        
        missing = [key for key, value in required.items() if not value]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True
