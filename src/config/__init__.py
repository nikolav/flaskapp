import os
from dotenv import load_dotenv

load_dotenv()


class Config:
  FOO     = os.getenv('FOO')
  MESSAGE = os.getenv('MESSAGE')

