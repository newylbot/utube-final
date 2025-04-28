import subprocess
import time
import sys
from pyrogram import Client
from bot.config import Config  # Import API credentials
from pyrogram.enums import ParseMode
from fastapi import FastAPI
import uvicorn
import threading
import os

LOG_MONITOR_PATTERN = r"AttributeError: type object 'Messages' has no attribute 'DAILY_QOUTA_REACHED'"
first_start = True  # Flag to track if it's the first start or a restart

# Initialize FastAPI to keep Koyeb instance alive
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Bot is running"}

def start_fastapi():
    """Start FastAPI server only if it's not already running."""
    if not os.environ.get("FASTAPI_STARTED"):  # Prevent multiple starts
        os.environ["FASTAPI_STARTED"] = "1"
        uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

def send_message(is_restart=False):
    """Send a message to Telegram when the bot starts or restarts."""
    message = (
        "<b>🤖 Bot Started Fresh....\n\nHit /start and follow the instructions...\n\n"
        "If already done....\n🔥Start Uploading...</b>"
        if not is_restart else
        "<b>🔄 Bot restarted automatically due to Quota Exceeded.\n\n"
        "⌛Wait for 5 to 7 seconds to initialize...\n\n"
        "💻Then Start uploading again.....</b>"
    )

    try:
        with Client("supervisor", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN) as app:
            app.send_message(Config.BOT_OWNER, message, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(f"[Bot] Failed to send message: {e}")

def restart_bot(is_restart=False):
    """Restart the bot process and send a Telegram message."""
    global first_start

    if first_start:
        print("\n[Bot] Starting for the first time...")
        first_start = False
    else:
        print("\n[Bot] Restarting due to an error...")

    send_message(is_restart=is_restart)  # Send restart or first-start message
    time.sleep(3)  # Delay before restart

    return subprocess.Popen(
        ["python3", "-m", "bot"], 
        stdout=sys.stdout,  # Send logs to console
        stderr=sys.stderr,  # Send errors to console
        text=True
    )

def monitor_bot():
    """Monitor the bot logs and restart on error."""
    bot_process = restart_bot(is_restart=False)  # First start message

    while True:
        try:
            bot_process.wait()  # Wait for process to exit

            print("\n[Bot] Process exited! Restarting...\n")
            bot_process = restart_bot(is_restart=True)  # Restart message

        except Exception as e:
            print(f"\n[Bot] Exception: {e}")
            bot_process.kill()
            time.sleep(5)
            bot_process = restart_bot(is_restart=True)  # Restart message

if __name__ == "__main__":
    # Start FastAPI in a separate thread (only once)
    threading.Thread(target=start_fastapi, daemon=True).start()
    # Start monitoring the bot
    monitor_bot()
