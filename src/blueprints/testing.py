
from flask      import Blueprint
from flask_cors import CORS


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  from src.utils         import Utils
  from src.models.assets import Assets
  from src.models.assets import AssetsType
  from flask_app import db
  from src.schemas.serialization import SchemaSerializeAssets

  r = Utils.ResponseStatus()
  a = None

  try:
    _err, _db = db
    a = Assets(name = Assets.codegen(), type = AssetsType.PHYSICAL_PRODUCT.value)
    _db.session.add(a)
    _db.session.commit()
    
  except Exception as e:
    r.error = e
  
  else:
    r.status = { 'asset': SchemaSerializeAssets().dump(a) }
  
  return r.dump()
