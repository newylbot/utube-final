# YouTube Uploader Bot

A simple Telegram bot to upload videos to YouTube using the [YouTube Data API v3](https://developers.google.com/youtube/v3/). Developed in Python3.

## Features
- Upload videos directly from Telegram to YouTube
- Customize video title, description, and privacy settings
- Supports multiple authorized users

## Requirements
- Python 3.6+
- Telegram Bot API credentials
- Google API credentials (YouTube Data API v3)

## Setup

### Clone & Virtual Environment
```bash
 git clone https://github.com/odysseusmax/utube.git
 cd utube
 python3 -m venv venv
 source venv/bin/activate
```

### Install Dependencies
```bash
 pip3 install -r requirements.txt
```

### Environment Variables
Set the following variables:
- `BOT_TOKEN` - Get from [BotFather](https://tx.me/BotFather)
- `API_ID` & `API_HASH` - Get from [Telegram](https://my.telegram.org)
- `CLIENT_ID` & `CLIENT_SECRET` - Get from [Google Console](https://console.developers.google.com)
- `BOT_OWNER` - Your Telegram ID
- `UPLOAD_MODE` - `private`, `public`, or `unlisted` (default: `private`)

### Running the Bot
```bash
 python3 -m bot
```

If everything is set up correctly, the bot should be running. Use `/start` to check.

## Notes
- **Daily Upload Limit**: The YouTube API allows ~6 uploads per day due to quota limits.
- **Unverified Apps**: Uploaded videos will remain private unless the app is verified by Google.
- **Copyright**: Uploading copyrighted content may lead to video removal.

## Contact
For support, contact **[@itz_lumino](https://telegram.dog/itz_lumino)**.

## License
Released under [GNU GPL v3.0](LICENSE).

