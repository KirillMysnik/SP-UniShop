# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from commands import CommandReturn
from commands.typed import TypedClientCommand, TypedSayCommand
from messages import HudDestination, SayText2, TextMsg

# UniShop Engine
from .core.global_item_manager import global_item_manager
from .core.shop_clients import shop_clients
from .core.strings import common_strings, insert_chat_tag


# =============================================================================
# >> EXTERNAL INTERFACE SETUP
# =============================================================================
_external_interfaces = []


def external_interface(func):
    _external_interfaces.append(func)
    return func


# =============================================================================
# >> EXTERNAL INTERFACES
# =============================================================================
@external_interface
def create_item(plugin_name, class_id, subclass_id):
    return global_item_manager.create_item(plugin_name, class_id, subclass_id)


@external_interface
def shop_client_from_userid(userid):
    return shop_clients.from_userid(userid)


@external_interface
def shop_client_from_database_id(database_id):
    return shop_clients.from_database_id(database_id)


@external_interface
def shop_client_from_index(index):
    return shop_clients[index]


@external_interface
def send_shop_motd(index):
    pass


@external_interface
def send_shop_popup(index):
    pass


@external_interface
def send_inventory_motd(index):
    pass


@external_interface
def send_inventory_popup(index):
    pass


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_external_interface_dict():
    result = {}
    for interface in _external_interfaces:
        result[interface.__name__] = interface

    return result


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
say_text2_unknown_shop_mode = SayText2(insert_chat_tag(
    common_strings['error unknown_shop_mode']))

text_msg_unknown_shop_mode = TextMsg(common_strings['error unknown_shop_mode'],
    destination=HudDestination.CONSOLE)

say_text2_unknown_inventory_mode = SayText2(insert_chat_tag(
    common_strings['error unknown_inventory_mode']))

text_msg_unknown_inventory_mode = TextMsg(
    common_strings['error unknown_inventory_mode'],
    destination=HudDestination.CONSOLE)


# =============================================================================
# >> COMMANDS
# =============================================================================
@TypedClientCommand('shop')
@TypedSayCommand('!shop')
@TypedSayCommand('/shop')
def typed_shop(command_info, mode="motd"):
    try:
        {
            'motd': send_shop_motd,
            'popup': send_shop_popup,
        }[mode.lower()](command_info.index)

    except KeyError:
        if command_info.team_only is None:
            text_msg_unknown_shop_mode.send(command_info.index)
        else:
            say_text2_unknown_shop_mode.send(command_info.index)

    if command_info.command_string.startswith('/'):
        return CommandReturn.BLOCK


@TypedClientCommand('inventory')
@TypedSayCommand('!inventory')
@TypedSayCommand('/inventory')
def typed_inventory(command_info, mode="motd"):
    try:
        {
            'motd': send_inventory_motd,
            'popup': send_inventory_popup,
        }[mode.lower()](command_info.index)

    except KeyError:
        if command_info.team_only is None:
            text_msg_unknown_inventory_mode.send(command_info.index)
        else:
            say_text2_unknown_inventory_mode.send(command_info.index)

    if command_info.command_string.startswith('/'):
        return CommandReturn.BLOCK
