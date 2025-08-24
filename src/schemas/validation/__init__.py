
from marshmallow import Schema
from marshmallow import fields

class SchemaAuthArguments(Schema):
  uid = fields.String(required = True)

