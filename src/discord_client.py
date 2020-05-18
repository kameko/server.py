
import logging
import discord
import asyncio
from .events import Events

# TODO: make a folder and config for each new guild. do not acknowledge the
# guild in any way (not even save messages, but respect commands) if the
# auto-generated config is not set up (either manually or through a command)

class DiscordClient(discord.Client):
    def __init__(self, logger: logging.Logger, events: Events):
        super().__init__()
        self.log    = logger
        self.events = events
        self.commands = []
        self.cancelled = False
        self.events.on_system_shutdown(self.__handle_system_shutdown)
    
    async def disconnect(self) -> None:
        await self.change_presence(status=discord.Status.invisible)
        await self.close()
    
    async def on_ready(self) -> None:
        self.log.info("Connected to Discord as " + self.user.name)
        game = discord.Game("prototype")
        await self.change_presence(status=discord.Status.online, activity=game)
    
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return
        if self.cancelled:
            await self.change_presence(status=discord.Status.invisible)
            await self.close()
            
        block = False
        for command in self.commands:
            if command.detect(message):
                block = command.block_event
                await command.handle(message)
        if not block:
            self.events.request_on_discord_message_recieve(self, message)
    
    def __handle_system_shutdown(self, caller: object) -> None:
        self.cancelled = True
