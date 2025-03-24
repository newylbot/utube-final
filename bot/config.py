class Config:
    # Telegram API credentials
    BOT_TOKEN = ""  # Replace with your bot token
    SESSION_NAME = "" # Without @ Add Your bot Username
    API_ID = 123456  # Replace with your API ID
    API_HASH = "" # Add your API Hash Here

    # YouTube API credentials
    CLIENT_ID = "" # Add your Client ID here
    CLIENT_SECRET = "" # Add your Client ID Secret

    # Bot owner and authorized users
    BOT_OWNER = 1234567890  # Replace with your Telegram user ID
    AUTH_USERS = [BOT_OWNER, 1234567890]  # Add more user IDs as needed

    # Video settings
    VIDEO_DESCRIPTION = "" # Your default video description
    VIDEO_CATEGORY = 27  # Default category (change as needed)
    VIDEO_TITLE_PREFIX = ""
    VIDEO_TITLE_SUFFIX = " |-๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ"

    # Default Thumbnail (Optional)
    THUMBNAIL_FILE = "bot/t.png"  # Change to the correct filename
    
    # Add Playlist ID here to add your Videos in a Specific Playlist
    PLAYLIST_ID = "" # Add your Playlist ID here

    YOUTUBE_API_SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.readonly"
]

    #_____WATERMARK-SECTION_____#
    # Enable watermarking (True = ON, False = OFF)
    # Currently in Beta Stage... Might Not work Properly.... 
    # This will add permanent watermark on your video....  
    # Use with at your OWN RISK......
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
