
from flask import g

from src.graphql.setup import mutation
from flask_app         import aws_session
from src.config        import Config
from src.utils         import Utils

from src.middleware.gql_arguments_schema import gql_arguments_schema
from src.schemas.validation import SchemaS3ValidatePrefixInput


# awsUploadDeleteObjectsAllUnderPrefix(prefix: String): JsonData!
@mutation.field('awsUploadDeleteObjectsAllUnderPrefix')
@gql_arguments_schema(SchemaS3ValidatePrefixInput())
def resolve_awsUploadDeleteObjectsAllUnderPrefix(_obj, _info, prefix = None):
  r = Utils.ResponseStatus()

  deletedCount = 0
  
  try:
    _err, aws = aws_session
    s3 = aws.client('s3')

    prefix_ = g.arguments['prefix']

    paginator = s3.get_paginator('list_objects_v2')
    delete_batch = {'Objects': []}

    for page in paginator.paginate(Bucket = Config.AWS_UPLOAD_S3_BUCKET, Prefix = prefix_):
      for node in page.get('Contents', []):
        key = node['Key']
        # skip root 'uploads' folder
        if Config.AWS_UPLOAD_S3_PREFIX != key:
          # add keys to delete to `delete_batch:Objects`
          delete_batch['Objects'].append({'Key': key})
          # 1000 objects max per s3 delete call
          if Config.AWS_UPLOAD_S3_MAX_PER_BATCH_DELETE == len(delete_batch['Objects']):
            res = s3.delete_objects(Bucket = Config.AWS_UPLOAD_S3_BUCKET, Delete = delete_batch)
            deletedCount += len(res['Deleted'])
            delete_batch = {'Objects': []}

    # delete rest
    if delete_batch['Objects']:
      res = s3.delete_objects(Bucket = Config.AWS_UPLOAD_S3_BUCKET, Delete = delete_batch)
      deletedCount += len(res['Deleted'])

  except Exception as e:
    r.error = e
  
  else:
    r.status = { 'deletedCount': deletedCount }
  
  
  return r.dump()

