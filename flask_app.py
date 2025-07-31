from flask import Flask

from src.config import Config


app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY


# graphql:setup @[`POST /graphql`]
from src.graphql.setup import graphql_mount_endpoint
graphql_mount_endpoint(app)

@app.route('/', methods=('GET',))
def hello():
    return f'!hello {Config.MESSAGE}!'


# cors:setup
from src.config.cors import cors_setup
cors_setup(app)


if __name__ == '__main__':
    app.run(debug=True)


