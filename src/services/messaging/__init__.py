
from firebase_admin import messaging
from flask          import g

from src.services.cache import Cache


class CloudMessaging:
  
  @staticmethod
  def user_tokens():
    # this user tokens
    return [tok for tok, val in Cache.cloud_messaging_tokens(g.user.uid).items() if True == val]
  
  
  @staticmethod
  def notifications_send(*, payload, tokens = None, image = None):
    if tokens is None:
      # load this user tokens
      tokens = CloudMessaging.user_tokens()
    return messaging.send_each(
      [messaging.Message(
          notification = messaging.Notification(
            title = payload['title'],
            body  = payload['body'],
            image = image,
          ),
          data  = payload.get('data'),
          token = token,
        ) for token in tokens])


  @staticmethod
  def messages_send(*, payload, tokens = None):
    if tokens is None:
      # load this user tokens
      tokens = CloudMessaging.user_tokens()
    return messaging.send_each(
      [messaging.Message(
                  data  = payload,
                  token = token, 
                ) for token in tokens])
  

  @staticmethod
  def send(*, PAYLOAD, TOKENS = None, IMAGE = None, SILENT = False):
    if SILENT:
      return CloudMessaging.messages_send(payload = PAYLOAD, tokens = TOKENS)
    else:
      return CloudMessaging.notifications_send(payload = PAYLOAD, tokens = TOKENS, image = IMAGE)
  
  
  @staticmethod
  def topics_subscribe(subscriptions):
    # subscriptions: { [topic: string]: Token[] | None }
    pass

  
  @staticmethod
  def topics_unsubscribe(unsubscriptions):
    # unsubscriptions: { [topic: string]: Token[] | None }
    pass

  
  @staticmethod
  def topics_publish(payloads, *, SILENT = False):
    # payloads : { [topic: string]: payload:dict }; 
    # SILENT?  : bool
    pass


  @staticmethod
  def response_send_successful(resp):
    '''
    Returns True if at least one SendResponse succeeded.
    Safe even if counters are missing or inconsistent.
    '''
    if not resp or not getattr(resp, 'responses', None):
      return False

    return any(r.success for r in resp.responses)


