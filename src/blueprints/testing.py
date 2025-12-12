
from flask      import Blueprint
from flask_cors import CORS


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  from src.models.assets import Assets
  from src.models.assets import AssetsType
  from src.utils         import Utils
  from flask_app         import db
  from src.utils.unique  import Unique
  from src.schemas.serialization import SchemaSerializeAssets

  r = Utils.ResponseStatus()
  a = None

  try:
    _err, _dbcli = db
    a = Assets(name = f'A:{Unique.id()}', type = AssetsType.PHYSICAL_PRODUCT.value)
    _dbcli.session.add(a)
    _dbcli.session.commit()

  except Exception as e:
    r.error = e
  
  else:
    r.status = { 'asset': SchemaSerializeAssets(exclude = ('assets_has',)).dump(a) }
  
  return r.dump()
