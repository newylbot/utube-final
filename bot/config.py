class Config:
    # Telegram API credentials
    BOT_TOKEN = "Add your BOT TOKEN here"
    SESSION_NAME = "Add your BOT USERNAME here" # Without @
    API_ID = 123456  # Replace with your API ID
    API_HASH = "ADD your API HASH here"

    # YouTube API credentials
    CLIENT_ID = "Add your client ID here"
    CLIENT_SECRET = "Add your client SECRET here"

    # Bot owner and authorized users
    BOT_OWNER = 123456789  # Replace with your Telegram user ID
    AUTH_USERS = [BOT_OWNER, 123456789]  # Add more user IDs as needed

    # Video settings
    VIDEO_DESCRIPTION = "" # Your default video description
    VIDEO_CATEGORY = 22  # Default category (change as needed)
    VIDEO_TITLE_PREFIX = ""
    VIDEO_TITLE_SUFFIX = " |-๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ"

    # Default Thumbnail (Optional)
    THUMBNAIL_FILE = "bot/t.png"  # Change to the correct filename
    
    #_____WATERMARK-SECTION_____#
    # Enable watermarking (True = ON, False = OFF)
    # Currently in Beta Stage... Might Not work Properly.... This will add permanent watermark on your video....  Use with at your OWN RISK......
    WATERMARK_ENABLED = False
    # Path to watermark image
    WATERMARK_IMAGE = "bot/t.png"
    # Watermark position (topleft, topright, bottomleft, bottomright)
    WATERMARK_POSITION = "bottomright"
    
    # Debugging
    DEBUG = True

    # Upload mode (public, private, unlisted)
    UPLOAD_MODE = "unlisted"

    # Credential file for YouTube authentication
    CRED_FILE = "auth_token.txt"
