
from flask      import Blueprint
from flask_cors import CORS


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  from src.models.nodes          import Nodes
  from src.schemas.serialization import SchemaSerializeNodes
  
  return SchemaSerializeNodes(many = True, exclude = ('parent', 'children',)).dump(Nodes.lsa())

