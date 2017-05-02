# =============================================================================
# >> IMPORTS
# =============================================================================
# UniShop
from .engine import unishop_engine
from .plugins import UniShopPlugin


# =============================================================================
# >> CLASSES
# =============================================================================
class ItemClass:
    items_consumed_per_use = 1

    def __init__(self, unishop_plugin, id_, lang_strings):
        if not isinstance(unishop_plugin, UniShopPlugin):
            raise ValueError("'unishop_pluign' argument must be a "
                             "valid UniShopPlugin instance")

        self.unishop_plugin = unishop_plugin
        self.id = id_
        self.lang_strings = lang_strings

        unishop_plugin.register_item_class(id_, self)

    def get_item_icon(self, item):
        return '/'.join((
            self.unishop_plugin.plugin_name, "icons", item.subclass + ".png"))

    def can_item_be_used(self, item):
        return True

    def on_item_created(self, item, creation_token):
        pass

    def on_item_deleted(self, item_id):
        pass

    def on_item_bought_from_shop(self, item, shop_client, price):
        pass

    def on_item_used(self, item):
        item.quantity -= self.items_consumed_per_use

    def create_item(self, subclass_id):
        if not unishop_engine.available:
            raise RuntimeError("UniShop Engine is not loaded")

        creation_token = unishop_engine.create_item(
            self.unishop_plugin.plugin_name, self.id, subclass_id)

        return creation_token
