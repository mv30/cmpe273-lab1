
class Student:
    
    id: int
    name: str
    
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    @staticmethod
    def from_dict( dict):
        id = None
        name = None
        if 'id' in dict:
            id = int(dict['id'])
        if 'name' in dict:
            name = str(dict['name'])
        return Student( id, name)

students = dict()

def resolve_create( obj, info, student_dict):
    student_dict['id'] = len(students) + 1
    student = Student.from_dict(student_dict)
    students[ student.id ] = student
    return student

def resolve_find_one_by_id( obj, info, sid):
    return students[sid]

def resolve_find_all( obj, info):
    return list(students.values())

def find_all_by_id_in( sids):
    res = []
    for sid in sids:
        res.append(students[sid])
    return res
