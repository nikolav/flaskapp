
from flask import g

from src.graphql.setup  import mutation
from src.utils          import Utils
from src.config         import Config
from src.services.cache import Cache


# viberChannelSetupChannelsDrop(channels: [String!]): JsonData!
@mutation.field('viberChannelSetupChannelsDrop')
def resolve_viberChannelSetupChannelsDrop(_obj, _info, channels = []):
  r = Utils.ResponseStatus()
  viber_channels = {}
  patch = {}

  try:
    if channels:
      viber_channels = Cache.auth_profile(g.user.uid).get(Config.VIBER_CHANNELS_CACHE_KEY, {})
      # if has channels to drop
      #   reset channels cache
      if any(ch in viber_channels for ch in channels):
        patch = { ch: viber_channels[ch] for ch in viber_channels if not ch in channels }
        Cache.auth_profile_patch(g.user.uid, 
            patch = { Config.VIBER_CHANNELS_CACHE_KEY: patch }, 
            merge = False,
          )

  except Exception as e:
    r.error = e

  else:
    r.status = [ch for ch in patch]


  return r.dump()


