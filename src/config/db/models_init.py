
from src.config import Config


print('@debug sqldb --models-init')

def models_init(db):
    _err, _db = db

    from src.models.docs   import Docs
    from src.models.tags   import Tags
    from src.models.assets import Assets
    from src.models.orders import Orders
    from src.models.nodes  import Nodes

    # drop/create schema
    if Config.REBUILD_SCHEMA:
      _db.drop_all()
    
    # create schema
    _db.create_all()


