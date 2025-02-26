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

## 🛠Setup

### Clone & Virtual Environment (For Local Setup)

```bash
git clone https://github.com/odysseusmax/utube.git
cd utube
python3 -m venv venv
source venv/bin/activate
```

### ⏬Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 📌Environment Variables

There is a `.env` file named `add_variables.env`. Add your details inside this file before running the bot:

```
API_ID=your_api_id_here
API_HASH=your_api_hash_here
BOT_TOKEN=your_bot_token_here
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
BOT_OWNER=your_bot_owner_id_here
SESSION_NAME=your_session_name_here
DEBUG=true
UPLOAD_MODE=unlisted
```

### 🔑 Getting Google API Credentials (Client ID & Secret)

To use the YouTube Data API, you need Google API credentials:

1. **Go to the Google Cloud Console**: [GCP Cloud Conole](https://console.developers.google.com)
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
5. **Copy your `Client ID` and `Client Secret`** and add them to `add_variables.env`.

## 💻Setting Environment Variables in VPS (For Manual Setup)

To set environment variables only on a VPS, use the following commands:

```bash
export API_ID="your_api_id_here"
export API_HASH="your_api_hash_here"
export BOT_TOKEN="your_bot_token_here"
export CLIENT_ID="your_client_id_here"
export CLIENT_SECRET="your_client_secret_here"
export BOT_OWNER="your_bot_owner_id_here"
export SESSION_NAME="your_session_name_here"
export DEBUG="true"
export UPLOAD_MODE="unlisted"
```

### 🤖Running the Bot Locally

```bash
python3 -m bot
```

↪️If everything is set up correctly, the bot should be running. Use `/start` to check.

---

## 🐳 Docker Setup (Recommended)

If you want to run the bot using Docker, follow these steps:

### **1️⃣ Build and Run the Docker Container**

1. **Add your details in the `add_variables.env` file.**
2. **Build the Docker Image**
   ```bash
   docker build -t youtube-uploader-bot .
   ```
3. **Run the Container**
   ```bash
   docker run -d --name yt-bot youtube-uploader-bot
   ```

**No need to manually specify `--env-file`!**
The `Dockerfile` automatically loads the environment variables from `add_variables.env` inside the container.

---

## 🔔Notes

- **Daily Upload Limit**: The YouTube API allows ~6 uploads per day due to quota limits.
- **Unverified Apps**: Uploaded videos will remain private unless the app is verified by Google.
- **Copyright**: Uploading copyrighted content may lead to video removal.

## 🤙🏻Contact

For support, contact **[๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ](https://telegram.dog/itz_lumino)**.

## 🪪License

Released under [GNU GPL v3.0](LICENSE).

