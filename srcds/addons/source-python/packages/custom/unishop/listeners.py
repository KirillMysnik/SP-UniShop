# =============================================================================
# >> IMPORTS
# =============================================================================
from listeners import ListenerManager, ListenerManagerDecorator


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
on_unishop_available_listener_manager = ListenerManager()
on_unishop_unavailable_listener_manager = ListenerManager()
on_item_created_listener_manager = ListenerManager()
on_item_pre_deleted_listener_manager = ListenerManager()
on_item_deleted_listener_manager = ListenerManager()
on_item_loaded_from_database_listener_manager = ListenerManager()
on_item_owner_changed_listener_manager = ListenerManager()
on_item_quantity_changed_listener_manager = ListenerManager()
on_item_name_or_description_changed_listener_manager = ListenerManager()
on_misplaced_item_discarded_listener_manager = ListenerManager()
on_item_bought_from_shop_listener_manager = ListenerManager()
on_item_used_listener_manager = ListenerManager()


# =============================================================================
# >> CLASSES
# =============================================================================
class OnUniShopAvailable(ListenerManagerDecorator):
    manager = on_unishop_available_listener_manager


class OnUniShopUnavailable(ListenerManagerDecorator):
    manager = on_unishop_unavailable_listener_manager


class OnItemCreated(ListenerManagerDecorator):
    manager = on_item_created_listener_manager


class OnItemDeleted(ListenerManagerDecorator):
    manager = on_item_deleted_listener_manager


class OnItemPreDeleted(ListenerManagerDecorator):
    manager = on_item_pre_deleted_listener_manager


class OnItemLoadedFromDatabase(ListenerManagerDecorator):
    manager = on_item_loaded_from_database_listener_manager


class OnItemOwnerChanged(ListenerManagerDecorator):
    manager = on_item_owner_changed_listener_manager


class OnItemQuantityChanged(ListenerManagerDecorator):
    manager = on_item_quantity_changed_listener_manager


class OnItemNameOrDescriptionChanged(ListenerManagerDecorator):
    manager = on_item_name_or_description_changed_listener_manager


class OnMisplacedItemDiscarded(ListenerManagerDecorator):
    manager = on_misplaced_item_discarded_listener_manager


class OnItemBoughtFromShop(ListenerManagerDecorator):
    manager = on_item_bought_from_shop_listener_manager


class OnItemUsed(ListenerManagerDecorator):
    manager = on_item_used_listener_manager
