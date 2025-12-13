
from functools import wraps

from flask import request
from flask import make_response
from flask import g

from marshmallow.exceptions import ValidationError


def arguments_schema(schema_validate):
  def decorated(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      error  = '@error:arguments_schema'
      status = 500
      data   = None

      try:
        # validate/load request data
        data = schema_validate.load(request.get_json())

      except ValidationError as err:
        # @400
        error  = err
        status = 400

      except Exception as err:
        # @500
        error = err
      
      else:
        # @200
        # set global `.arguments` to parsed input; run next
        g.arguments = data
        return fn(*args, **kwargs)
      
      # send error
      return make_response({ 'error': str(error) }, status)

    return wrapper

  return decorated
