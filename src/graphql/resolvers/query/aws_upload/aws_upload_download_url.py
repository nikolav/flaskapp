
from datetime import timedelta

from flask import g
from botocore.config import Config as BotoConfig

from src.graphql.setup import query
from flask_app         import aws_session
from src.config        import Config
from src.utils         import Utils

from src.middleware.gql_arguments_schema import gql_arguments_schema
from src.schemas.validation import SchemaS3ValidateDownloadUrl


# awsUploadDownloadUrl(key: String!, forceDownload: Boolean): JsonData!
@query.field('awsUploadDownloadUrl')
@gql_arguments_schema(SchemaS3ValidateDownloadUrl())
def resolve_awsUploadDownloadUrl(_obj, _info, key, forceDownload = False):
  r = Utils.ResponseStatus()

  download_url = None
  
  try:
    _err, aws = aws_session
    s3 = aws.client('s3', 
                  config      = BotoConfig(signature_version = 's3v4'),
                  region_name = Config.AWS_UPLOAD_S3_BUCKET_REGION,
                )

    key_           = g.arguments['key']
    forceDownload_ = g.arguments['forceDownload']
    
    download_url = s3.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = { 
                'Bucket': Config.AWS_UPLOAD_S3_BUCKET, 
                'Key'   : key_,
                # 'ResponseContentDisposition': 'inline',
                'ResponseContentDisposition': 'attachment' if forceDownload_ else '',
              },
        ExpiresIn = int(timedelta(days = 1).total_seconds()),
      )
  
  except Exception as e:
    r.error = e
  
  else:
    r.status = { 'downloadUrl': download_url }
  
  
  return r.dump()

