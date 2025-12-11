
from flask      import Blueprint
from flask_cors import CORS


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  from src.models.docs import Docs
  from src.utils       import Utils
  from src.schemas.serialization import SchemaSerializeDocs

  r = Utils.ResponseStatus()

  try:
    d = Docs.by_key('foo:1')
    r.status = { 'doc': SchemaSerializeDocs().dump(d) }

  except Exception as e:
    r.error = e
  
  return r.dump()
