
import logging
import time
import threading
from .events import Events
from .discord_client import DiscordClient

class Server:
    def __init__(self, logger: logging.Logger, events: Events, discord: DiscordClient):
        self.log       = logger
        self.events    = events
        self.discord   = discord
        self.cancelled = False
        self.events.on_system_shutdown(self.__handle_system_shutdown)
    
    def connect_to_discord(self, token: str) -> None:
        self.discord.run(token)
    
    def disconnect_from_discord(self) -> None:
        self.cancelled = True
    
    def wait_for_shutdown_request(self) -> None:
        while not self.cancelled:
            time.sleep(0.5)
    
    def __handle_system_shutdown(self, caller: object) -> None:
        self.log.info("System shutdown requested by %s.", str(caller))
        # self.cancelled = True
        self.disconnect_from_discord()
    
