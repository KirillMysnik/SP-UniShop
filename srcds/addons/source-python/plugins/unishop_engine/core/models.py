# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import json
from time import time

# Site-Package
from sqlalchemy import Boolean, Column, Integer, String, Text

# UniShop Engine
from .config import config
from .orm import Base


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
class ShopClient(Base):
    __tablename__ = config['database']['prefix'] + "shop_clients"

    id = Column(Integer, primary_key=True)
    steamid64 = Column(String(32))

    credits = Column(Integer)
    slots = Column(Integer)
    created_at = Column(Integer)
    last_seen_at = Column(Integer)
    slot_data = Column(Text)
    misplaced_items = Column(Text)

    @classmethod
    def create(cls, steamid64):
        shop_client = cls()
        shop_client.steamid64 = steamid64
        shop_client.credits = 0
        shop_client.slots = 0

        shop_client.created_at = time()

        shop_client.slot_data = json.dumps(dict())
        shop_client.misplaced_items = json.dumps(list())

        return shop_client


class Item(Base):
    __tablename__ = config['database']['prefix'] + "items"

    id = Column(Integer, primary_key=True)
    plugin_name = Column(String(64))
    class_id = Column(String(64))
    subclass_id = Column(String(64))

    owner_id = Column(Integer)
    name_str = Column(String(64))
    description_str = Column(String(64))
    quantity = Column(Integer)
    created_at = Column(Integer)
    expires_at = Column(Integer)
    item_data = Column(Text)

    @classmethod
    def create(cls, plugin_name, class_id, subclass_id):
        item = cls()
        item.plugin_name = plugin_name
        item.class_id = class_id
        item.subclass_id = subclass_id

        item.owner_id = -1

        item.quantity = 1
        item.created_at = time()
        item.expires_at = -1

        item.item_data = json.dumps(dict())

        return item
