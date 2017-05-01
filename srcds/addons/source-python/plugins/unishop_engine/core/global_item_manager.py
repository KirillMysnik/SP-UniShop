# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from threading import Thread

# UniShop
from unishop.listeners import (
    on_item_created_listener_manager,
    on_item_deleted_listener_manager,
    on_item_loaded_from_database_listener_manager,
    on_item_pre_deleted_listener_manager)

# UniShop Engine
from .items import Item


# =============================================================================
# >> CLASSES
# =============================================================================
class GlobalItemManager(dict):
    def __init__(self):
        super().__init__()

        self._item_creation_token = 0

    def __missing__(self, item_id):
        item = Item(item_id)

        def load_item_from_database():
            item.load_from_database()
            on_item_loaded_from_database_listener_manager.notify(item)

        Thread(target=load_item_from_database).start()
        super().__setitem__(item_id, item)
        return item

    def __setitem__(self, item_id, item):
        raise ValueError("Can't set items to GlobalItemManager instance")

    def __delitem__(self, item_id):
        if item_id not in self:
            return

        item = super().__getitem__(item_id)
        Thread(target=item.save_to_database).start()
        super().__delitem__(item_id)

    def delete_item(self, item):
        if item.id is None:
            raise ValueError(
                "Can't delete the item, its ID is set to None. "
                "You are trying to delete either already deleted "
                "item or yet-to-be-created item")

        item_id = item.id

        def delete_item_from_database():
            on_item_pre_deleted_listener_manager.notify(item)

            item_class = item.item_class
            item.delete_from_database()

            if item_id in self:
                super().__delitem__(item_id)

            if item_class is not None:
                item_class.on_item_deleted(item_id)

            on_item_deleted_listener_manager.notify(item_id)

        Thread(target=delete_item_from_database).start()

    def create_item(self, plugin_name, class_id, subclass_id):
        self._item_creation_token += 1

        item = Item(plugin_name=plugin_name, class_id=class_id,
                    subclass_id=subclass_id)

        def create_item():
            item.load_from_database()

            super().__setitem__(item.id, item)

            item_class = item.item_class
            if item_class is not None:
                item_class.on_item_created(item, self._item_creation_token)

            on_item_created_listener_manager.notify(
                item, self._item_creation_token)

            self._item_creation_token -= 1

        Thread(target=create_item).start()

        return self._item_creation_token

global_item_manager = GlobalItemManager()
