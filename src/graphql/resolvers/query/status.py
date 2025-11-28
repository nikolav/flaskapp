
from sqlalchemy import text

from src.graphql.setup import query
from src.utils         import Utils


@query.field('status')
def resolve_status(_o, _i):
  redis_version = None
  mongo_version = None
  db_version    = None

  r = Utils.ResponseStatus()

  try:
    from flask_app import redis_client
    from flask_app import mongo
    from flask_app import db

    if mongo:
      _err_mongo, client_mongo = mongo
      mongo_version = client_mongo.cx.server_info()['version'] if client_mongo else ''

    if redis_client:
      _err_redis, client_redis = redis_client
      redis_version = client_redis.info().get('redis_version') if client_redis else ''
        
    if db:
      _err_db, client_db = db
      db_version = client_db.session.execute(
            text("SELECT version();")
          ).scalar() if client_db else ''

  except Exception as e:
    r.error = e

  else:
    r.status = {
      'status' : 'ok',
      'redis'  : redis_version,
      'mongo'  : mongo_version,
      'db'     : db_version,
    }

  return r.dump()
