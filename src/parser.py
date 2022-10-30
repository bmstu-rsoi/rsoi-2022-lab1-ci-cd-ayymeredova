from marshmallow import Schema, fields


class PersonSchema(Schema):
    name=fields.String(attribute="name", required=True)
    address=fields.String(attribute="address", required=True)
    work=fields.String(attribute="work", required=True)
    age = fields.Integer(attribute="age", required=True)