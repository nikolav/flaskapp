
import json
from http import HTTPStatus
from uuid import uuid4 as uuid

from marshmallow import fields
from marshmallow import Schema

from src.config import Config


class _SchemaResponseStatus(Schema):
  error  = fields.Method('resolve_error')
  status = fields.Method('resolve_status')

  def resolve_error(self, node):
    err_ = getattr(node, 'error')
    return str(err_) if None != err_ else None

  def resolve_status(self, node):
    return getattr(node, 'status')


_schema       = _SchemaResponseStatus()
_httpStatuses = { val.value: val.name.lower() for val in HTTPStatus }

class Utils:  
  httpStatuses = _httpStatuses

  class ResponseStatus():
    def __init__(self):
      self.error  = None
      self.status = None
    
    def dump(self):
      return _schema.dump(self)
    
    def __repr__(self):
      return json.dumps(self.dump())
  

  @staticmethod
  def file_extension(filename):
    if not filename or '.' not in filename:
        return ''
    ext = filename.rsplit('.', 1)[-1].lower()
    # keep it simple; optionally validate allowed extensions
    return f'.{ext}'
  
  
  @staticmethod
  def aws_key_random(filename):
    return f'{Config.AWS_UPLOAD_S3_PREFIX.rstrip('/')}/{uuid().hex}{Utils.file_extension(filename)}'


