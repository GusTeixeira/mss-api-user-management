from marshmallow import Schema, fields, INCLUDE

class UserSchema(Schema):
    nome = fields.Str(required=True)
    documento = fields.Str(required=False)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)

    class Meta:
        unknown = INCLUDE
        
class LoginSchema(Schema):
    username = fields.Str(required=False)
    password = fields.Str(required=True)

    class Meta:
        unknown = INCLUDE