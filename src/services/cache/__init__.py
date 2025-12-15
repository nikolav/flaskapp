
import json

from flask_app        import redis_client
from src.config       import Config
from src.utils.dicts  import Dicts


class Cache:
  _err, client = redis_client if redis_client else (None, None)

  @staticmethod
  def key(token, *, DEFAULT_FACTORY = dict):
    rdata = None
    data  = None
    
    try:
      rdata = Cache.client.get(token)
      if isinstance(rdata, (bytes, bytearray)):
        rdata = rdata.decode('utf-8', errors = 'replace')
      
      data = json.loads(rdata)

      if not isinstance(data, dict):
        raise
    
    except:
      pass
    
    else:
      return data
    
    return DEFAULT_FACTORY()
  

  @staticmethod
  def auth_profile(uid):
    return Cache.key(f'{Config.AUTH_PROFILE}{uid}')
  
  
  @staticmethod
  def auth_profile_patch(uid, *, patch, merge = True):
    if patch and uid:
      token = f'{Config.AUTH_PROFILE}{uid}'
      return Cache.commit(token, PATCH = patch, MERGE = merge)
  
  
  @staticmethod
  def cloud_messaging_tokens(uid):
    return Cache.auth_profile(uid).get(Config.CLOUD_MESSAGING_TOKENS)
  
  
  @staticmethod
  def commit(token, *, PATCH = None, MERGE = True):
    if not Cache.client or PATCH is None:
      raise Exception('@Cache:invalid')

    if MERGE:
      cache = Cache.key(token)
      Dicts.merge(cache, PATCH)
    else:
      cache = PATCH

    payload = json.dumps(cache, ensure_ascii = False)

    Cache.client.set(token, payload)

    return True


  @staticmethod
  def ls(*, MATCH = '*', COUNT = 1000):
    # keys are bytes if FlaskRedis was initialized without 'decode_responses=True'
    return map(lambda key: key.decode('utf-8'), Cache.client.scan_iter(match = MATCH, count = COUNT))


  @staticmethod
  def drop_paths_at_key(token, *paths):
    # paths <string:dotted>[]
    changes = 0
    
    if paths:
      dd = Cache.key(token)
      if dd:
        for path in paths:
          changes += Dicts.rm(dd, path, SEPARATOR = '.')
        
        if 0 < changes:
          Cache.commit(token, PATCH = dd, MERGE = False)
    
    return changes


