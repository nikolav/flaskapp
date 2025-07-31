import os
from dotenv import load_dotenv

load_dotenv()


ENV_ = os.getenv('ENV')

class Config:

  ENV         = ENV_
  DEVELOPMENT = 'development' == ENV_
  PRODUCTION  = 'production'  == ENV_
  
  SECRET_KEY = os.getenv('SECRET_KEY')
  
  MESSAGE    = os.getenv('MESSAGE')

