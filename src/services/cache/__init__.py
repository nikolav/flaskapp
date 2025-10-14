
import json

from flask_app        import redis_client
from src.config       import Config
from src.utils.discts import Dicts


class Cache:
  _err, client = redis_client

  @staticmethod
  def key(token):
    return {} if not Cache.client.exists(token) else json.loads(Cache.client.get(token).decode())
  
  @staticmethod
  def auth_profile(uid):
    return Cache.key(f'{Config.AUTH_PROFILE}{uid}')
  
  @staticmethod
  def auth_profile_patch(uid, *, patch, merge = True):
    if patch and uid:
      token = f'{Config.AUTH_PROFILE}{uid}'
      Cache.commit(token, patch = patch, merge = merge)
  
  @staticmethod
  def cloud_messaging_tokens(uid):
    return Cache.auth_profile(uid).get(Config.CLOUD_MESSAGING_TOKENS)
  
  @staticmethod
  def commit(token, *, patch = None, merge = True):
    if patch:
      if False != merge:
        cache = Cache.key(token)
        Dicts.merge(cache, patch)

      else:
        cache = patch

      Cache.client.set(token, json.dumps(cache))
