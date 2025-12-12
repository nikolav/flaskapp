
from flask      import Blueprint
from flask_cors import CORS


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  from src.models.assets          import Assets
  from src.schemas.serialization import SchemaSerializeAssets
  from flask_app import db


  _err, _db = db
  
  a = _db.session.get(Assets, 4)

  _db.session.delete(a)
  _db.session.commit()

  return SchemaSerializeAssets(many = True).dump(Assets.lsa())

