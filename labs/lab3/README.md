## Graphql api

## student creation

Request
```
mutation first_mutation {
    createStudent(student_dict: { name: "Kam" }) {
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
            "name": "Kam"
        }
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