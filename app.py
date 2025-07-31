from flask import Flask
from src.config import Config

app = Flask(__name__)

@app.route("/")
def hello():
    return f'hello {Config.MESSAGE}'

if __name__ == "__main__":
    app.run(debug=True)
