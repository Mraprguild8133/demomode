import os
import asyncio
import mimetypes
import urllib.parse
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from wasabi_handler import WasabiHandler
import time
import uuid

os.makedirs(Config.DOWNLOAD_DIR, exist_ok=True)

app = Client(
    "telegram_wasabi_bot",
    api_id=int(Config.API_ID) if Config.API_ID else 0,
    api_hash=Config.API_HASH or "",
    bot_token=Config.BOT_TOKEN or ""
)

wasabi = WasabiHandler()

def format_bytes(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def format_speed(bytes_per_second):
    return f"{format_bytes(bytes_per_second)}/s"

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    welcome_text = """
🚀 **High-Speed Telegram Storage Bot**

Upload files up to 4GB and get instant download links!

**Commands:**
/start - Show this message
/help - Get help

**How to use:**
1. Send me any file (up to 4GB)
2. I'll upload it to secure cloud storage
3. You'll get a shareable download link

**Features:**
✅ Support for files up to 4GB
✅ High-speed uploads and downloads
✅ Secure cloud storage (Wasabi)
✅ Real-time progress tracking
✅ Shareable download links (7 days)
▶️ Online streaming for videos and audio

Just send me a file to get started!
"""
    await message.reply_text(welcome_text)

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    help_text = """
📚 **Help Guide**

**Supported File Types:**
• Documents
• Videos
• Audio
• Photos
• Any other file type (up to 4GB)

**How it works:**
1. Send me any file
2. I'll download it with high-speed processing
3. Upload it to Wasabi cloud storage
4. Generate a secure download/streaming link
5. Send you the link (valid for 7 days)

**Tips:**
• Larger files take longer to process
• You'll see real-time progress updates
• Videos & audio can be streamed directly in browser
• Links expire after 7 days for security
• Optimized for maximum upload/download speed

Need more help? Just send me a file!
"""
    await message.reply_text(help_text)

@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def handle_file(client: Client, message: Message):
    status_msg = await message.reply_text("📥 Starting download...")
    local_path = None
    
    try:
        if message.document:
            file_info = message.document
            file_name = file_info.file_name
        elif message.video:
            file_info = message.video
            file_name = f"video_{int(time.time())}.mp4"
        elif message.audio:
            file_info = message.audio
            file_name = f"audio_{int(time.time())}.mp3"
        elif message.photo:
            file_info = message.photo
            file_name = f"photo_{int(time.time())}.jpg"
        else:
            await status_msg.edit_text("❌ Unsupported file type!")
            return
        
        file_size = file_info.file_size
        
        if file_size > 4 * 1024 * 1024 * 1024:
            await status_msg.edit_text("❌ File too large! Maximum size is 4GB.")
            return
        
        local_path = os.path.join(Config.DOWNLOAD_DIR, f"{uuid.uuid4()}_{file_name}")
        
        start_time = time.time()
        last_update = 0
        
        async def download_progress(current, total):
            nonlocal last_update
            current_time = time.time()
            
            if current_time - last_update < 1 and current != total:
                return
            
            last_update = current_time
            percentage = (current / total) * 100
            elapsed = current_time - start_time
            speed = current / elapsed if elapsed > 0 else 0
            
            progress_bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
            
            text = f"""
📥 **Downloading from Telegram...**

{progress_bar} {percentage:.1f}%

📊 {format_bytes(current)} / {format_bytes(total)}
⚡ Speed: {format_speed(speed)}
"""
            try:
                await status_msg.edit_text(text)
            except:
                pass
        
        await message.download(file_name=local_path, progress=download_progress)
        
        await status_msg.edit_text("☁️ Uploading to cloud storage...")
        
        upload_start = time.time()
        last_upload_update = 0
        loop = asyncio.get_event_loop()
        
        def upload_progress(current, total):
            nonlocal last_upload_update
            current_time = time.time()
            
            if current_time - last_upload_update < 1 and current != total:
                return
            
            last_upload_update = current_time
            percentage = (current / total) * 100
            elapsed = current_time - upload_start
            speed = current / elapsed if elapsed > 0 else 0
            
            progress_bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
            
            text = f"""
☁️ **Uploading to Cloud Storage...**

{progress_bar} {percentage:.1f}%

📊 {format_bytes(current)} / {format_bytes(total)}
⚡ Speed: {format_speed(speed)}
"""
            
            asyncio.run_coroutine_threadsafe(safe_update(status_msg, text), loop)
        
        async def safe_update(msg, text):
            try:
                await msg.edit_text(text)
            except:
                pass
        
        unique_name = f"{uuid.uuid4()}_{file_name}"
        object_key = await wasabi.upload_file(local_path, unique_name, upload_progress)
        
        content_type, _ = mimetypes.guess_type(file_name)
        is_streamable = content_type and (content_type.startswith('video/') or content_type.startswith('audio/'))
        
        download_link = wasabi.generate_download_link(object_key, streaming=is_streamable)
        
        total_time = time.time() - start_time
        avg_speed = file_size / total_time if total_time > 0 else 0
        
        days = Config.LINK_EXPIRATION // 86400
        
        # Get web domain for player URL
        web_domain = os.getenv('REPLIT_DEV_DOMAIN') or os.getenv('REPL_SLUG') + '.repl.co'
        if not web_domain:
            web_domain = 'localhost:5000'
        
        scheme = 'https' if 'repl.co' in web_domain else 'http'
        
        file_type = 'video' if content_type and content_type.startswith('video/') else 'audio' if content_type and content_type.startswith('audio/') else 'document'
        
        # Create player URL
        encoded_url = urllib.parse.quote(download_link, safe='')
        encoded_name = urllib.parse.quote(file_name, safe='')
        player_url = f"{scheme}://{web_domain}/player?url={encoded_url}&name={encoded_name}&type={file_type}"
        
        if is_streamable:
            file_type_icon = "🎥" if content_type.startswith('video/') else "🎵"
            success_text = f"""
✅ **Upload Successful!**

{file_type_icon} **File:** {file_name}
📦 **Size:** {format_bytes(file_size)}
⏱️ **Time:** {total_time:.1f}s
⚡ **Avg Speed:** {format_speed(avg_speed)}

⏰ **Link expires in {days} days**

Choose an option below:
"""
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("▶️ Stream Online", url=player_url),
                    InlineKeyboardButton("📥 Direct Download", url=download_link)
                ]
            ])
        else:
            success_text = f"""
✅ **Upload Successful!**

📄 **File:** {file_name}
📦 **Size:** {format_bytes(file_size)}
⏱️ **Time:** {total_time:.1f}s
⚡ **Avg Speed:** {format_speed(avg_speed)}

⏰ **Link expires in {days} days**

Choose an option below:
"""
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("📥 Download File", url=download_link)
                ]
            ])
        
        await status_msg.edit_text(success_text, reply_markup=keyboard)
            
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")
        print(f"Error processing file: {e}")
    finally:
        if local_path and os.path.exists(local_path):
            try:
                os.remove(local_path)
            except Exception as cleanup_error:
                print(f"Warning: Could not delete temporary file {local_path}: {cleanup_error}")

# Error handler for large files
@app.on_message(filters.video & filters.private)
async def handle_large_video(client: Client, message: Message):
    if message.video.file_size > 4 * 1024 * 1024 * 1024:
        await message.reply_text("❌ Video file too large! Maximum size is 4GB.")

# Service message handler
@app.on_message(filters.service)
async def service_message(client: Client, message: Message):
    # Ignore service messages like pin notifications, etc.
    return

if __name__ == "__main__":
    try:
        Config.validate()
        print("✅ Configuration validated")
        print("🚀 Starting Telegram Bot...")
        print("🤖 Bot is running...")
        app.run()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n📝 Please set the required environment variables.")
        print("   You can copy .env.example to .env and fill in your credentials.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        wasabi.close()
