
from flask      import Blueprint
from flask_cors import CORS


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  from src.utils         import Utils
  from src.models.tags   import Tags

  r = Utils.ResponseStatus()
  a = None

  try:
    r.status = Tags.exits('foo:1')

  except Exception as e:
    r.error = e
  
  return r.dump()
