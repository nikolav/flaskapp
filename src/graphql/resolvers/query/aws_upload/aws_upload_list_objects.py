
from flask import g

from src.graphql.setup import query
from flask_app         import aws_session
from src.config        import Config
from src.utils         import Utils

from src.middleware.gql_arguments_schema import gql_arguments_schema
from src.schemas.validation import SchemaS3ListObjects


# awsUploadListObjects(prefix: String): JsonData!
@query.field('awsUploadListObjects')
@gql_arguments_schema(SchemaS3ListObjects())
def resolve_awsUploadListObjects(_obj, _info, prefix = None):
  r = Utils.ResponseStatus()

  prefix_     = None
  isTruncated = None
  objects     = []

  try:
    _err, aws = aws_session
    s3 = aws.client('s3')

    prefix_ = g.arguments['prefix']

    res = s3.list_objects_v2(
        Bucket  = Config.AWS_UPLOAD_S3_BUCKET, 
        Prefix  = prefix_, 
        MaxKeys = 122,
      )

    isTruncated = res.get('IsTruncated', False)

    objects = [
      {
        'key'          : node['Key'],
        'size'         : node.get('Size'),
        'lastModified' : node.get('LastModified').isoformat() if node.get('LastModified') else None,
        'etag'         : node.get('ETag'),
      } for node in res.get('Contents', [])]
      
  except Exception as e:
    r.error = e

  else:
    r.status = { 'objects': objects, 'isTruncated': isTruncated }
  
  
  return r.dump()

