
import logging
from .discord_handler import DiscordHandler

class Server:
    def __init__(self):
        self.setup_logging()
    
    def connect(self, token: str):
        self.dh = DiscordHandler()
        self.dh.run(token)
    
    def setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("server.py")
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s: %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        self.log = logger
        return logger
