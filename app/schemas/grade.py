from marshmallow import Schema, fields
from datetime import datetime

class GradeSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Int(required=True)
    course_id = fields.Int(required=True)
    score = fields.Float(required=True)
    submission_date = fields.DateTime(dump_only=True)
    comments = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Nested relationships
    student = fields.Nested('StudentSchema', only=('id', 'student_id', 'first_name', 'last_name', 'email'), dump_only=True)
    course = fields.Nested('CourseSchema', only=('id', 'code', 'name', 'semester'), dump_only=True) 