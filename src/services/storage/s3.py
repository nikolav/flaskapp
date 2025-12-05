
from flask_app  import aws_session
from src.utils  import Utils
from src.config import Config

from . import StorageBackend


_err, _session = aws_session if aws_session else (None, None)

class StorageS3(StorageBackend):
  def __init__(self, bucket_name, *, BASE_PATH = '', REGION = Config.AWS_REGION_NAME):
    self.s3        = _session.client('s3', region_name = REGION) if _session else None
    self.bucket    = bucket_name
    self.base_path = BASE_PATH.strip('/')

  def _full_path(self, path):
    return f'{self.base_path}/{path.lstrip('/')}' if self.base_path else path.lstrip('/')

  def save(self, file_obj, path, content_type = None):
    r        = Utils.ResponseStatus()
    response = None
    
    key = self._full_path(path)

    try:
      response = self.s3.upload_fileobj(
        Fileobj   = file_obj,
        Bucket    = self.bucket,
        Key       = key,
        ExtraArgs = {} if not content_type else { 'ContentType': content_type },
      )
      
    except Exception as e:
      r.error = e

    else:
      r.status = {
        'reponse': response,
        'url'    : self.url(key),
      }
    
    return r


  def url(self, path):
    return f'https://{self.bucket}.s3.amazonaws.com/{path.lstrip('/')}'
