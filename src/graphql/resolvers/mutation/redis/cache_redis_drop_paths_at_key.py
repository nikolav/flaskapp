
from src.graphql.setup          import mutation
from src.utils                  import Utils
from src.services.cache         import Cache
from src.config                 import Config
from src.services.io            import IO


# cacheRedisDropPathsAtKey(cache_key: String!, paths: [String!]!, separator: String): JsonData!
@mutation.field('cacheRedisDropPathsAtKey')
def resolve_cacheRedisDropPathsAtKey(_obj, _info, cache_key, paths, separator = None):
  r       = Utils.ResponseStatus()
  changes = 0

  try:
    changes += Cache.drop_paths_at_key(cache_key, *paths, SEPARATOR = separator)

  except Exception as e:
    r.error = e
  
  else:
    r.status = { 'keysDeletedCount': changes }
    if 0 < changes:
      IO.signal(f'{Config.IOEVENT_REDIS_CACHE_KEY_UPDATED_prefix}{cache_key}')
  
  return r.dump()


