

import requests

from flask import g

from src.graphql.setup   import mutation
from src.utils           import Utils
from src.config          import Config
from src.services.cache  import Cache


# viberSendTextMessage(payload: JsonData!): JsonData!
@mutation.field('viberSendTextMessage')
def resolve_viberSendTextMessage(_obj, _info, payload):
  # payload: { [chName1]: <text message>, [chName2]: <text message> }
  r = Utils.ResponseStatus()
  
  result   = []
  channels = {}

  try:
    
    # load viber channels
    channels = Cache.auth_profile(g.user.uid).get(Config.VIBER_CHANNELS_CACHE_KEY, {})
    
    result = [requests.post(Config.VIBER_CHANNELS_POST_MESSAGE_URL,
                json = {
                  'auth_token' : channels[channel_name]['auth_token'],
                  'from'       : channels[channel_name]['from'],
                  'type'       : 'text',
                  'text'       : text
                }).json() 
                  for channel_name, text in payload.items()
                    if channel_name in channels]

  except Exception as err:
    r.error = err

  else:
    r.status = result
    

  return r.dump()

