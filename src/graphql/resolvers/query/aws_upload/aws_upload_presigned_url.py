
from datetime import timedelta

from flask import g

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

  upload_url  = None
  key         = None
  contentType = None

  try:
    _err, aws = aws_session
    
    s3 = aws.client('s3')
    
    # g.arguments: { filename, contentType, key? }
    filename    = g.arguments['filename']
    contentType = g.arguments['contentType']
    key         = g.arguments.get('key') or Utils.aws_key_random(filename)

    upload_url = s3.generate_presigned_url(
      ClientMethod = 'put_object',
      Params = {
        'Bucket'      : Config.AWS_UPLOAD_S3_BUCKET,
        'Key'         : key,
        'ContentType' : contentType,
      },
      ExpiresIn = int(timedelta(hours = 1).total_seconds()),
    )

  except Exception as e:
    r.error = e

  else:
    r.status = { 'uploadUrl': upload_url, 'key': key, 'contentType': contentType }

  
  return r.dump()

