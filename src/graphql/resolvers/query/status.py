
from src.graphql.setup import query


@query.field('status')
def resolve_status(_o, _i):
  redis_version = None
  mongo_version = None

  try:
    from flask_app import redis_client
    from flask_app import mongo

    if redis_client:
      _err_redis, client_redis = redis_client
      redis_version     = client_redis.info().get('redis_version') if client_redis else ''
    
    if mongo:
      _err_mongo, client_mongo = mongo
      mongo_version = client_mongo.cx.server_info()['version'] if client_mongo else ''
        
  except:
    pass

  return {
    'status' : 'ok',
    'redis'  : redis_version,
    'mongo'  : mongo_version,
  }


