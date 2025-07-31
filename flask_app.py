from flask          import Flask
from flask_cors     import CORS
from flask_talisman import Talisman

from src.config import Config


app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['REDIS_URL']  = Config.REDIS_URL


# routes:setup
#  graphql @[`POST /graphql`]
from src.graphql.setup import graphql_mount_endpoint
graphql_mount_endpoint(app)

#  misc.
@app.route('/', methods=('GET',))
def hello():
    return f'!hello {Config.MESSAGE}!'


# cors:setup
CORS(app, 
    supports_credentials = True, 
    resources = {
        r'/graphql': {'origins': '*'},
    } if Config.PRODUCTION else '',
)


# talisman:setup
#  content security headers
Talisman(app, 
         force_https=False,
        )


# services
#  :redis
redis_client = None
if Config.REDIS_INIT:
  from src.config.redis import redis_init
  redis_client = redis_init(app)



if __name__ == '__main__':
    app.run(debug=True)


