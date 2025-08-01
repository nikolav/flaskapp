from flask          import Flask
from flask_cors     import CORS
from flask_talisman import Talisman
# https://github.com/miguelgrinberg/flask-socketio/issues/40#issuecomment-48268526
from flask_socketio import SocketIO

from src.config import Config


app = Flask(__name__,
            template_folder = Config.FLASK_TEMPLATES_FOLDER,
            )

app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['REDIS_URL']  = Config.REDIS_URL


# services:redis
redis_client = None
if Config.REDIS_INIT:
  from src.config.redis import redis_init
  redis_client = redis_init(app)

# services:cors
CORS(app, 
    supports_credentials = True, 
    resources = {
        r'/graphql': {'origins': '*'},
    } if Config.PRODUCTION else '',
)

# services:talisman
#  content security headers
Talisman(app, 
         force_https=False,
        )
        
# services:io
#  realtime support
from src.config.io import socketio_setup
io = socketio_setup(app)


# routes:graphql, @[`POST /graphql`]
from src.graphql.setup import graphql_mount_endpoint
graphql_mount_endpoint(app)

# routes:misc.

@app.route('/', methods=('GET',))
def hello():
    return f'!hello {Config.MESSAGE}!'



