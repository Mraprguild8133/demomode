# Telegram Wasabi Storage Bot

A high-speed Telegram bot that uploads files to Wasabi cloud storage and generates shareable download links. Built with Pyrogram and Boto3 for optimal performance.

## Features

- **Large File Support**: Handle files up to 4GB
- **Ultra-Fast Transfers**: Multipart uploads with 10x concurrent chunks for maximum speed
- **TgCrypto Acceleration**: 5-10x faster encryption for Telegram operations
- **Real-time Progress**: Live progress tracking with speed indicators
- **Secure Storage**: Files stored in Wasabi S3-compatible cloud storage
- **7-Day Links**: Generate shareable links valid for 7 days
- **Online Streaming**: Video and audio files can be played directly in browser
- **Multiple Formats**: Support for documents, videos, audio, and photos

## Requirements

- Python 3.11+
- Telegram API credentials (API_ID, API_HASH, BOT_TOKEN)
- Wasabi storage account

## Installation

1. Install dependencies (already done in Replit):
```bash
pip install pyrogram tgcrypto boto3 python-dotenv
```

2. Set up environment variables using the Secrets tool in Replit:
   - `API_ID` - Your Telegram API ID
   - `API_HASH` - Your Telegram API Hash
   - `BOT_TOKEN` - Your bot token from @BotFather
   - `WASABI_ACCESS_KEY` - Wasabi access key
   - `WASABI_SECRET_KEY` - Wasabi secret key
   - `WASABI_BUCKET` - Wasabi bucket name
   - `WASABI_REGION` - Wasabi region (e.g., us-east-1)

## Getting Telegram API Credentials

1. Visit https://my.telegram.org/apps
2. Log in with your phone number
3. Create a new application
4. Copy your API_ID and API_HASH

## Getting Bot Token

1. Open Telegram and search for @BotFather
2. Send `/newbot` and follow the instructions
3. Copy the bot token provided

## Getting Wasabi Credentials

1. Sign up at https://wasabi.com
2. Create a bucket in your preferred region
3. Generate access keys from the account settings
4. Note your bucket name and region

## Usage

Run the bot:
```bash
python main.py
```

In Telegram:
1. Start a chat with your bot
2. Send `/start` to see the welcome message
3. Send any file (up to 4GB)
4. Receive a shareable link (valid for 7 days)
   - Videos/Audio: Get a streaming link for direct browser playback
   - Other files: Get a standard download link

## Commands

- `/start` - Display welcome message
- `/help` - Show help information

## Architecture

- **main.py** - Bot handlers and message processing
- **config.py** - Configuration and environment variable management
- **wasabi_handler.py** - Wasabi S3 operations with async support
- **.env.example** - Template for environment variables

## Performance Optimizations

- **TgCrypto**: 5-10x faster Telegram encryption/decryption
- **Multipart Uploads**: 8MB chunks with 10x concurrent transfers
- **Async/Await**: Non-blocking operations throughout
- **ThreadPoolExecutor**: Parallel S3 operations
- **Real-time Progress**: Live speed and progress tracking
- **Automatic Cleanup**: Temporary files removed after upload

## Streaming Support

- **Auto-Detection**: Videos and audio files automatically configured for streaming
- **Inline Playback**: Direct browser playback without downloading
- **Proper Headers**: ContentType and ContentDisposition set for optimal streaming
- **Format Support**: Works with MP4, MKV, AVI, MP3, M4A, WAV, and more

## Security

- Environment variables for sensitive data
- Time-limited download links (7 days by default)
- No storage of user credentials
- Automatic file cleanup after upload
- Secure Wasabi S3 storage

## License

MIT License
