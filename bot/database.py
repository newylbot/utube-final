from pymongo import MongoClient
from bot.config import Config  # ✅ Import Config properly

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URL)
        self.db = self.client['utube_bot']  # Database name
        self.collection = self.db['settings']  # Collection name

        # Initialize settings if not exists
        if self.collection.count_documents({}) == 0:
            self.collection.insert_one({
                "video_title_prefix": "",
                "video_title_suffix": " |-๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ",
                "playlist_id": ""
            })

    def get_settings(self):
        return self.collection.find_one()

    def update_setting(self, key, value):
        self.collection.update_one({}, {"$set": {key: value}})
