
import logging
import sqlite3
import os
import discord
from .events import Events

class DiscordDatabase:
    def __init__(self, logger: logging.Logger, events: Events):
        self.conn      = None
        self.connected = False
        self.log       = logger
        self.events    = events
        self.events.on_system_shutdown(self.__handle_system_shutdown)
        self.events.on_discord_message_recieve(self.__handle_message_recieve)
        self.events.on_discord_message_updated(self.__handle_message_updated)
    
    def configure_event_handler(self, constr: str, stay_open: bool = True) -> None:
        self.__constr    = constr
        self.__stay_open = stay_open
    
    def connect(self, constr: str, ensure_create: bool = True) -> None:
        self.__ensure_dir(constr)
        self.conn = sqlite3.connect(constr)
        self.connected = True
        if ensure_create:
            self.ensure_create()
    
    def ensure_create(self) -> None:
        if not self.connected:
            raise ValueError("Database not connected.")
        c = self.conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS messages
            (
                id                    INTEGER PRIMARY KEY,
                message_id            INTEGER,
                message_content       TEXT,
                creation_time         TEXT,
                author_id             INTEGER,
                author_name           TEXT,
                author_display        TEXT,
                author_discriminator  INTEGER,
                channel_id            INTEGER,
                channel_name          TEXT,
                guild_id              INTEGER,
                guild_name            TEXT,
                number_of_edits       INTEGER,
                number_of_attachments INTEGER
            )
            """)
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS message_edit_history
            (
                id                    INTEGER PRIMARY KEY,
                message_id            INTEGER,
                edit_time             TEXT,
                revision              INTEGER,
                new_content           TEXT
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS message_attachment
            (
                id                    INTEGER PRIMARY KEY,
                message_id            INTEGER,
                url                   TEXT,
                filename              TEXT,
                size_bytes            INTEGER
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS users
            (
                id                    INTEGER PRIMARY KEY,
                user_id               INTEGER,
                user_name             TEXT,
                user_disriminator     INTEGER,
                guilds_cvs            TEXT,
                permissions_cvs       TEXT
            )
            """
        )
        self.conn.commit()
    
    def disconnect(self) -> None:
        if self.connected and self.conn != None:
            self.conn.close()
        self.connected = False
    
    def save_message(self, message: discord.Message) -> None:
        if not self.connected:
            raise ValueError("Database not connected.")
        entities = (
                message.id,
                message.content,
                message.created_at.isoformat(timespec='seconds'),
                message.author.id,
                message.author.name,
                message.author.display_name,
                message.author.discriminator,
                message.channel.id,
                message.channel.name,
                message.channel.guild.id,
                message.channel.guild.name,
                0,
                len(message.attachments)
            )
        c = self.conn.cursor()
        try:
            c.execute(
                """
                INSERT INTO messages
                (
                    message_id,
                    message_content,
                    creation_time,
                    author_id,
                    author_name,
                    author_display,
                    author_discriminator,
                    channel_id,
                    channel_name,
                    guild_id,
                    guild_name,
                    number_of_edits,
                    number_of_attachments
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                entities
            )
            if len(message.attachments) > 0:
                for attach in message.attachments:
                    attach_entities = (
                        message.id,
                        attach.url,
                        attach.filename,
                        attach.size
                    )
                    c.execute(
                        """
                        INSERT INTO message_attachment
                        (
                            message_id,
                            url,
                            filename,
                            size_bytes
                        )
                        VALUES (?, ?, ?, ?)
                        """,
                        attach_entities
                    )
            self.conn.commit()
        except:
            self.conn.rollback()
            raise
    
    def update_message_content(self, old_message: discord.Message, new_message: discord.Message) -> None:
        if not self.connected:
            raise ValueError("Database not connected.")
        c = self.conn.cursor()
        try:
            # TODO: get old message. if it doesn't exist, return.
            # then, add old message to message_edit_history.
            # then, update message's number_of_edits and content
            c.execute("SELECT * FROM messages WHERE message_id = ?", (new_message.id,))
            
            rows = c.fetchmany(1)
            
            if len(rows) == 0:
                self.log.info("Tried to update a message with ID " + str(new_message.id) + " in the database, but it was not found.")
                return
            
            db_msg = rows[0]
            # TODO: https://docs.python.org/3.8/library/sqlite3.html#row-objects 
            self.conn.commit()
        except:
            self.conn.rollback()
            raise
    
    def save_or_update_discord_user(self, user) -> None:
        if not self.connected:
            raise ValueError("Database not connected.")
        c = self.conn.cursor()
        try:
            # TODO: ...
            self.conn.commit()
        except:
            self.conn.rollback()
            raise
    
    def commit(self) -> None:
        if not self.connected:
            raise ValueError("Database not connected.")
        self.conn.commit()
    
    def __handle_system_shutdown(self, sender: object) -> None:
        self.disconnect()
    
    def __handle_message_recieve(self, sender: object, message: discord.Message) -> None:
        try:
            if not self.connected:
                self.connect(self.__constr)
            self.save_message(message)
            self.save_or_update_discord_user(message.author)
        finally:
            if not self.__stay_open:
                self.disconnect()
    
    def __handle_message_updated(self, sender: object, old_message: discord.Message, new_message: discord.Message) -> None:
        if old_message.content == new_message.content and old_message.pinned != new_message.pinned:
            # message was only pinned, ignore it.
            return
        try:
            if not self.connected:
                self.connect(self.__constr)
            self.update_message_content(old_message, new_message)
        finally:
            if not self.__stay_open:
                self.disconnect()
    
    def __ensure_dir(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
