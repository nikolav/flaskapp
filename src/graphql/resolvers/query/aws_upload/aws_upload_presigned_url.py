
from datetime import timedelta

from flask import g
from botocore.config import Config as BotoConfig

from src.graphql.setup import query
from flask_app         import aws_session
from src.config        import Config
from src.utils         import Utils

from src.schemas.validation import SchemaS3PresignedUploadInput
from src.middleware.gql_arguments_schema import gql_arguments_schema


# awsUploadPresignedUrl(filename: String!, contentType: String!, key: String): JsonData!
@query.field('awsUploadPresignedUrl')
@gql_arguments_schema(SchemaS3PresignedUploadInput())
def resolve_awsUploadPresignedUrl(_obj, _info, filename, contentType, key = None):
  r = Utils.ResponseStatus()

  UPLOAD_URL   = None
  CONTENT_TYPE = None
  KEY          = None

  try:
    _err, aws = aws_session
    
    # s3 = aws.client('s3') 
    s3 = aws.client('s3', 
                  config      = BotoConfig(signature_version = 's3v4'),
                  region_name = Config.AWS_UPLOAD_S3_BUCKET_REGION,
                )
    
    # g.arguments: { filename, contentType, key? }
    FILENAME     = g.arguments['filename']
    CONTENT_TYPE = g.arguments['contentType']
    KEY          = g.arguments.get('key') or Utils.aws_key_random(FILENAME)

    UPLOAD_URL = s3.generate_presigned_url(
      ClientMethod = 'put_object',
      Params = {
        'Bucket'      : Config.AWS_UPLOAD_S3_BUCKET,
        'Key'         : KEY,
        'ContentType' : CONTENT_TYPE,
      },
      ExpiresIn = int(timedelta(hours = 1).total_seconds()),
    )

  except Exception as e:
    r.error = e

  else:
    r.status = { 'uploadUrl': UPLOAD_URL, 'contentType': CONTENT_TYPE, 'key': KEY }

  
  return r.dump()

