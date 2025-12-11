from flask_redis import FlaskRedis

from src.config  import Config


print('@debug redis --init')

initialized = False
error       = None
client      = None

def redis_init(app):
  global client
  global error
  global initialized

  if not initialized:  
    app.config['REDIS_URL'] = Config.REDIS_URL

    try:
      client = FlaskRedis()
      client.init_app(app)

      # access internal redis{} @redis-py
      #  client._redis_client


    except Exception as err:
      error = err
    
    
    initialized = True
    
  
  return error, client

