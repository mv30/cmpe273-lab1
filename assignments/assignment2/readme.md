## URL shortener 

### url creation

Request
```
curl --location --request POST 'http://127.0.0.1:5000/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "group_id": "sjsu",
    "original_url": "https://www.linkedin.com/",
    "tags": [
        "professional",
        "networking"
    ]
}'
```

Response
```
{
    "click_count": 0,
    "group_id": "sjsu",
    "original_url": "https://www.linkedin.com/",
    "shorten_url": "dca6074c",
    "tags": [
        "professional",
        "networking"
    ]
}
```

On repeated same requests different url generated thats handled with collision resolution


Response
```
{
    "click_count": 0,
    "group_id": "sjsu",
    "original_url": "https://www.linkedin.com/",
    "shorten_url": "aa9dd5b5",
    "tags": [
        "career",
        "jobs"
    ]
}
```


### get details from short url

Request
```
curl --location --request GET 'http://127.0.0.1:5000/get_details/4ef43251'
```

Response
```
{'group_id': 'sjsu', 'shorten_url': '4ef43251', 'original_url': 'https://www.linkedin.com/', 'click_count': 0, 'tags':
['professional', 'networking']}
```

### get original url from short url

Request
```
curl --location --request GET 'http://127.0.0.1:5000/get/dca6074c'
```

Response
```
https://www.linkedin.com/
```

### get click counts from short url

Request
```
curl --location --request GET 'http://127.0.0.1:5000/get_clicks/dca6074c'
```

Response
```
5
```

### patch update url details

Request
```
curl --location --request PATCH 'http://127.0.0.1:5000/patch' \
--header 'Content-Type: application/json' \
--data-raw '{
    "click_count": 0,
    "group_id": "sjsu",
    "original_url": "https://www.linkedin.com/",
    "shorten_url": "dca6074c",
    "tags": [
        "professional",
        "networking",
        "digital marketting",
        "social networking"
    ]
}'
```

Response
```
{
    "click_count": 5,
    "group_id": "sjsu",
    "original_url": "https://www.linkedin.com/",
    "shorten_url": "dca6074c",
    "tags": [
        "professional",
        "networking",
        "digital marketting",
        "social networking"
    ]
}
```

### update an existing url details

Request
```
curl --location --request PUT 'http://127.0.0.1:5000/update' \
--header 'Content-Type: application/json' \
--data-raw '{
    "click_count": 0,
    "group_id": "sjsu",
    "original_url": "https://www.google.com/",
    "shorten_url": "aa9dd5b5",
    "tags": [
        "search engine",
        "learning"
    ]
}'
```

Response
```
{
    "click_count": 0,
    "group_id": "sjsu",
    "original_url": "https://www.google.com/",
    "shorten_url": "aa9dd5b5",
    "tags": [
        "search engine",
        "learning"
    ]
}
```

### delete an existing url details

Request
```
curl --location --request DELETE 'http://127.0.0.1:5000/remove/4ef43251'
```

Response
```
{
    "click_count": 0,
    "group_id": "sjsu",
    "original_url": "https://www.linkedin.com/",
    "shorten_url": "4ef43251",
    "tags": [
        "professional",
        "networking"
    ]
}
```

