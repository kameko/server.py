
import logging
import discord
from .base import BaseCommand
from ..events import Events
from ..discord_client import DiscordClient

class ShutdownCommand(BaseCommand):
    def __init__(self, logger: logging.Logger, events: Events, discord: DiscordClient):
        super().__init__(logger, events, "Shutdown")
        self.discord = discord
        self.block_event = True
    
    def detect(self, message: discord.Message) -> bool:
        if message.content.lower() == "shutdown":
            # TODO: get authorized user names
            return True
        return False
    
    async def handle(self, message: discord.Message) -> None:
        self.events.request_system_shutdown(self)
        await self.discord.disconnect()

