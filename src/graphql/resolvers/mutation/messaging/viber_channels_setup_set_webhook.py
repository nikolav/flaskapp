

import requests

from src.graphql.setup  import mutation
from src.utils          import Utils
from src.utils.dates    import utcnow
from src.config         import Config
from src.services.cache import Cache

from flask import g
# from flask_app import db


# viberChannelSetupSetWebhook(url: String!, auth_token: String!, is_global: Boolean): JsonData!
@mutation.field('viberChannelSetupSetWebhook')
def resolve_viberChannelSetupSetWebhook(_obj, _info, url, auth_token, is_global = False):
  r = Utils.ResponseStatus()
  
  ch_name = None
  ch_info = None

  try:
    
    # validate url
    # https://developers.viber.com/docs/tools/channels-post-api/#post-parameters
    dw = requests.post(Config.VIBER_CHANNELS_SET_WEBHOOK_URL, 
                    json = {
                      'url'        : url,
                      'auth_token' : auth_token,
                    }).json()
    
    if 0 != dw.get('status'):
      raise Exception('viber:setup:error --VIBER_CHANNELS_SET_WEBHOOK_URL')
    
    # access viber account
    di = requests.post(Config.VIBER_CHANNELS_ACCOUNT_INFO_URL,
                      json = {
                        'auth_token': auth_token,
                      }).json()
    
    if 0 != di.get('status'):
      raise Exception('viber:setup:error --VIBER_CHANNELS_ACCOUNT_INFO_URL')
    
    # cache channel admin account info for sending messages
    members = di.get('members', [])
    ch_admin = next((m for m in members if 'superadmin' == m.get('role')), None)

    if not ch_admin:
      raise Exception('viber:setup:error --NO-CHANNEL-ADMIN')
    
    ch_name = di['name']
    ch_info = { 
                '@'          : utcnow().isoformat(),
                'auth_token' : auth_token, 
                'from'       : ch_admin['id'], 
                'is_global'  : is_global,
              }

    Cache.auth_profile_patch(g.user.uid, 
                            patch = { Config.VIBER_CHANNELS_CACHE_KEY: { ch_name: ch_info } })

  except Exception as e:
    r.error = e
  
  else:    
    r.status = { 'channel': { ch_name: ch_info } }


  return r.dump()
  
