
import logging
import discord
from ..events import Events

class BaseCommand:
    def __init__(self, logger: logging.Logger, events: Events, command_name: str):
        self.log = logger
        self.events = events
        self.command_name = command_name
        self.block_event = False
    
    async def detect(self, message: discord.Message) -> bool:
        raise NotImplementedError("Please Implement this method")
    
    async def handle(self, message: discord.Message) -> None:
        raise NotImplementedError("Please Implement this method")
    
