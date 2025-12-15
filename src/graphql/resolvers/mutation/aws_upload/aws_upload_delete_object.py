
from flask import g

from src.graphql.setup import mutation
from flask_app         import aws_session
from src.config        import Config
from src.utils         import Utils
from src.utils.dicts   import Dicts

from src.middleware.gql_arguments_schema import gql_arguments_schema
from src.schemas.validation import SchemaS3ValidateDeleteObjectInput


# awsUploadDeleteObject(key: String!): JsonData!
@mutation.field('awsUploadDeleteObject')
@gql_arguments_schema(SchemaS3ValidateDeleteObjectInput())
def resolve_awsUploadDeleteObject(_obj, _info, key):
  r     = Utils.ResponseStatus()
  res   = None
  code_ = None

  try:
    _err, aws = aws_session
    s3 = aws.client('s3')

    key_ = g.arguments['key']

    res = s3.delete_object(
        Bucket = Config.AWS_UPLOAD_S3_BUCKET, 
        Key    = key_,
      )
    
    # res.check@ResponseMetadata/HTTPStatusCode
    code_   = Dicts.get(res, 'ResponseMetadata/HTTPStatusCode')
    status_ = Utils.httpStatuses.get(code_, None)
    
  except Exception as e:
    r.error = e
  
  else:
    r.status = {'code': code_, 'status': status_, 'key': key_ }

  
  return r.dump()

