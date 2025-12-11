from flask_sqlalchemy import SQLAlchemy

from src.utils.model_base import ModelBase
from src.config           import Config


print('@debug sqldb --init')

initialized = False
error       = None
cli         = None

def sqldb_init(app):
  global initialized
  global error
  global cli

  if not initialized:
    app.config['SQLALCHEMY_DATABASE_URI']        = Config.DATABASE_URI_production if Config.PRODUCTION else Config.DATABASE_URI_development
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_ECHO']                = not Config.PRODUCTION or Config.SQLALCHEMY_ECHO

    try:
      cli = SQLAlchemy(app, 
                      model_class = ModelBase,
                    )
    
    except Exception as e:
      error = e
    
  initialized = True

  return error, cli

