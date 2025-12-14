import re

from marshmallow import Schema
from marshmallow import fields
from marshmallow import pre_load
from marshmallow import validates
from marshmallow import ValidationError

from src.utils.re import RE_NO_PATH_SEPARATORS
from src.config   import Config


class SchemaAuthArguments(Schema):
  idToken = fields.String(required = True)


class SchemaValidateCloudMessagingMessage(Schema):
  title = fields.String(required = True)
  body  = fields.String(required = True)
  # data  = fields.Dict(allow_none = True)
  data = fields.Raw(allow_none = True, required = False)


class SchemaS3PresignedUploadInput(Schema):
  '''
    Input schema for presigned S3 uploads.

    Create:
      { filename, contentType }

    Update:
      { filename, contentType, key }
  '''

  filename    = fields.String(required = True)
  contentType = fields.String(required = True, data_key = 'contentType')
  key         = fields.String(required = False, allow_none = True)

  # Normalization
  
  @pre_load
  def content_type_normalized(self, data, **kwargs):
    '''
      Replace contentType using MIME_ALIASES so downstream
      code always sees canonical MIME values.
    '''
    ct = data.get('contentType')
    if ct:
      data['contentType'] = Config.UPLOADS_MIME_ALIASES.get(ct.lower(), ct.lower())
    return data

  # Validators

  @validates('filename')
  def validate_filename(self, value, **kwargs):
    if not value or not value.strip():
      raise ValidationError('Filename is required')

    if Config.UPLOADS_MAX_FILENAME_LENGTH < len(value):
      raise ValidationError('Filename too long')

    if not re.fullmatch(RE_NO_PATH_SEPARATORS, value):
      raise ValidationError('Filename must not contain path separators')

    # Optional: prevent hidden files like `.env`
    if value.startswith('.'):
      raise ValidationError('Hidden filenames are not allowed')

  @validates('contentType')
  def validate_content_type(self, value, **kwargs):
    if value not in Config.UPLOADS_ALLOW_CONTENT_TYPES:
      raise ValidationError(f'Unsupported contentType: {value}')

  @validates('key')
  def validate_key(self, value, **kwargs):
    if value is None:
      return

    if not value.startswith(Config.AWS_UPLOAD_S3_PREFIX):
      raise ValidationError('Invalid S3 key prefix')

    if '..' in value or value.startswith('/'):
      raise ValidationError('Invalid S3 key path')

