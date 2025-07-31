from flask          import Flask
from flask_cors     import CORS
from flask_talisman import Talisman


from src.config import Config


app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY


# graphql:setup @[`POST /graphql`]
from src.graphql.setup import graphql_mount_endpoint
graphql_mount_endpoint(app)

# routes:misc.
@app.route('/', methods=('GET',))
def hello():
    return f'!hello {Config.MESSAGE}!'


# cors:setup
if Config.PRODUCTION:    
    CORS(app, 
        supports_credentials = True, 
        resources = {
            r'/graphql': {'origins': '*'},
        }
    )
else:
    CORS(app, supports_credentials = True)


# security headers setup
Talisman(app, 
         force_https=False,
        )


if __name__ == '__main__':
    app.run(debug=True)


