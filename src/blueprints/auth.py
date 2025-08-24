

from flask      import g
from flask      import Blueprint
from flask_cors import CORS

from firebase_admin import auth

from src.middleware.arguments_schema import arguments_schema
from src.schemas.validation          import SchemaAuthArguments
from src.services.jwt                import JWT


bp_auth = Blueprint('auth', __name__, url_prefix = '/auth')

# cors blueprints for cross-domain
CORS(bp_auth)

@bp_auth.route('/authenticate', methods = ('POST',))
@arguments_schema(SchemaAuthArguments())
def resolve_route_authenticate():
  error = '@error:authenticate:access_token'
  token = None
  user  = None
  uid   = g.arguments['uid']

  try:
    user = auth.get_user(uid)
    if not user:
      raise Exception('access denied')
    
    token = JWT.encode({ 'uid': user.uid })

  except Exception as e:
    error = e

  else:
    if token:
      return { 'token': token }, 200
  
  return { 'error': str(error) }, 401


