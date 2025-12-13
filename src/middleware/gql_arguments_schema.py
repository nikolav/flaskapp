
from functools import wraps

from flask         import g
from graphql.error import GraphQLError
from marshmallow   import ValidationError


def gql_arguments_schema(schema):
  def decorated(fn):
    @wraps(fn)
    def wrapper(obj, info, **kwargs):
      print('@debug --gql_arguments_schema')
      data = {}
      
      try:
        data = schema.load(kwargs)
      
      except ValidationError as e:
        raise GraphQLError(
          'Invalid arguments',
          extensions = {
            'code'   : 'BAD_USER_INPUT',
            'fields' : e.messages,
          })

      g.arguments = data
      return fn(obj, info, **kwargs)
    
    return wrapper
  
  return decorated
    
