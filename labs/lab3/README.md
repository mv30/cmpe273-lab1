## Graphql api

## student creation

Request
```
mutation first_mutation {
    createStudent(student_dict: { name: "John" }) {
        id
        name
    }
}
```

Response
```
{
    "data": {
        "createStudent": {
            "id": 3,
            "name": "John"
        }
    }
}
```

## student updation

Request
```
mutation first_mutation {
    updateStudent( sid: 3, student_dict: { name: "Johny" }) {
        id
        name
    }
}
```

Response
```
{
    "data": {
        "updateStudent": {
            "id": 3,
            "name": "Johny"
        }
    }
}
```

## find student by id

Request
```
query first_query {
    findStudentById( sid: 1) {
        name
    }
}
```

Response
```
{
    "data": {
        "findStudentById": {
            "name": "Mark"
        }
    }
}
```

## lsit all students

Request
```
query first_query {
    findAllStudents{
        id
        name
    }
}
```

Response
```
{
    "data": {
        "findAllStudents": [
            {
                "id": 1,
                "name": "Mark"
            },
            {
                "id": 2,
                "name": "Tom"
            },
            {
                "id": 3,
                "name": "Johny"
            }
        ]
    }
}
```

## class creation

Request
```
mutation first_mutation {
    createClass( class_dict: { subject: "Computer Science" }) {
        id
        subject
    }
}
```

Response
```
{
    "data": {
        "createClass": {
            "id": 1,
            "subject": "Computer Science"
        }
    }
}
```

## class updation

Request
```
mutation first_mutation {
    updateClass( cid: 1, class_dict: { subject: "Distributed System" }) {
        id
        subject
    }
}
```

Response
```
{
    "data": {
        "updateClass": {
            "id": 1,
            "subject": "Distributed System"
        }
    }
}
```

## addition of students to class

Request
```
mutation first_mutation {
    addStudentToClass(cid: 1, sid: 2)
}
```

Response
```
{
    "data": {
        "addStudentToClass": " Student added "
    }
}
```

## find class by id

Request
```
query first_query {
    findClassById( cid: 1) {
        id
        subject
        students {
            id 
            name
        }
    }
}
```

Response
```
{
    "data": {
        "findClassById": {
            "id": 1,
            "students": [
                {
                    "id": 1,
                    "name": "Mark"
                },
                {
                    "id": 2,
                    "name": "Tom"
                },
                {
                    "id": 3,
                    "name": "John"
                }
            ],
            "subject": "Distributed System"
        }
    }
}
```