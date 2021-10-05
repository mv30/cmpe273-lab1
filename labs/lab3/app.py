from flask import Flask
from flask import request
from flask import jsonify

from ariadne import graphql_sync
from ariadne import snake_case_fallback_resolvers
from ariadne import ObjectType
from ariadne import load_schema_from_path
from ariadne import make_executable_schema
from ariadne.constants import PLAYGROUND_HTML

import student_service
import class_service

app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/trials", methods=['POST'])
def find_any():
    data = request.get_json()
    success, result = graphql_sync( schema, data, context_value=request, debug=app.debug)
    return jsonify(result)


query = ObjectType("Query")

query.set_field("findStudentById", student_service.resolve_find_one_by_id)
query.set_field("findAllStudents", student_service.resolve_find_all)

query.set_field("findClassById", class_service.resolve_find_class_by_id)

mutation = ObjectType("Mutation")

mutation.set_field("createStudent", student_service.resolve_create)

mutation.set_field("createClass", class_service.resolve_create_class)
mutation.set_field("addStudentToClass", class_service.resolve_add_student_to_class)

type_def = load_schema_from_path("schema.graphql")
schema = make_executable_schema( type_def, query, mutation, snake_case_fallback_resolvers)