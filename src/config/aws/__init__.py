
print('@aws_session:init')

initialized = False
error       = None
aws_session = None

def aws_session_init(app):
  global initialized
  global error
  global aws_session

  if not initialized:  
    import boto3
    from src.config import Config

    try:
      aws_session = boto3.Session(
        aws_access_key_id     = Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY,
        # region_name           = Config.AWS_REGION_NAME,
      )

    except Exception as err:
      error = err
    
    initialized = True
    
  
  return error, aws_session


