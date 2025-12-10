
from flask      import Blueprint
from flask_cors import CORS


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  from src.services.cache import Cache
  from src.utils          import Utils

  r     = Utils.ResponseStatus()
  token = 'foo:1'

  try:
    r.status = { token: Cache.key(token) }

  except Exception as e:
    r.error = e

  return r.dump()
