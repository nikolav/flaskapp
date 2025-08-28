
import bcrypt
import base64


class PWD:

  @staticmethod
  def hash(password):
    bPasswordHashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return base64.b64encode(bPasswordHashed).decode('utf-8')
  
  @staticmethod
  def verify(password, b64_hashed_password):
    bPassword       = password.encode('utf-8')
    bPasswordHashed = base64.b64decode(b64_hashed_password.encode('utf-8'))
    return bcrypt.checkpw(bPassword, bPasswordHashed)
  
