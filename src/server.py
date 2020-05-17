
import logging
import time
import threading
import asyncio
from .events import Events
from .discord_handler import DiscordHandler

class Server:
    def __init__(self, logger: logging.Logger, events: Events, discord: DiscordHandler):
        self.log       = logger
        self.events    = events
        self.discord   = discord
        self.cancelled = False
        self.events.on_system_shutdown(self.__handle_system_shutdown)
    
    def connect(self, token: str) -> None:
        self.discord_thread = threading.Thread(target=self.__start_client, args=(token,))
        self.discord_thread.start()
        self.discord_dc_waiter = threading.Thread(target=self.__wait_for_disconnect_request)
        self.discord_dc_waiter.start()
    
    def disconnect(self) -> None:
        self.cancelled = True
    
    def wait_for_shutdown_request(self) -> None:
        while not self.cancelled:
            time.sleep(0.5)
    
    def __handle_system_shutdown(self, caller: object) -> None:
        self.log.info("System shutdown requested by %s.", str(caller))
        self.cancelled = True
    
    def __start_client(self, token: str) -> None:
        self.discord.run(token)
    
    def __wait_for_disconnect_request(self) -> None:
        while not self.cancelled:
            time.sleep(0.5)
        asyncio.run(self.discord.close())
        self.discord_thread.join()
