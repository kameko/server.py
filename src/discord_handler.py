
import discord
import logging

class DiscordHandler(discord.Client):
    def __init__(self):
        self.log = logging.getLogger("server.py")
        super().__init__()
    
    async def on_ready(self) -> None:
        self.log.info("Connected to Discord.")
    
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return
        
        self.log.info(message.content)
        
        if message.content == "shutdown":
            await self.change_presence(status=discord.Status.offline)
            await self.close()
            return
        await message.channel.send(message.content)