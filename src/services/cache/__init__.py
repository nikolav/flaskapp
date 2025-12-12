
import json

from flask_app        import redis_client
from src.config       import Config
from src.utils        import Utils
from src.utils.discts import Dicts


class Cache:
  _err, client = redis_client if redis_client else (None, None)

  @staticmethod
  def key(token, *, DEFAULT_FACTORY = dict):
    raw  = None
    data = None

    if not Cache.client:
      return DEFAULT_FACTORY()
    
    raw = Cache.client.get(token)
    if not raw:
      return DEFAULT_FACTORY()
    
    if isinstance(raw, (bytes, bytearray)):
      raw = raw.decode('utf-8', errors = 'replace')
    
    try:
      data = json.loads(raw)
    except Exception:
      return DEFAULT_FACTORY()

    return data if isinstance(data, dict) else DEFAULT_FACTORY()
  
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
    if not Cache.client or not PATCH:
      raise Exception('@Cache:invalid')

    if MERGE:
      cache = Cache.key(token)
      Dicts.merge(cache, PATCH)
    else:
      cache = PATCH

    payload = json.dumps(cache, ensure_ascii = False)

    Cache.client.set(token, payload)

    return True
