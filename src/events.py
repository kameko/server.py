
from typing import Callable
import discord

class Events:
    def __init__(self):
        self.system_shutdown_callbacks = []
        self.discord_message_recieve_callbacks = []
        self.discord_message_updated_callbacks = []
    
    # system
    
    def on_system_shutdown(self, callback: Callable[[object], None]) -> None:
        self.system_shutdown_callbacks.append(callback)
    
    def request_system_shutdown(self, sender: object) -> None:
        for callback in self.system_shutdown_callbacks:
            callback(sender)
    
    # discord
    
    def on_discord_message_recieve(self, callback: Callable[[object, discord.Message], None]) -> None:
        self.discord_message_recieve_callbacks.append(callback)
    
    def request_on_discord_message_recieve(self, sender: object, message: discord.Message) -> None:
        for callback in self.discord_message_recieve_callbacks:
            callback(sender, message)
    
    def on_discord_message_updated(self, callback: Callable[[object, discord.Message, discord.Message], None]) -> None:
        self.discord_message_updated_callbacks.append(callback)
    
    def request_on_discord_message_updated(self, sender: object, old_message: discord.Message, new_message: discord.Message) -> None:
        for callback in self.discord_message_updated_callbacks:
            callback(sender, old_message, new_message)
    
