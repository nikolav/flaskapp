
from flask      import Blueprint
# from flask      import request
from flask_cors import CORS

from flask import make_response
from flask import jsonify


bp_webhook = Blueprint('webhook', __name__, url_prefix = '/webhook')

# cors blueprints
CORS(bp_webhook)

@bp_webhook.route('/<string:key>', methods = ('POST',))
def route_handle_webhook(key = ''):
  # data = request.get_json()
  return make_response(jsonify(''), 200)
