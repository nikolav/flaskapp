import os
from dotenv import load_dotenv

load_dotenv()


class Config:
  MESSAGE    = os.getenv('MESSAGE')
  SECRET_KEY = os.getenv('SECRET_KEY')
