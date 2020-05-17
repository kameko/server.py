
import logging
from src.discord_handler import DiscordHandler
from src.server import Server

def setup_logger() -> None:
    logger = logging.getLogger("server.py")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def setup_depends() -> None:
    global server
    log     = logging.getLogger("server.py")
    discord = DiscordHandler(log)
    server  = Server(log, discord)

def read_discord_token() -> None:
    global discord_token
    try:
        token_file = open(".token", "r")
        discord_token = token_file.read()
    finally:
        token_file.close()

def main() -> None:
    setup_logger()
    setup_depends()
    read_discord_token()
    server.connect(discord_token)

main()
