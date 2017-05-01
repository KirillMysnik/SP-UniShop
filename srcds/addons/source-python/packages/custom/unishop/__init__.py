# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from listeners import OnPluginLoaded, OnPluginUnloaded

# UniShop
from .engine import unishop_engine, UNISHOP_ENGINE_PLUGIN_NAME


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnPluginLoaded
def listener_on_plugin_loaded(plugin):
    if plugin.name == UNISHOP_ENGINE_PLUGIN_NAME:
        unishop_engine.plugin = plugin


@OnPluginUnloaded
def listener_on_plugin_unloaded(plugin):
    if plugin.name == UNISHOP_ENGINE_PLUGIN_NAME:
        unishop_engine.plugin = None
