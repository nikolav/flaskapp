
from flask_app  import db
from src.config import Config


_err, _dbcli = db

tblSuffix_dev        = Config.TABLE_NAME_SUFFIX_dev
tblSuffix_production = Config.TABLE_NAME_SUFFIX_production

tblSuffix = tblSuffix_production if Config.PRODUCTION else tblSuffix_dev

tagsTable = f'tags{tblSuffix}'
docsTable = f'docs{tblSuffix}'

lnTableDocsTags = f'ln_docs_tags{tblSuffix}'


ln_docs_tags = _dbcli.Table(
  lnTableDocsTags,
  _dbcli.Column('doc_id', _dbcli.ForeignKey(f'{docsTable}.id'), primary_key = True),
  _dbcli.Column('tag_id', _dbcli.ForeignKey(f'{tagsTable}.id'), primary_key = True),
)
