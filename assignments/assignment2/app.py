from random import seed
import random
from string import ascii_lowercase
from hashlib import md5
from flask import Flask, request, jsonify

random.seed(1)
app = Flask(__name__)
data = {}

values = list(ascii_lowercase)
for i in range(10):
    values.append(str(i))

class UrlDetails:
    
    group_id: str
    shorten_url: str
    original_url: str
    click_count: int
    tags: list[str]

    def __init__(self, group_id, shorten_url, original_url, click_count, tags) -> None:
        self.group_id = group_id
        self.shorten_url = shorten_url
        self.original_url = original_url
        self.click_count = click_count
        self.tags = tags
    
    @staticmethod
    def from_dict(details_map: dict):

        url_details = UrlDetails( None, None, None, None, None)

        if not ('click_count' in details_map):
            details_map['click_count'] = 0
        if not ('group_id' in details_map):
            details_map['group_id'] = 'bit.ly'

        if 'group_id' in details_map:
            url_details.group_id = details_map['group_id']
        if 'shorten_url' in details_map:
            url_details.shorten_url = details_map['shorten_url']
        if 'original_url' in details_map:
            url_details.original_url = details_map['original_url']
        if 'click_count' in details_map:
            url_details.click_count = details_map['click_count']
        if 'tags' in details_map:
            url_details.tags = details_map['tags']

        return url_details

    def to_dict(self):
        res = dict()
        if self.group_id is not None:
            res['group_id'] = self.group_id
        if self.shorten_url is not None:
            res['shorten_url'] = self.shorten_url
        if self.original_url is not None:
            res['original_url'] = self.original_url 
        if self.click_count is not None:
            res['click_count'] = self.click_count
        if self.tags is not None:
            res['tags'] = self.tags      
        return res
        

    def get_shortened_url( original_url: str):
        original_url_as_list = list(original_url)
        n = len(original_url)
        # handling collisions
        while True:
            shorten_url = str(md5(original_url.encode()).hexdigest()[:8])
            if shorten_url not in data:
                return shorten_url
            rand_id = int(random.random()*len(values))
            rand_char = values[rand_id]
            str_id = int(random.random()*n)
            original_url_as_list[str_id] = rand_char
            original_url = str(original_url_as_list)

def check_validity(url):
    if url is None:
        raise Exception(' shorten url can not be NONE ')        
    if url not in data:
        raise Exception(' shorten url was not FOUND ')        

@app.route("/create", methods=['POST'])
def shorten():
    url_details = UrlDetails.from_dict(request.get_json())
    url_details.shorten_url = UrlDetails.get_shortened_url(url_details.original_url)
    url_details.click_count = 0
    data[url_details.shorten_url] = url_details
    return jsonify(url_details.to_dict())

@app.route("/get/<url>", methods=['GET'])
def get(url):
    check_validity(url)
    url_details = data[url]
    url_details.click_count = url_details.click_count + 1
    data[url] = url_details
    return url_details.original_url

@app.route("/get_clicks/<url>",methods=['GET'])
def get_click_counts(url):
    check_validity(url)
    url_details = data[url]
    return str(url_details.click_count)

@app.route("/patch", methods=['PATCH'])
def patch():
    url_details_to_update = UrlDetails.from_dict(request.get_json())
    check_validity(url_details_to_update.shorten_url)
    url_details = data[url_details_to_update.shorten_url]
    if url_details_to_update.tags is not None:
        url_details.tags = url_details_to_update.tags
    data[url_details.shorten_url] = url_details.shorten_url
    return jsonify(url_details.to_dict())

@app.route("/update", methods=['PUT'])
def update():
    url_details_to_update = UrlDetails.from_dict(request.get_json())
    check_validity(url_details_to_update.shorten_url)
    url_details_to_update.click_count = 0
    data[url_details_to_update.shorten_url] = url_details_to_update
    return jsonify(url_details_to_update.to_dict())

@app.route("/remove/<url>", methods=['DELETE'])
def delete(url):
    check_validity(url)
    url_details = data[url]
    del data[url]
    return jsonify(url_details.to_dict())
