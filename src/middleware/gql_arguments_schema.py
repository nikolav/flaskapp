
from functools import wraps

from graphql.error import GraphQLError
from marshmallow   import ValidationError


def gql_arguments_schema(schema):
  def decorated(fn):
    @wraps(fn)
    def wrapper(obj, info, **kwargs):
      print('@debug --gql_arguments_schema')
      data = kwargs
      
      try:
        data = schema.load(data)
      
      except ValidationError as e:
        raise GraphQLError(
          'Invalid arguments',
          extensions = {
            'code'   : 'BAD_USER_INPUT',
            'fields' : e.messages,
          })

      return fn(obj, info, **data)
    
    return wrapper
  
  return decorated
    
