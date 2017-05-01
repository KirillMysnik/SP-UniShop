# =============================================================================
# >> IMPORTS
# =============================================================================
# UniShop
from .engine import unishop_engine
from .plugins import UniShopPlugin


# =============================================================================
# >> CLASSES
# =============================================================================
class ItemClassMeta:
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)

        if namespace.get('abstract', False):
            del cls.abstract
            return

        if not hasattr(cls, 'unishop_plugin'):
            raise ValueError("Class '{}' doesn't have 'unishop_plugin' "
                             "attribute".format(cls))

        if not hasattr(cls, 'id'):
            raise ValueError(
                "Class '{}' doesn't have 'id' attribute".format(cls))

        if cls.unishop_plugin is None:
            raise ValueError("Class '{}' has its 'unishop_plugin' "
                             "attribute set to None".format(cls))

        if cls.id is None:
            raise ValueError("Class '{}' has its 'id' "
                             "attribute set to None".format(cls))

        if not isinstance(cls.unishop_plugin, UniShopPlugin):
            raise ValueError("'unishop_pluign' attribute must be a "
                             "valid UniShopPlugin instance")

        cls.unishop_plugin.register_item_class(cls.id, cls)


class ItemClass(metaclass=ItemClassMeta):
    items_consumed_per_use = 1

    def __init__(self, unishop_plugin, id_, lang_strings):
        self.unishop_plugin = unishop_plugin
        self.id = id_
        self.lang_strings = lang_strings

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
