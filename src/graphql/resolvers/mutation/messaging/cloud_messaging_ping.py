
from marshmallow import EXCLUDE

from src.graphql.setup      import mutation
from src.services.messaging import CloudMessaging
from src.schemas.validation import SchemaValidateCloudMessagingMessage
from src.utils              import Utils


@mutation.field('cloudMessagingPing')
def resolve_cloudMessagingPing(_obj, _info, 
                               payload = {
                                 'title' : 'title --ping', 
                                 'body'  : 'body --ping',
                                }):
  r   = Utils.ResponseStatus()
  res = None

  try:
    res = CloudMessaging.send(
        PAYLOAD = SchemaValidateCloudMessagingMessage(unknown = EXCLUDE).load(payload),
        SILENT  = False,
      )

  except Exception as e:
    r.error = e
  
  else:
    r.status = str(res)

  return r.dump()

