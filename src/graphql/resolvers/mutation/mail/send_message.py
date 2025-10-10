
from src.graphql.setup      import mutation
from src.services.mail.smtp import SMTP


# mailSendMessage(to: String!, subject: String!, template: String!, context: JsonData): JsonData!
@mutation.field('mailSendMessage')
def resolve_mailSendMessage(_obj, _info, to, subject, template, context = {}):
  r = SMTP.send(
    to      = to,
    subject = subject,
    message = SMTP.render_mail_template(template, **context)
  )

  return r.dump()

