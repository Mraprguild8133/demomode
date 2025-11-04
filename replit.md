# Telegram Wasabi Storage Bot

## Overview
Ultra-high-speed Telegram bot that handles file uploads up to 4GB, stores them in Wasabi cloud storage, and generates shareable download/streaming links valid for 7 days. Built with Pyrogram (Telegram MTProto API), TgCrypto for acceleration, and Boto3 (AWS S3-compatible client) with multipart upload optimization.

## Project Status
Created: November 4, 2025
Status: Development

## Architecture

### Core Components
1. **main.py** - Telegram bot handlers with Pyrogram
   - /start and /help commands
   - File handler for documents, videos, audio, photos
   - Real-time progress tracking for downloads and uploads
   - Automatic file cleanup

2. **wasabi_handler.py** - Wasabi S3 operations
   - Async upload/download with progress callbacks
   - Presigned URL generation for downloads
   - ThreadPoolExecutor for non-blocking operations

3. **config.py** - Environment variable management
   - Validation of required credentials
   - Configuration constants

### Key Features
- Support for files up to 4GB
- TgCrypto acceleration (5-10x faster Telegram operations)
- Multipart uploads with 10x concurrent chunks (8MB each)
- Async/await for high-speed operations
- Real-time progress bars with speed indicators
- Online streaming for video/audio files
- Automatic content-type detection
- Time-limited download links (default: 7 days)
- Temporary file cleanup

## Dependencies
- pyrogram: Telegram MTProto API client
- tgcrypto: High-performance cryptography for Pyrogram (5-10x speed boost)
- boto3: AWS S3-compatible client for Wasabi
- python-dotenv: Environment variable management

## Required Environment Variables
- API_ID: Telegram API ID
- API_HASH: Telegram API Hash
- BOT_TOKEN: Bot token from @BotFather
- WASABI_ACCESS_KEY: Wasabi access key
- WASABI_SECRET_KEY: Wasabi secret key
- WASABI_BUCKET: Wasabi bucket name
- WASABI_REGION: Wasabi bucket region (e.g., us-east-1)

## File Structure
```
.
├── main.py              # Bot entry point and handlers
├── config.py            # Configuration management
├── wasabi_handler.py    # Wasabi S3 operations
├── .env.example         # Environment variable template
├── .gitignore          # Git ignore rules
└── README.md           # User documentation
```

## Recent Changes
- November 4, 2025: Initial project setup
  - Installed Python 3.11 and dependencies (pyrogram, boto3, python-dotenv)
  - Created bot structure with async support
  - Implemented Wasabi S3 integration
  - Added progress tracking for uploads/downloads

- November 4, 2025: Performance and feature enhancements
  - Installed TgCrypto for 5-10x faster Telegram operations
  - Implemented multipart uploads (8MB chunks, 10x concurrency)
  - Added online streaming support for video/audio files
  - Extended link expiration from 1 hour to 7 days
  - Auto-detection of streamable content types
  - Proper ContentType and ContentDisposition headers for streaming
  - Fixed thread-safe async operations for upload progress
