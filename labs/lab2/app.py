from marshmallow.fields import Method
from werkzeug.wrappers import request
from schema.students import Student, StudentsSchema
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, request
from datetime import datetime
from flasgger import Swagger

spec = APISpec(
    title="SJSU Student Registration API",
    version="0.0.1",
    openapi_version="3.0.3",
    plugins=[
        # FromFilePlugin("resource"),
        FlaskPlugin(),
        MarshmallowPlugin()
    ],
)

students = []
app = Flask(__name__)
swagger = Swagger(app) 

@app.route("/students/<id>",methods=['GET'])
def get_one(id):
    """ Fetch one student by id
    This api returns an existing student whose id is matches with the id param
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        default: 1
    definitions:
        student:
            type: object
            properties:
                id:
                    type: integer
                first_name:
                    type: string
                last_name:
                    type: string
                email:
                    type: string
                sjsu_id:
                    type: string
            required:
                - first_name
                - last_name
                - email
                - sjsu_id
    responses:
      200:
        description: target student entry
        schema:
          $ref: '#/definitions/student'
      404:
        description: no entry found
        schema:
          type: string
        examples:
          rgb: ' not found :('
    """
    global students
    id = int(id)
    student_schema = StudentsSchema(many=True)
    filtered_students = list(filter(lambda student: student.id == id, students))
    print(filtered_students)
    if len(filtered_students) > 0:
        return student_schema.dumps(filtered_students)
    else :
        return 'Not found', 404

@app.route("/students",methods=['GET'])
def get_all(): 
    """Fetch all existing students
    This api returns all the existing students
    ---
    definitions:
        student:
            type: object
            properties:
                id:
                    type: integer
                first_name:
                    type: string
                last_name:
                    type: string
                email:
                    type: string
                sjsu_id:
                    type: string
            required:
                - first_name
                - last_name
                - email
                - sjsu_id
    responses:
      200:
        description: all student entries
        schema:
            $ref: '#/definitions/student'
    """
    student_schema = StudentsSchema(many=True)
    student_data = student_schema.dumps(students)
    return student_data


@app.route('/students',methods=['POST'])
def create():
    """create a new student
    This api creates a new student with specified description
    ---
    definitions:
        student:
            type: object
            properties:
                id:
                    type: integer
                first_name:
                    type: string
                last_name:
                    type: string
                email:
                    type: string
                sjsu_id:
                    type: string
            required:
                - first_name
                - last_name
                - email
                - sjsu_id
    parameters:
      - name: student
        in: body
        schema:
          $ref: '#/definitions/student'
        required: true
    responses:
      200:
        description: newly created student entry
        schema:
          $ref: '#/definitions/student'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    global students
    student_schema = StudentsSchema()
    student = student_schema.load(request.get_json())
    current_time_stamp = datetime.now()
    student.create_timestamp = current_time_stamp
    student.update_timestamp = current_time_stamp
    students.append(student)
    return student_schema.dump(student)

@app.route("/students/<id>",methods=['PATCH'])
def patch(id):
    """patch update
    This api updates a subset of properties an existing student with specified description
    ---
    definitions:
        student:
            type: object
            properties:
                id:
                    type: integer
                first_name:
                    type: string
                last_name:
                    type: string
                email:
                    type: string
                sjsu_id:
                    type: string
            required:
                - first_name
                - last_name
                - email
                - sjsu_id
    parameters:
      - name: id
        in: path
        schema:
            type: integer
            required: true
            default: 1
      - name: student
        in: body
        schema:
          $ref: '#/definitions/student'
        required: true
    responses:
      200:
        description: patch-updated student entry
        schema:
          $ref: '#/definitions/student'
      404:
        description: no entry found
        schema:
          type: string
        examples:
          rgb: ' not found :('
    """
    global students
    id = int(id)
    student_schema = StudentsSchema()
    student = student_schema.load(request.get_json())
    res = 'Nothing updated'
    for i in range(len(students)):
        if students[i].id == id:
            if student.first_name is not None:
                students[i].first_name = student.first_name
            if student.last_name is not None:
                students[i].last_name = student.last_name
            if student.sjsu_id is not None:
                students[i].sjsu_id= student.sjsu_id
            if student.email is not None:
                students[i].email = student.email
            students[i].update_timestamp = datetime.now()
            res = student_schema.dump(students[i])
            return res
    return res, 404

@app.route("/students/<id>", methods=['PUT'])
def update(id):
    """patch update
    This updatesan existing student with specified description
    ---
    definitions:
        student:
            type: object
            properties:
                id:
                    type: integer
                first_name:
                    type: string
                last_name:
                    type: string
                email:
                    type: string
                sjsu_id:
                    type: string
            required:
                - first_name
                - last_name
                - email
                - sjsu_id
    parameters:
      - name: id
        in: path
        schema:
            type: integer
            required: true
            default: 1
      - name: student
        in: body
        schema:
          $ref: '#/definitions/student'
        required: true
    responses:
      200:
        description: updated student entry
        schema:
          $ref: '#/definitions/student'
      404:
        description: no entry found
        schema:
          type: string
        examples:
          rgb: ' not found :('
    """
    global students
    id = int(id)
    student_schema = StudentsSchema()
    student = student_schema.load(request.get_json())
    for i in range(len(students)):
        if students[i].id == student.id:
            students[i].first_name = student.first_name
            students[i].last_name = student.last_name
            students[i].email = student.email
            students[i].sjsu_id = student.sjsu_id
            students[i].update_timestamp = datetime.now()
            return student_schema.dump(students[i])
    return 'Not found', 404

@app.route("/students/<id>",methods=['DELETE'])
def delete_one(id):
    """delete on by id
    This api deletes any student with matching id
    ---
    definitions:
        student:
            type: object
            properties:
                id:
                    type: integer
                first_name:
                    type: string
                last_name:
                    type: string
                email:
                    type: string
                sjsu_id:
                    type: string
            required:
                - first_name
                - last_name
                - email
                - sjsu_id
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        default: 1
    responses:
      200:
        description: deleted student entry
        schema:
          $ref: '#/definitions/student'
      404:
        description: no entry found
        schema:
          type: string
        examples:
          rgb: ' not found :('
    """
    global students
    id = int(id)
    student_schema = StudentsSchema()
    deleted_students = list(filter(lambda student: student.id == id, students))
    students = list(filter(lambda student: student.id != id, students))
    if len(deleted_students) > 0:
        return student_schema.dump(deleted_students[0])
    else :
        return 'Nothing deleted', 404


with app.test_request_context():
    spec.path(view=get_all)
    spec.path(view=get_one)
    spec.path(view=create)
    spec.path(view=delete_one)
    spec.path(view=update)