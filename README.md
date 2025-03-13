# 🚀**YouTube Uploader Bot**

A simple Telegram bot to upload videos to YouTube using the [YouTube Data API v3](https://developers.google.com/youtube/v3/). Developed in Python3.

## ⚡Features

- Upload videos directly from Telegram to YouTube......
- Customize video title, description, and privacy settings.....
- Supports multiple authorized users....

## ✅Requirements

- Python 3.6+
- Telegram Bot API credentials
- Google API credentials (YouTube Data API v3)
- Docker (optional, for containerized deployment)

## 🧪Setup

### Clone & Virtual Environment (For Local Setup)

```bash
git clone https://github.com/newylbot/utube-final.git utube
cd utube
python3 -m venv venv
source venv/bin/activate
```

### ⏬Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 📌Configuration

Instead of using an `.env` file, all configuration values are now managed in `config.py`. Open `config.py` and update the necessary fields:

```python
class Config:
    BOT_TOKEN = "your_bot_token_here"
    SESSION_NAME = "your_bot_username_here"
    API_ID = 123456  # Replace with your API ID
    API_HASH = "your_api_hash_here"
    CLIENT_ID = "your_client_id_here"
    CLIENT_SECRET = "your_client_secret_here"
    BOT_OWNER = 123456789  # Replace with your Telegram user ID
    AUTH_USERS = [BOT_OWNER, 987654321]  # Add more user IDs as needed
    VIDEO_DESCRIPTION = "Default video description"
    VIDEO_CATEGORY = 22  # Default category
    VIDEO_TITLE_PREFIX = "๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ"
    VIDEO_TITLE_SUFFIX = ""
    DEBUG = True
    UPLOAD_MODE = "unlisted"
    CRED_FILE = "auth_token.txt"
```

## 🔗 Getting Google API Credentials (Client ID & Secret)

<details>
<summary>⏩ Click to Expand</summary>

To use the YouTube Data API, you need Google API credentials:

1. **Go to the Google Cloud Console**: [GCP Cloud Console](https://console.developers.google.com)
2. **Create a new project** (or select an existing one).
3. **Enable the YouTube Data API v3**:
   - Go to `APIs & Services` > `Library` > Search for `YouTube Data API v3`
   - Click `Enable`
4. **Create OAuth 2.0 Credentials**:
   - Go to `APIs & Services` > `Credentials`
   - Click `Create Credentials` > `OAuth Client ID`
   - Choose `Application Type: Web Application`
   - Set `Authorized Redirect URIs` to `http://localhost`
   - Click `Create`
5. **Copy your `Client ID` and `Client Secret`** and add them to `config.py`.

</details>

### 🤖 Running the Bot Locally

```bash
python3 -m bot
```

↪️ If everything is set up correctly, the bot should be running. Use `/start` to check.

---

## 💪 Docker Setup (Recommended)

If you want to run the bot using Docker, follow these steps:

### **1️⃣ Build and Run the Docker Container**

1. **Ensure `config.py` is updated with your credentials.**
2. **Build the Docker Image**
   ```bash
   docker build -t youtube-uploader-bot .
   ```
3. **Run the Container**
   ```bash
   docker run -d --name yt-bot youtube-uploader-bot
   ```

✅ No need to specify `--env-file` manually! The bot now reads configurations directly from `config.py`.

---

## 🔔Notes

- **Daily Upload Limit**: The YouTube API allows ~6 uploads per day due to quota limits.
- **Unverified Apps**: Uploaded videos will remain private unless the app is verified by Google.
- **Copyright**: Uploading copyrighted content may lead to video removal.

## 🤙🏻Contact

For support, contact **[๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ](https://telegram.dog/itz_lumino)**.

## 🧪License

Released under [GNU GPL v3.0](LICENSE).
