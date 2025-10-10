
import smtplib
from email.mime.text      import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import render_template

from src.config import Config
from src.utils  import Utils


class SMTP:
  @staticmethod
  def send(*, to, subject, message):
    r = Utils.ResponseStatus()
    result = None

    msg = MIMEMultipart('alternative')
    msg['To']      = to
    msg['Subject'] = subject
    msg['From']    = Config.mail['EMAIL_SENDER']

    msg.attach(MIMEText(message, 'html'))

    try:
      with smtplib.SMTP_SSL(Config.mail['HOST'], Config.mail['PORT']) as server:
        server.login(Config.mail['USER'], Config.mail['PASSWORD'])
        result = server.send_message(msg)

    except Exception as e:
      r.error = e
    
    else:
      r.status = result

    
    return r
  

  @staticmethod
  def render_mail_template(template_name, **context):
    return render_template(f'mail/{template_name}/index.html', **context)

