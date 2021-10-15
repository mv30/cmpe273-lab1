## Twitter api


### add user api

Request
```
curl --location --request POST 'http://127.0.0.1:5000/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "john.smith@gmail.com",
    "name": "John Smith"
}'
```

Reponse
```
{
    "email": "john.smith@gmail.com",
    "followers": [],
    "id": "1",
    "name": "John Smith",
    "tweets": []
}
```

### add follower api

Request
```
curl --location --request PATCH 'http://127.0.0.1:5000/users/1/followers/3'
```

Reponse
```
{
    "email": "john.smith@gmail.com",
    "followers": [
        "3",
        "2"
    ],
    "id": "1",
    "name": "John Smith",
    "tweets": []
}
```

### post a tweet api

Request
```
curl --location --request POST 'http://127.0.0.1:5000/users/1/tweets' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tweet": "Hello Everyone"
}'
```

Reponse
```
{
    "tweet": "Hello Everyone",
    "tweet_id": "3"
}
```


### get details of user

Request
```
curl --location --request GET 'http://127.0.0.1:5000/users/1'
```

Reponse
```
{
    "email": "john.smith@gmail.com",
    "followers": [
        "3",
        "2"
    ],
    "id": "1",
    "name": "John Smith",
    "tweets": [
        {
            "tweet": "Fan art is the best",
            "tweet_id": "1"
        },
        {
            "tweet": "Vaccines have a proven track record of saving lives. Let’s keep it going!",
            "tweet_id": "2"
        },
        {
            "tweet": "Hello Everyone",
            "tweet_id": "3"
        }
    ]
}
```

### get details of user-timeline

Request
```
curl --location --request GET 'http://127.0.0.1:5000/users/1/timeline'
```

Reponse
```
{
    "timeline": [
        {
            "tweet": "Fan art is the best",
            "tweet_id": "1",
            "user_id": "1"
        },
        {
            "tweet": "Vaccines have a proven track record of saving lives. Let’s keep it going!",
            "tweet_id": "2",
            "user_id": "1"
        },
        {
            "tweet": "Hello Everyone",
            "tweet_id": "3",
            "user_id": "1"
        }
    ]
}
```