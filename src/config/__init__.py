import os
from dotenv import load_dotenv

load_dotenv()


ENV_ = os.getenv('ENV')

class Config:

  ENV         = ENV_
  DEVELOPMENT = 'development' == ENV_
  PRODUCTION  = 'production'  == ENV_
  PORT        = os.getenv('PORT')
  
  SECRET_KEY = os.getenv('SECRET_KEY')
  
  MESSAGE = os.getenv('MESSAGE')

  
  REDIS_INIT = bool(os.getenv('REDIS_INIT'))
  REDIS_URL  = os.getenv('REDIS_URL')

  # paths
  FLASK_TEMPLATES_FOLDER = os.getenv('FLASK_TEMPLATES_FOLDER')

  # io:cors
  IO_CORS_ALLOW_ORIGINS = (
    '*',
  )


