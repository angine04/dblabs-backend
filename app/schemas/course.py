from marshmallow import Schema, fields

class CourseScheduleSchema(Schema):
    id = fields.Int(dump_only=True)
    day = fields.Str(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)

class CourseSchema(Schema):
    id = fields.Int(dump_only=True)
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    credits = fields.Int(required=True)
    instructor = fields.Str(required=True)
    semester = fields.Str(required=True)
    capacity = fields.Int(required=True)
    status = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Nested relationships
    schedule = fields.Nested(CourseScheduleSchema, many=True)