import sqlite3
from bot.config import Config

class Database:
    def __init__(self):
        # Connect to SQLite database (it will create it if it doesn't exist)
        self.conn = sqlite3.connect('bot_config.db')  # SQLite database file
        self.cursor = self.conn.cursor()

        # Create settings table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Initialize default settings if not already in the database
        self._initialize_settings()

    def _initialize_settings(self):
        # Insert default settings if the table is empty
        self.cursor.execute('SELECT COUNT(*) FROM settings')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
                INSERT INTO settings (key, value) VALUES
                ('video_title_prefix', ''),
                ('video_title_suffix', ' |-๏ ʟᴜᴍɪɴᴏ ⇗ ˣᵖ'),
                ('playlist_id', '')
            ''')
            self.conn.commit()

    def get_settings(self):
        # Fetch all settings from the database
        self.cursor.execute('SELECT key, value FROM settings')
        settings = dict(self.cursor.fetchall())
        return settings

    def update_setting(self, key, value):
        # Update a specific setting in the database
        self.cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)
        ''', (key, value))
        self.conn.commit()

    def close(self):
        # Close the database connection when done
        self.conn.close()
