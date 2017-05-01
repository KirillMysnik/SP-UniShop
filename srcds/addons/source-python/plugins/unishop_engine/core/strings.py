# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from translations.strings import LangStrings

# UniShop Engine
from ..info import info


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def insert_chat_tag(message):
    message = message.tokenized(**message.tokens, **COLOR_SCHEME)
    message = common_strings['chat_base'].tokenized(
        message=message, **COLOR_SCHEME)

    return message


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
COLOR_SCHEME = {
    'color_tag': '\x01',
    'color_highlight': '\x03',
    'color_default': '\x01',
    'color_error': '\x03',
}

common_strings = LangStrings(info.name + "/strings")
config_strings = LangStrings(info.name + "/config")
