# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import json

# UniShop
from unishop.listeners import (
    on_item_owner_changed_listener_manager,
    on_item_quantity_changed_listener_manager,
    on_item_used_listener_manager)
from unishop.plugins import unishop_plugins

# UniShop Engine
from .models import Item as DB_Item
from .orm import SessionContext
from .shop_clients import shop_clients
from .strings import common_strings


# =============================================================================
# >> CLASSES
# =============================================================================
class Item(dict):
    def __init__(self, id_=None, plugin_name=None, class_id=None,
                 subclass_id=None):

        super().__init__()

        self.id = id_

        self._plugin_name = plugin_name
        self._class_id = class_id
        self._subclass_id = subclass_id

        self._owner_id = -1
        self._name_str = ""
        self._description_str = ""
        self._quantity = 1

        self._loaded = False
        self._in_sync = True

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._in_sync = False

    def __delitem__(self, key):
        super().__delitem__(key)
        self._in_sync = False

    @property
    def loaded(self):
        return self._loaded

    @property
    def in_sync(self):
        return self._in_sync

    @property
    def plugin(self):
        return unishop_plugins.get(self._plugin_name)

    @property
    def item_class(self):
        plugin = self.plugin
        if plugin is None:
            return None

        return plugin.get_item_class(self._class_id)

    @property
    def subclass(self):
        return self._subclass_id

    def get_owner(self):
        if self._owner_id < 0:
            return None

        return shop_clients.from_database_id(self._owner_id)

    def set_owner(self, owner):
        if self._owner_id == owner.database_id:
            return

        old_owner_id = self._owner_id
        self._owner_id = owner.database_id
        self._in_sync = False

        on_item_owner_changed_listener_manager.notify(self, old_owner_id)

    owner = property(get_owner, set_owner)

    @property
    def name(self):
        item_class = self.item_class
        if item_class is None:
            return common_strings['item_name unknown_item']

        return item_class.lang_strings[self._name_str]

    @property
    def description(self):
        item_class = self.item_class
        if item_class is None:
            return common_strings['item_desc unknown_item']

        return item_class.lang_strings[self._description_str]

    @property
    def icon(self):
        item_class = self.item_class
        if item_class is None:
            return "unishop/img/unknown_item.png"

        return item_class.get_item_icon(self)

    def get_quantity(self):
        return self._quantity

    def set_quantity(self, quantity):
        if quantity == self._quantity:
            return

        old_quantity = self._quantity
        self._quantity = quantity
        self._in_sync = False

        on_item_quantity_changed_listener_manager.notify(self, old_quantity)

    quantity = property(get_quantity, set_quantity)

    def set_name_and_description_keys(
            self, name_str=None, description_str=None):

        if name_str is None and description_str is None:
            return

        if name_str is not None:
            self._name_str = name_str

        if description_str is not None:
            self._description_str = description_str

        self._in_sync = False

    def use(self):
        item_class = self.item_class
        if item_class is None:
            raise RuntimeError(
                "Can't use this item because its class '{}' (plugin '{}') is "
                "unavailable".format(self._class_id, self._plugin_name))

        if not item_class.can_item_be_used(self):
            return False

        item_class.on_item_used(self)
        on_item_used_listener_manager.notify(self)
        return True

    def load_from_database(self):
        self.clear()

        with SessionContext() as session:
            if self.id is None:
                db_item = DB_Item.create(
                    self.plugin_name, self.class_id, self.subclass_id)

                session.add(db_item)
                session.commit()

                self.id = db_item.id

            else:
                db_item = session.query(DB_Item).filter_by(id=self.id).one()

            self._owner_id = db_item.owner_id
            self._name_str = db_item.name_str
            self._description_str = db_item.description_str
            self._quantity = db_item.quantity
            self.update(json.loads(db_item.item_data))

        self._loaded = True

    def save_to_database(self):
        if not self._loaded:
            return

        with SessionContext() as session:
            db_item = session.query(DB_Item).filter_by(id=self.id).one()
            db_item.owner_id = self._owner_id
            db_item.name_str = self._name_str
            db_item.description_str = self._description_str
            db_item.quantity = self._quantity
            db_item.item_data = json.dumps(self)

            session.commit()

        self._in_sync = True

    def delete_from_database(self):
        if self.id is None:
            return

        with SessionContext() as session:
            session.query(DB_Item).filter_by(id=self.id).delete()
            self.id = None

        self._loaded = False
        self._in_sync = True
