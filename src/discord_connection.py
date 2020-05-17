
import discord
import logging
from .events import Events

class DiscordConnection(discord.Client):
    def __init__(self, logger: logging.Logger, events: Events):
        self.log    = logger
        self.events = events
        super().__init__()
    
    async def on_ready(self) -> None:
        self.log.info("Connected to Discord as " + self.user.name)
    
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return
        
        if message.content == "shutdown":
            self.events.request_system_shutdown(self)
            await self.change_presence(status=discord.Status.offline)
            await self.close()
            return
        self.events.request_on_discord_message_recieve(self, message)