
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

