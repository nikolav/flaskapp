
from flask import g

from src.graphql.setup import query
from flask_app         import aws_session
from src.config        import Config
from src.utils         import Utils

from src.middleware.gql_arguments_schema import gql_arguments_schema
from src.schemas.validation import SchemaS3ValidateObjectMetadataInput
from src.schemas.serialization import SchemaS3ObjectMetadata


# awsUploadObjectMetadata(key: String!): JsonData!
@query.field('awsUploadObjectMetadata')
@gql_arguments_schema(SchemaS3ValidateObjectMetadataInput())
def resolve_awsUploadObjectMetadata(_obj, _info, key):
  r = Utils.ResponseStatus()

  key_     = None
  metadata = {}

  try:
    _err, aws = aws_session
    s3 = aws.client('s3')
    
    key_ = g.arguments['key']

    res = s3.head_object(
        Bucket = Config.AWS_UPLOAD_S3_BUCKET, 
        Key    = key_,
      )
    
    # { LastModified ContentLength ETag ContentType Metadata? }
    metadata = SchemaS3ObjectMetadata().dump(res)
  
  except Exception as e:
    r.error = e
  
  else:
    r.status = { 'key': key_, 'metadata': metadata }

  
  return r.dump()

