
from typing import List
from typing import Optional
from uuid   import uuid4 as uuid

from sqlalchemy     import Index
from sqlalchemy     import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.utils.mixins import MixinTimestamps
from src.utils.mixins import MixinByIds
from src.utils.mixins import MixinExistsID
from src.utils.mixins import MixinFieldMergeable
from src.utils.mixins import MixinIncludesTags
from src.utils.mixins import MixinReprSimple

from src.schemas.serialization import SchemaSerializeNodes

from . import nodesTable
from . import ln_nodes_tags

from flask_app import db


_err, _db = db

class Nodes(MixinTimestamps, MixinByIds, MixinExistsID, MixinFieldMergeable, MixinIncludesTags, MixinReprSimple, _db.Model):
  __tablename__ = nodesTable

  id   : Mapped[int]  = mapped_column(primary_key = True)
  key  : Mapped[str]  = mapped_column(default = lambda: str(uuid()))
  data : Mapped[dict] = mapped_column(JSON, default = dict)

  # foreign, self-referential
  parent_id = mapped_column(
      _db.ForeignKey(
          f'{nodesTable}.id', 
          # ondelete = 'SET NULL',
          ondelete = 'CASCADE',
        ), 
      index    = True, 
      nullable = True,
    )

  # virtual
  tags     : Mapped[List['Tags']]      = relationship(secondary = ln_nodes_tags, back_populates = 'nodes')
  parent   : Mapped[Optional['Nodes']] = relationship(remote_side = 'Nodes.id', back_populates = 'children')
  children : Mapped[List['Nodes']]     = relationship(cascade = 'all, delete-orphan', back_populates = 'parent',
    single_parent   = True,   # helps enforce delete-orphan rules
    passive_deletes = True,   # works well with ondelete behavior
  )

  
  def is_root(self):
    return self.parent_id is None
  
  
  def dump(self, *args, **kwargs):
    return SchemaSerializeNodes(*args, **kwargs).dump(self)

  
  @staticmethod
  def lsa():
    return _db.session.scalars(_db.select(Nodes))


# extra index
Index('ix_nodes_parent_id_id', Nodes.parent_id, Nodes.id)
