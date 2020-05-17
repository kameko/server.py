
import logging
import sqlite3
import os
import discord
from .events import Events

class DiscordDatabase:
    def __init__(self, logger: logging.Logger, events: Events):
        self.connected = False
        self.log       = logger
        self.events    = events
        self.events.on_discord_message_recieve(self.__handle_message_recieve)
    
    def configure_event_handler(self, constr: str, stay_open: bool = True) -> None:
        self.__constr    = constr
        self.__stay_open = stay_open
    
    def connect(self, constr: str, ensure_create: bool = True) -> None:
        self.__ensure_dir(constr)
        self.conn = sqlite3.connect(constr)
        if ensure_create:
            self.ensure_create()
        self.connected = True
    
    def ensure_create(self) -> None:
        if not self.connected:
            raise ValueError("Database not connected.")
        c = self.conn.cursor()
        c.execute(
            """
                CREATE TABLE IF NOT EXISTS messages
                (
                    id                   INTEGER PRIMARY KEY,
                    message_id           INTEGER,
                    message_content      TEXT,
                    author_name          TEXT,
                    author_display       TEXT,
                    author_discriminator INTEGER,
                    author_id            INTEGER
                )
            """)
        c.commit()
    
    def disconnect(self) -> None:
        self.conn.close()
        self.connected = False
    
    def save(self, message: discord.Message) -> None:
        if not self.connected:
            raise ValueError("Database not connected.")
        entities = (
                message.id,
                message.content,
                message.author.name,
                message.author.display_name,
                message.author.discriminator,
                message.author.id
            )
        c = self.conn.cursor()
        c.execute(
            """
                INSERT INTO messages
                (
                    message_id,
                    message_content,
                    author_name,
                    author_display,
                    author_discriminator,
                    author_id
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """,
            entities
        )
    
    def update(self, message: discord.Message) -> None:
        pass
    
    def __handle_message_recieve(self, sender: object, message: discord.Message) -> None:
        try:
            if not self.connected:
                self.connect(self.__constr)
            self.save(message)
        finally:
            if not self.__stay_open:
                self.disconnect()
    
    def __ensure_dir(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
