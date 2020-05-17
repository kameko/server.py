
import logging
from src.events import Events
from src.discord_database import DiscordDatabase
from src.discord_connection import DiscordConnection
from src.server import Server

def setup_logger(level) -> logging.Logger:
    logger    = logging.getLogger("server.py")
    handler   = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s: %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

def setup_depends() -> Server:
    log        = logging.getLogger("server.py")
    events     = Events()
    discord_db = DiscordDatabase(log, events)
    discord_db.configure_event_handler("./.data/discord/messages.db")
    discord    = DiscordConnection(log, events)
    server     = Server(log, events, discord)
    return server

def read_discord_token() -> str:
    try:
        token_file    = open(".token", "r")
        discord_token = token_file.readline()
        return discord_token
    finally:
        token_file.close()

def main() -> None:
    logger        = setup_logger(logging.DEBUG)
    server        = setup_depends()
    discord_token = read_discord_token()
    
    server.connect_to_discord(discord_token)
    server.wait_for_shutdown_request()
