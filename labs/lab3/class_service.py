
import json
from student_service import find_all_by_id_in

class Class:
    
    id: int
    subject: str
    students: list

    def __init__(self, id, subject, students) -> None:
        self.id = id
        self.subject = subject
        self.students = students
    
    @staticmethod
    def from_dict( dict):
        id = None
        subject = None
        students = None
        if 'id' in dict:
            id = int(dict['id'])
        if 'subject' in dict:
            subject = str(dict['subject'])
        if 'students' in dict:
            students = dict['students']
        return Class( id, subject, students)

classes = dict()

def resolve_create_class( obj, info, class_dict):
    class_dict['id'] = len(classes) + 1
    class_ob = Class.from_dict(class_dict)
    classes[class_ob.id] = [ class_ob, set() ]
    return class_ob

def resolve_update_class( obj, info, cid, class_dict):
    class_ob = Class.from_dict(class_dict)
    existing_class_ob = classes[cid][0]
    if class_ob.subject is not None:
        existing_class_ob.subject = class_ob.subject
    return existing_class_ob

def resolve_add_student_to_class( obj, info, cid, sid):
    classes[cid][1].add(sid)
    return ' Student added '

def resolve_find_class_by_id( obj, info, cid):
    (res_class, sids) = classes[cid]
    students = find_all_by_id_in(sids)
    res_class.students = students
    return res_class


