from flask_restful import fields

section_field = {
    "id": fields.Integer,
    "name": fields.String,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,
}

user_field = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "active": fields.Boolean,
}

product_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "price": fields.Float,
    "stock": fields.Float,
    "expiry": fields.DateTime,
    "mfd": fields.DateTime,
    "unit_of_sale": fields.String,
    "section_id": fields.Integer,
    "section": fields.Nested(section_field),
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,
}