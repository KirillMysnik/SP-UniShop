# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from plugins.manager import plugin_manager

# UniShop
from .listeners import (
    on_unishop_available_listener_manager,
    on_unishop_unavailable_listener_manager)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
UNISHOP_ENGINE_PLUGIN_NAME = "unishop_engine"


# =============================================================================
# >> CLASSES
# =============================================================================
class UniShopEngine(dict):
    def __init__(self):
        super().__init__()

        self._plugin = None
        self.plugin = plugin_manager.get_plugin_instance(
            UNISHOP_ENGINE_PLUGIN_NAME)

    def set_plugin(self, plugin):
        if self._plugin is None and plugin is None:
            return

        if self._plugin is not None and plugin is not None:
            return

        self._plugin = plugin

        if plugin is None:
            self.clear()
            on_unishop_unavailable_listener_manager.notify()
        else:
            self.update(self._plugin.module.get_external_interface_dict())
            on_unishop_available_listener_manager.notify()

    plugin = property(fset=set_plugin)

    @property
    def available(self):
        return self._plugin is not None

    def __getattr__(self, key):
        if key in self:
            return self[key]

        raise AttributeError

unishop_engine = UniShopEngine()
