
from flask      import Blueprint
from flask_cors import CORS


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  from src.models.docs import Docs
  from src.utils       import Utils

  r = Utils.ResponseStatus()

  try:
    d = Docs.by_key('foo:1')
    r.status = { 'doc': d.dump() }

  except Exception as e:
    r.error = e
  
  return r.dump()
