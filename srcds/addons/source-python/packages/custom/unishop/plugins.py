# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from core import WeakAutoUnload


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
unishop_plugins = {}


# =============================================================================
# >> CLASSES
# =============================================================================
class UniShopPlugin(WeakAutoUnload):
    def __init__(self, plugin_name):
        if plugin_name in unishop_plugins:
            raise ValueError("Plugin name '{}' is already "
                             "registered".format(plugin_name))

        self._plugin_name = plugin_name
        self._item_classes = {}

        unishop_plugins[plugin_name] = self

    @property
    def plugin_name(self):
        return self._plugin_name

    def _unload_instance(self):
        del unishop_plugins[self._plugin_name]

    def register_item_class(self, item_class_id, item_class):
        if item_class_id in self._item_classes:
            raise ValueError("Item class with id '{}' is already "
                             "registered".format(item_class_id))

        self._item_classes[item_class_id] = item_class

    def unregister_item_class(self, item_class_id):
        del self._item_classes[item_class_id]

    def get_item_class(self, item_class_id):
        return self._item_classes.get(item_class_id)
