

import Adyen
from src.config import Config

initialized = False
error       = None
service     = None


def adyen_service():
  global initialized
  global error
  global service

  try:
    if not initialized:
      service = Adyen.Adyen()
      service.client.platform = Config.ADYEN_ENV
      service.client.xapikey  = Config.ADYEN_API_KEY
      
      initialized = True
    
  except Exception as e:
    error = e
  
  return error, service


