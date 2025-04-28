import subprocess
import time
import sys
import threading
import os
import logging
from pyrogram import Client
from bot.config import Config  # Import your API credentials
from pyrogram.enums import ParseMode
from fastapi import FastAPI
import uvicorn

import logging

def clean_logging():
    """Fully silence unwanted logs."""
    # Set the root logger to the highest level to silence unwanted logs
    logging.basicConfig(level=logging.CRITICAL)
    
    # Set pymongo, motor, asyncio, httpx, and other relevant libraries to the highest level
    for logger_name in ["pymongo", "motor", "asyncio", "httpx", "uvicorn"]:
        logging.getLogger(logger_name).setLevel(logging.CRITICAL)

    # Specifically silence the pyrogram logs too, which might be verbose in your case
    logging.getLogger("pyrogram").setLevel(logging.CRITICAL)
    
    # Disable any additional loggers that pymongo uses internally
    logging.getLogger("pymongo.topology").setLevel(logging.CRITICAL)
    logging.getLogger("pymongo.connection").setLevel(logging.CRITICAL)
    logging.getLogger("pymongo.command").setLevel(logging.CRITICAL)

    # Silence specific internal logs that might still show up
    logging.getLogger("pyrogram.connection.connection").setLevel(logging.CRITICAL)
    logging.getLogger("pyrogram.session.session").setLevel(logging.CRITICAL)
    logging.getLogger("pyrogram.client").setLevel(logging.CRITICAL)

clean_logging()

# --- BOT SUPERVISOR SECTION ---
LOG_MONITOR_PATTERN = r"AttributeError: type object 'Messages' has no attribute 'DAILY_QUOTA_REACHED'"
first_start = True  # Track if it's the first startup

# Initialize FastAPI server to keep bot alive (for Koyeb/Heroku etc.)
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Bot is running"}

def start_fastapi():
    """Start FastAPI server only once."""
    if not os.environ.get("FASTAPI_STARTED"):
        os.environ["FASTAPI_STARTED"] = "1"
        port = int(os.getenv("PORT", 8080))  # Make port configurable
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

def send_message(is_restart=False):
    """Send message to owner on start or restart."""
    message = (
        "<b>🤖 Bot Started Fresh....\n\nHit /start and follow the instructions...\n\n"
        "If already done....\n🔥Start Uploading...</b>"
        if not is_restart else
        "<b>🔄 Bot restarted automatically due to Quota Exceeded.\n\n"
        "⌛ Wait for 5 to 7 seconds to initialize...\n\n"
        "💻 Then Start uploading again.....</b>"
    )

    try:
        with Client("supervisor", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN) as app:
            app.send_message(Config.BOT_OWNER, message, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(f"[Bot] Failed to send start/restart message: {e}")

def restart_bot(is_restart=False):
    """Restart the bot and send notification."""
    global first_start

    if first_start:
        print("\n[Bot] Starting for the first time...")
        first_start = False
    else:
        print("\n[Bot] Restarting bot due to crash/error...")

    send_message(is_restart=is_restart)
    time.sleep(3)

    try:
        return subprocess.Popen(
            ["python3", "-m", "bot"],
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
    except Exception as e:
        print(f"[Bot] Failed to start bot process: {e}")
        sys.exit(1)

def monitor_bot():
    """Monitor bot process and restart on crash."""
    bot_process = restart_bot(is_restart=False)

    while True:
        try:
            bot_process.wait()  # Wait until bot stops
            print("\n[Bot] Bot process exited! Restarting...\n")
            bot_process = restart_bot(is_restart=True)

        except KeyboardInterrupt:
            print("\n[Bot] Supervisor received shutdown signal. Exiting gracefully...")
            bot_process.terminate()
            sys.exit(0)

        except Exception as e:
            print(f"\n[Bot] Supervisor Exception: {e}")
            bot_process.kill()
            time.sleep(5)
            bot_process = restart_bot(is_restart=True)

if __name__ == "__main__":
    # Start FastAPI server in background
    threading.Thread(target=start_fastapi, daemon=True).start()
    # Start monitoring and restarting bot
    monitor_bot()
