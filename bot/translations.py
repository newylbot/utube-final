class Messages:

    START_MSG = (
        "👋 Hi there, {}!\n\n"
        "I'm **YouTube Uploader Bot**. I can upload any Telegram video to YouTube 📤.\n"
        "Just **authorize** me first, then send me a video.\n\n"
        "Check /help for more info. 🚀"
    )

    HELP_MSG = [
        "📌 **How I Work:**\n"
        "1️⃣ **Authorize** me to upload to your YouTube channel. 📲\n"
        "2️⃣ **Forward** any Telegram video to me. 🎥\n"
        "3️⃣ **Reply** `/upload` or `/u` to upload. You can also add a title after the command.\n"
        "4️⃣ I **process & upload** the video to YouTube. 🚀\n"
        "5️⃣ You get the **YouTube link** after the upload. ✅",
        
        "📺 **Create a YouTube Channel:**\n"
        "1️⃣ Sign in to YouTube on your phone or PC. 🖥️\n"
        "2️⃣ Try uploading a video or creating a playlist. 🎬\n"
        "3️⃣ If you don’t have a channel yet, follow the steps to create one. 🔥\n"
        "4️⃣ Confirm & start uploading! 🚀",
        
        "✅ **Verify Your YouTube Account:**\n"
        "⚠️ Unverified accounts can only upload videos up to 15 minutes.\n"
        "[Verify your account here](http://www.youtube.com/verify) 🔗",
        
        "🔑 **Authorize Me:**\n"
        "1️⃣ Click the provided link & allow access. 🔗\n"
        "2️⃣ Copy the given code. 📋\n"
        "3️⃣ Come back & send `/authorise copied-code` or `/a`.\n\n"
        "🔒 Your privacy is safe. I only help with uploads!"
    ]

    NOT_A_REPLY_MSG = "❌ Please **reply** to a video file."

    NOT_A_MEDIA_MSG = "⚠️ No media found. " + NOT_A_REPLY_MSG

    NOT_A_VALID_MEDIA_MSG = "⛔ This is not a valid media file."

    DAILY_QUOTA_REACHED = "🚫 You have reached YouTube’s daily upload limit (6 videos). Try again tomorrow! ⏳"

    PROCESSING = "⏳ Processing your request..."

    NOT_AUTHENTICATED_MSG = "🔑 You haven't **authorized** me yet. See /help for instructions."

    NO_AUTH_CODE_MSG = "❌ No code found! Please provide a valid authorization code."

    AUTH_SUCCESS_MSG = "✅ **Authorization Successful!**\nYou're ready to upload to YouTube. 🎉"

    AUTH_FAILED_MSG = "❌ **Authentication Failed!**\nReason: `{}`"

    AUTH_DATA_SAVE_SUCCESS = "✅ **Auth Data Saved Successfully!**"
