# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from configparser import ConfigParser

# UniShop Engine
from .paths import UNISHOP_CFG_PATH, get_server_file


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
CONFIG_FILE = get_server_file(UNISHOP_CFG_PATH / "config.ini")

config = ConfigParser()
config.read(CONFIG_FILE)
