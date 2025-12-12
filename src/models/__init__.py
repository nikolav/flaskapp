
from flask_app  import db
from src.config import Config


_err, _db = db

tblSuffix_dev        = Config.TABLE_NAME_SUFFIX_dev
tblSuffix_production = Config.TABLE_NAME_SUFFIX_production

tblSuffix = tblSuffix_production if Config.PRODUCTION else tblSuffix_dev

# tables --names
tagsTable   = f'tags{tblSuffix}'
docsTable   = f'docs{tblSuffix}'
assetsTable = f'assets{tblSuffix}'
ordersTable = f'orders{tblSuffix}'
nodesTable  = f'nodes{tblSuffix}'

lnTableDocsTags       = f'ln_docs_tags{tblSuffix}'
lnTableAssetsTags     = f'ln_assets_tags{tblSuffix}'
lnTableOrdersTags     = f'ln_orders_tags{tblSuffix}'
lnTableOrdersItems    = f'ln_orders_items{tblSuffix}'
lnTableAssetsAssets   = f'ln_assets_assets{tblSuffix}'
lnTableNodesTags      = f'ln_nodes_tags{tblSuffix}'

# tables --ln
ln_docs_tags = _db.Table(
  lnTableDocsTags,
  _db.Column('doc_id', _db.ForeignKey(f'{docsTable}.id'), primary_key = True),
  _db.Column('tag_id', _db.ForeignKey(f'{tagsTable}.id'), primary_key = True),
)

ln_assets_tags = _db.Table(
  lnTableAssetsTags,
  _db.Column('asset_id', _db.ForeignKey(f'{assetsTable}.id'), primary_key = True),
  _db.Column('tag_id',   _db.ForeignKey(f'{tagsTable}.id'),   primary_key = True),
)

ln_orders_tags = _db.Table(
  lnTableOrdersTags,
  _db.Column('order_id', _db.ForeignKey(f'{ordersTable}.id'), primary_key = True),
  _db.Column('tag_id',   _db.ForeignKey(f'{tagsTable}.id'),   primary_key = True),
)

ln_orders_items = _db.Table(
  lnTableOrdersItems,
  _db.Column('order_id', _db.ForeignKey(f'{ordersTable}.id'), primary_key = True),
  _db.Column('item_id',  _db.ForeignKey(f'{assetsTable}.id'), primary_key = True),
  _db.Column('amount',   _db.Integer, nullable = False, default = 0),
)

ln_assets_assets = _db.Table(
  lnTableAssetsAssets,
  _db.Column('asset_l_id', _db.ForeignKey(f'{assetsTable}.id'),  primary_key = True),
  _db.Column('asset_r_id', _db.ForeignKey(f'{assetsTable}.id'),  primary_key = True),
)

ln_nodes_tags = _db.Table(
  lnTableNodesTags,
  _db.Column('node_id', _db.ForeignKey(f'{nodesTable}.id'), primary_key = True),
  _db.Column('tag_id',  _db.ForeignKey(f'{tagsTable}.id'),  primary_key = True),
)

