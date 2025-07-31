from src.graphql.setup import query


@query.field('status')
def resolve_status(_o, _i):
  redis_client_version = None

  try:
    from flask_app import redis_client
    _err, client = redis_client
    redis_client_version = client.info().get('redis_version')
  except:
    pass

  return {
    'status' : 'ok',
    'redis'  : redis_client_version,
  }

