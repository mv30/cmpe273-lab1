
from marshmallow import Schema, fields, post_load
from datetime import datetime

class StudentsSchema(Schema):
    
    id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    sjsu_id = fields.Str(required=True)
    email = fields.Str(required=True)
    create_timestamp = fields.DateTime(format="timestamp")
    update_timestamp = fields.DateTime(format="timestamp")

    @post_load
    def make_user(self, data, **kwargs):
        return Student(**data)

class Student:

    id: str
    first_name: str
    last_name: str
    sjsu_id: str
    email: str
    create_timestamp: datetime
    update_timestamp: datetime

    def __init__(self, id, first_name, last_name, sjsu_id, email) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.sjsu_id = sjsu_id
        self.email = email



