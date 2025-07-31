from flask_cors import CORS

from src.config import Config


def cors_setup(app):
  if Config.PRODUCTION:    
    CORS(app, 
      supports_credentials = True, 
      resources = {
        # r'/auth'                  : {'origins': '*'},
        r'/graphql'               : {'origins': '*'},
        # r'/storage'               : {'origins': '*'},
        # r'/webhook_viber_channel' : {'origins': '*'},
        # r'/b64url'                : {'origins': '*'},
      }
    )
  else:
    CORS(app, supports_credentials = True)
