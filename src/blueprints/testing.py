
from flask      import Blueprint
from flask_cors import CORS


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  from src.services.cache import Cache
  # from src.utils import Utils
  from flask import request

  d = request.get_json()

  Cache.commit('foo:1', PATCH = d)

  return Cache.key('foo:1')