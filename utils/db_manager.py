# db_manager.py
import sqlite3
from datetime import datetime
import base64

class DatabaseManager:
    def __init__(self, db_name="finConnect.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            profile_img TEXT
        )
        """
        )
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            image_data TEXT,
            caption TEXT,
            post_time TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        )
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY,
            post_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        )
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            post_id INTEGER,
            user_id INTEGER,
            comment TEXT,
            comment_time TEXT,
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        )
        self.conn.commit()

    def add_user(self, username, profile_img_base64):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO users (username, profile_img) VALUES (?, ?)",
            (username, profile_img_base64),
        )
        self.conn.commit()

    def add_post(self, user_id, image_base64, caption):
        c = self.conn.cursor()
        post_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO posts (user_id, image_data, caption, post_time) VALUES (?, ?, ?, ?)",
            (user_id, image_base64, caption, post_time),
        )
        self.conn.commit()

    def add_like(self, post_id, user_id):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO likes (post_id, user_id) VALUES (?, ?)", (post_id, user_id)
        )
        self.conn.commit()

    def add_comment(self, post_id, user_id, comment):
        c = self.conn.cursor()
        comment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO comments (post_id, user_id, comment, comment_time) VALUES (?, ?, ?, ?)",
            (post_id, user_id, comment, comment_time),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
