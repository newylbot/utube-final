import subprocess
import time
import re
from pyrogram import Client
from bot.config import Config  # Import API credentials
from pyrogram.enums import ParseMode

LOG_MONITOR_PATTERN = r"AttributeError: type object 'Messages' has no attribute 'DAILY_QOUTA_REACHED'"
first_start = True  # Flag to track if it's the first start or a restart

def send_message(is_restart=False):
    """Send a message to Telegram when the bot starts or restarts."""
    message = "<b>🤖 Bot Started Fresh....\n\nHit /start and follow the instructions...\n\nIf already done....\n🔥Start Uploading...</b>" if not is_restart else "<b>🔄 Bot restarted automatically due to Quota Exceeded.\n\n⌛Wait for 5 to 7 seconds to initialize...\n\n💻Then Start uploading again.....</b>"

    try:
        with Client("supervisor", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN) as app:
            app.send_message(Config.BOT_OWNER, message, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(f"[๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ Said] Failed to send message: {e}")

def restart_bot(is_restart=False):
    """Restart the bot process and send a Telegram message."""
    global first_start

    if first_start:
        print("\n[๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ Said] Bot is starting for the first time...")
        first_start = False
    else:
        print("\n[๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ Said] Restarting bot due to error...")

    send_message(is_restart=is_restart)  # Send restart or first-start message
    time.sleep(3)  # Delay before restart
    return subprocess.Popen(["python3", "-m", "bot"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def monitor_bot():
    """Monitor the bot logs and restart on error."""
    bot_process = restart_bot(is_restart=False)  # First start message

    while True:
        try:
            for line in bot_process.stderr:
                print(line, end="")  # Print logs in real-time

                if re.search(LOG_MONITOR_PATTERN, line):
                    print("\n[๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ Said] Error detected! Restarting bot...\n")
                    bot_process.kill()
                    bot_process = restart_bot(is_restart=True)  # Restart message

        except Exception as e:
            print(f"\n[๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ Said] Exception: {e}")
            bot_process.kill()
            time.sleep(5)
            bot_process = restart_bot(is_restart=True)  # Restart message

if __name__ == "__main__":
    monitor_bot()
