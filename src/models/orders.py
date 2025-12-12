
from enum import Enum

from typing import Optional
from typing import List

from uuid import uuid4 as uuid

from sqlalchemy     import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.utils.mixins import MixinTimestamps
from src.utils.mixins import MixinIncludesTags
from src.utils.mixins import MixinByIds
from src.utils.mixins import MixinExistsID
from src.utils.mixins import MixinFieldMergeable
from src.utils.mixins import MixinManageTagsOnOrders
from src.utils.mixins import MixinReprSimple

from . import db
from . import assetsTable
from . import ordersTable
from . import ln_orders_tags
from . import ln_orders_items

from .tags import Tags


_err, _dbcli = db


class OrdersIOEvents(Enum):
  IOEVENT_ORDERS_CONFIGRED_prefix = 'IOEVENT_ORDERS_CONFIGRED:b6c6caf1-9be2-57a5-9ba0-6254e59d6909:'


class OrdersTags(Enum):
  TAG_ORDERS_SHAREABLE_GLOBALY = 'TAG_ORDERS_SHAREABLE_GLOBALY:61cde3f6-cdf8-5769-bf11-93b91f4ff49d'


class OrdersStatus(Enum):
  ACTIVE    = "ACTIVE:494fe821-1910-5bb5-8a82-af57697341f6"     # currently being processed
  CANCELED  = "CANCELED:78d0e3bf-f5d2-5971-8e36-5b03e0a57dce"   # canceled by user/system
  DONE      = "DONE:189d735b-88ce-57f9-93c9-ab24f50569bb"       # successfully completed
  FAILED    = "FAILED:919125b5-d0cf-5b3b-8045-47260fd4fbf9"     # processing failed
  ON_HOLD   = "ON_HOLD:d46faaa3-28a6-5cfb-95d1-b973288eb086"    # temporarily paused
  PENDING   = "PENDING:44f16d28-04f4-5aee-b68c-4a0c6240549f"    # order created, awaiting processing


class Orders(MixinTimestamps, MixinIncludesTags, MixinByIds, MixinExistsID, MixinFieldMergeable, MixinManageTagsOnOrders, MixinReprSimple, _dbcli.Model):
  __tablename__ = ordersTable

  # ID
  id: Mapped[int] = mapped_column(primary_key = True)

  # fields
  key    : Mapped[Optional[str]] = mapped_column(default = uuid)
  status : Mapped[Optional[str]]
  data   : Mapped[Optional[dict]] = mapped_column(JSON)
  notes  : Mapped[Optional[str]]
  
  # .sid related asset:site
  asset_id = mapped_column(_dbcli.ForeignKey(f'{assetsTable}.id'))

  # virtual
  # related asset:site
  tags  : Mapped[List['Tags']]   = relationship(secondary = ln_orders_tags,  back_populates = 'orders')
  asset : Mapped['Assets']       = relationship(back_populates = 'asset_orders')
  items : Mapped[List['Assets']] = relationship(secondary = ln_orders_items, back_populates = 'orders')

