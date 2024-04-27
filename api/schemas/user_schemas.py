from marshmallow import Schema, fields, INCLUDE

class UserSchema(Schema):
    nome = fields.Str(required=True)
    documento = fields.Str(required=False)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)

    class Meta:
        unknown = INCLUDE