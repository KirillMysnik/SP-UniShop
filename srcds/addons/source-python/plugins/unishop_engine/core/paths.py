# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from paths import CFG_PATH, LOG_PATH, PLUGIN_DATA_PATH

# UniShop Engine
from ..info import info


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_server_file(path):
    server_path = path.dirname() / (path.namebase + "_server" + path.ext)
    if server_path.isfile():
        return server_path
    return path


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
UNISHOP_CFG_PATH = CFG_PATH / info.name
UNISHOP_LOG_PATH = LOG_PATH / info.name
UNISHOP_DATA_PATH = PLUGIN_DATA_PATH / info.name
