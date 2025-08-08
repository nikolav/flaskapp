
# https://marshmallow.readthedocs.io/en/stable/quickstart.html#field-validators-as-methods
from marshmallow import Schema
from marshmallow import fields


class SchemaSerializeTimes(Schema):
  created_at = fields.DateTime()
  updated_at = fields.DateTime()


class SchemaSerializeDocs(SchemaSerializeTimes):
  id   = fields.Integer()
  data = fields.Dict()
  key  = fields.String()


