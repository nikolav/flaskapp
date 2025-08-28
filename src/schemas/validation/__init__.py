from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate

class SchemaAuthArguments(Schema):
  idToken = fields.String(required = True)

class SchemaValidateCloudMessagingMessage(Schema):
  title = fields.String(required = True)
  body  = fields.String(required = True)
  data  = fields.Dict(allow_none = True)


#################
## payments:adyen
class SchemaAdyenAmount(Schema):
  currency = fields.String(required  = True, validate = validate.Length(equal = 3))
  value    = fields.Integer(required = True, validate = validate.Range(min = 0))

class SchemaAdyenSessionRequest(Schema):
    merchantAccount = fields.String(required = True)
    amount          = fields.Nested(SchemaAdyenAmount, required = True)
    reference       = fields.String(required = True)
    returnUrl       = fields.Url(required = True)
    ## Optional
    # countryCode = fields.String(validate = validate.Length(equal = 2))

