
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
    
    def connect(self, constr: str) -> None:
        self.__ensure_dir(constr)
        self.conn = sqlite3.connect(constr)
        self.connected = True
    
    def disconnect(self) -> None:
        self.conn.close()
        self.connected = False
    
    def save(self, message: discord.Message) -> None:
        self.log.info(message.content)
    
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
        
