from flask import Flask, request, jsonify

app = Flask(__name__)
db = {}
total_tweet_count = 0

class Tweet:
    
    tweet_id: str
    tweet: str

    def __init__(self, tweet_id, tweet) -> None:
        self.tweet_id = tweet_id
        self.tweet = tweet
    
    def to_dict( self):
        tweet_dict = {}
        if self.tweet_id is not None:
            tweet_dict['tweet_id'] = self.tweet_id
        if self.tweet is not None:
            tweet_dict['tweet'] = self.tweet
        return tweet_dict

    @staticmethod
    def from_dict( tweet_dict):
        tweet_id = None
        tweet = None
        if 'tweet_id' in tweet_dict:
            tweet_id = tweet_dict['tweet_id']
        if 'tweet' in tweet_dict:
            tweet = tweet_dict['tweet']
        return Tweet( tweet_id, tweet)

    def display( self):
        print(' tweet_id : ', self.tweet_id, ' tweet: ', self.tweet)

class User:
    
    id: str
    name: str
    email: str
    tweets: list[Tweet]
    followers: list[str]

    def __init__(self, id, name, email, tweets, followers) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.tweets = tweets
        self.followers = followers
    
    def to_dict(self):
        user_dict = {}
        tweet_dicts = []
        followers = []
        if self.id is not None:
            user_dict['id'] = self.id
        if self.name is not None:
            user_dict['name'] = self.name
        if self.email is not None:
            user_dict['email'] = self.email
        if self.tweets is not None:
            for tweet in self.tweets:
                tweet_dict = tweet.to_dict()
                tweet_dicts.append(tweet_dict)
        if self.followers is not None:
            for follower in self.followers:
                followers.append(follower)
        user_dict['tweets'] = tweet_dicts
        user_dict['followers'] = followers
        return user_dict

    @staticmethod 
    def from_dict(user_dict):
        id = None
        name = None
        email = None
        tweets = []
        followers = []
        if 'id' in user_dict:
            id = user_dict['id']
        if 'name' in user_dict:
            name = user_dict['name']
        if 'email' in user_dict:
            email = user_dict['email']
        if 'tweets' in user_dict:
            for tweet_dict in user_dict['tweets']:
                tweet = Tweet.from_dict(tweet_dict)
                tweets.append(tweet)
        if 'followers' in user_dict:
            followers = user_dict['followers']
        return User( id, name, email, tweets, followers)

    def display( self):
        print(' id: ', self.id, ' name: ', self.name, ' email: ', self.email, 'followers', self.followers)
        if self.tweets is not None:
            for tweet in self.tweets:
                tweet.display()

class TimelineReponse:

    user_id: int
    timeline: list[Tweet]

    def __init__(self, user_id) -> None:
        self.user_id = str(user_id)
        global db
        user = db[user_id]
        tweets = user.tweets
        self.timeline = sorted(tweets, key=lambda tweet: int(tweet.tweet_id))
    
    def to_dict( self):
        res = {}
        tweets_dicts = []
        for i in range(len(self.timeline)):
            tweet_dict = self.timeline[i].to_dict()
            tweet_dict['user_id'] = str(self.user_id)
            tweets_dicts.append(tweet_dict)
        res['timeline'] = tweets_dicts
        return res


@app.route('/users', methods=['POST'])
def create_user():
    global db
    user = User.from_dict(request.get_json())
    new_user_id = len(db) + 1
    user.id = str(new_user_id)
    db[new_user_id] = user
    return jsonify(user.to_dict()), 200

@app.route('/users/<user_id>/followers/<follower_id>', methods=['PATCH'])
def add_followers( user_id, follower_id):
    global db
    user_id = int(user_id)
    follower_id = int(follower_id)
    if user_id not in db:
        error_message = ' user_id ' + user_id + ' does not exists '
        return error_message, 404
    if follower_id not in db:
        error_message = ' follower_id ' + follower_id + ' does not exists '
        return error_message, 404
    user = db[user_id]
    followers = set(user.followers)
    followers.add(str(follower_id))
    user.followers = list(followers)
    db[user_id] = user
    return jsonify(user.to_dict()), 200

@app.route("/users/<user_id>/tweets", methods=['POST'])
def add_tweets( user_id):
    global db
    global total_tweet_count
    user_id = int(user_id)
    if user_id not in db:
        error_message = ' user_id ' + user_id + ' does not exists '
        return error_message, 404
    total_tweet_count = total_tweet_count + 1
    tweet = Tweet.from_dict(request.get_json())
    tweet.tweet_id = str(total_tweet_count)
    user = db[user_id]
    user.tweets.append(tweet)
    db[user_id] = user
    return jsonify(tweet.to_dict()), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user_id = int(user_id)
    user = db[user_id]
    return jsonify(user.to_dict()), 200

@app.route('/users/<user_id>/timeline', methods=['GET'])
def get_timeline( user_id):
    user_id = int(user_id)
    return jsonify(TimelineReponse(user_id).to_dict()), 200



