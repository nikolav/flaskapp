
from flask      import Blueprint
from flask_cors import CORS


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  from src.services.messaging import CloudMessaging

  res = CloudMessaging.send(
      PAYLOAD = { 'title': 'title:foo2', 'body': 'message:foo2' },
      SILENT  = True,
    )
  
  return { 'res': CloudMessaging.response_send_successful(res) }

