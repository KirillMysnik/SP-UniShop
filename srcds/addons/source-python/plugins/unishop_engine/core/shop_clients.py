# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import json
from threading import Thread
from time import time

# Source.Python
from listeners import OnClientActive
from players.dictionary import PlayerDictionary
from players.entity import Player
from steam import SteamID

# UniShop
from unishop.listeners import on_misplaced_item_discarded

# UniShop Engine
from .config import config
from .global_item_manager import global_item_manager
from .items import Item
from .models import ShopClient as DB_ShopClient
from .orm import SessionContext


# =============================================================================
# >> CLASSES
# =============================================================================
class ShopClient(list):
    def __init__(self, index):
        super().__init__()

        self.player = Player(index)
        self.steamid64 = str(SteamID.parse(self.player.steamid).to_uint64())
        self._database_id = None

        self.credits = 0
        self._slots = 0
        self._misplaced_items = []

        self._loaded = False
        self._in_sync = True

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise IndexError("Only integer slots are supported")

        if not 0 <= index < self._slots:
            raise IndexError("Only slots 0-{} are available for this "
                             "player".format(self._slots-1))

        return super().__getitem__(index)

    def __setitem__(self, index, item):
        if not isinstance(index, int):
            raise IndexError("Only integer slots are supported")

        if not 0 <= index < self._slots:
            raise IndexError("Only slots 0..{} are available for this "
                             "player".format(self._slots-1))

        if item is None or isinstance(item, Item):
            super().__setitem__(index, item)
        else:
            raise ValueError("Unknown item: {}".format(item))

        self._in_sync = False

    def _handle_misplaced_items(self):
        max_misplaced_items = int(config['inventory']['max_misplaced_items'])

        if max_misplaced_items < 0:
            return

        for item in self._misplaced_items[max_misplaced_items:]:
            on_misplaced_item_discarded.notify(item)
            global_item_manager.delete_item(item)

        self._misplaced_items[max_misplaced_items:] = []

    @property
    def database_id(self):
        return self._database_id

    @property
    def loaded(self):
        return self._loaded

    def get_slots(self):
        return self._slots

    def set_slots(self, slots):
        if slots == self._slots:
            return

        if slots < self._slots:
            for i in range(slots, self._slots):
                item = self[i]
                if item is not None:
                    self._misplaced_items.insert(0, item)

                self.pop()

            self._handle_misplaced_items()

        else:
            for x in range(slots - self._slots):
                if self._misplaced_items:
                    item = self._misplaced_items.pop()
                else:
                    item = None

                self.append(item)

        self._slots = slots

        self._in_sync = False

    slots = property(get_slots, set_slots)

    @property
    def room(self):
        room = 0
        for item in self:
            if item is None:
                room += 1
        return room

    def give(self, item, index=-1, force=False):
        if not isinstance(item, Item):
            raise ValueError("Unknown item: {}".format(item))

        if index < 0:
            for index, item_ in enumerate(self):
                if item_ is None:
                    super().__setitem__(index, item)
                    break

            else:
                if force:
                    self._misplaced_items.insert(0, item)
                    self._handle_misplaced_items()
                else:
                    raise ValueError("No room to place another item")

        else:
            if self[index] is not None:
                if force:

                    # We misplace the original item no matter if there's
                    # room in the inventory
                    self._misplaced_items.insert(0, self[index])
                    self._handle_misplaced_items()

                else:
                    raise ValueError(
                        "There's already an item at index {}".format(index))

            super().__setitem__(index, item)

        self._in_sync = False

    def load_from_database(self):
        self._misplaced_items.clear()
        self.clear()

        with SessionContext() as session:
            db_shop_client = (session
                              .query(DB_ShopClient)
                              .filter_by(steamid64=self.steamid64)
                              .one_or_none())

            if db_shop_client is None:
                db_shop_client = DB_ShopClient.create(self.steamid64)
                db_shop_client.slots = int(config['inventory']['init_slots'])
                db_shop_client.credits = int(
                    config['inventory']['init_credits'])

                session.add(db_shop_client)
                session.commit()

                self._database_id = db_shop_client.id

            self._slots = db_shop_client.slots
            self.extend([None] * self._slots)

            for index, item_id in json.loads(db_shop_client.slot_data.items()):
                self[index] = global_item_manager[item_id]

            for item_id in db_shop_client.misplaced_items:
                self._misplaced_items.append(global_item_manager[item_id])

            self.credits = db_shop_client.credits

        self._loaded = True
        self._handle_misplaced_items()

    def save_to_database(self):
        if not self._loaded:
            return

        with SessionContext() as session:
            db_shop_client = session.query(DB_ShopClient).filter_by(
                steamid64=self.steamid64).one()

            db_shop_client.last_seen_at = time()

            slot_data = {}
            for index, item in enumerate(self):
                if item is None:
                    continue

                slot_data[index] = item.id

            misplaced_items = []
            for item in self._misplaced_items:
                misplaced_items.append(item.id)

            db_shop_client.slot_data = json.dumps(slot_data)
            db_shop_client.misplaced_items = json.dumps(misplaced_items)
            db_shop_client.slots = self._slots
            db_shop_client.credits = self.credits

        self._in_sync = True


class ShopClientDictionary(PlayerDictionary):
    def from_database_id(self, database_id):
        for shop_client in self.values():
            if shop_client.loaded and shop_client.database_id == database_id:
                return shop_client

        raise KeyError("No connected ShopClient with database "
                       "id = {} found".format(database_id))

    def on_automatically_removed(self, index):
        shop_client = shop_clients[index]

        for item in shop_client:
            if item is None:
                continue

            del global_item_manager[item.id]

        Thread(target=shop_client.save_to_database).start()

shop_clients = ShopClientDictionary(ShopClient)


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnClientActive
def listener_on_client_active(index):
    shop_client = shop_clients[index]
    Thread(target=shop_client.load_from_database).start()
