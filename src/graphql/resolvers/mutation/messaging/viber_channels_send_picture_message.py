
import requests

from flask import g

from src.graphql.setup   import mutation
from src.utils           import Utils
from src.config          import Config
from src.services.cache  import Cache


# viberSendPictureMessage(payload: JsonData!): JsonData!
@mutation.field('viberSendPictureMessage')
def resolve_viberSendPictureMessage(_obj, _info, payload):
  # PicData: {  
  #  "media"!:"https://www.images.com/img.jpg!", 
  #  "text":"Picture description", 
  #  "thumbnail":"https://www.images.com/thumb.jpg" 
  # } 
  # payload: { [chName1]: <PicData>, [chName2]: <PicData> }
  r = Utils.ResponseStatus()
  
  result   = []
  channels = {}

  try:
    
    # load viber channels
    channels = Cache.auth_profile(g.user.uid).get(Config.VIBER_CHANNELS_CACHE_KEY, {})
    
    result = [requests.post(Config.VIBER_CHANNELS_POST_MESSAGE_URL,
                json = {
                  'auth_token': channels[channel_name]['auth_token'],
                  'from'      : channels[channel_name]['from'],
                  'type'      : 'picture',
                  'media'     : pic_data['media'],
                  'text'      : pic_data.get('text', ''),
                  'thumbnail' : pic_data.get('thumbnail'),
                }).json() 
                  for channel_name, pic_data in payload.items()
                    if channel_name in channels]

  except Exception as err:
    r.error = err

  else:
    r.status = result
    

  return r.dump()

