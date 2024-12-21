from marshmallow import Schema, fields

class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    date_of_birth = fields.Date(allow_none=True)
    enrollment_date = fields.Date(allow_none=True)
    program = fields.Str(required=True)
    status = fields.Str(required=True)
    contact_number = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True) 