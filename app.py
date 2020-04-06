# Importing modules
from flask import Flask, flash, render_template, request, jsonify, redirect, session
from flask import abort
import bcrypt
from flask_cors import CORS, cross_origin
from flask import make_response, url_for
import json
import random
from pymongo import MongoClient
from time import gmtime, strftime
import sqlite3


# connection to MongoDB Database
connection = MongoClient("mongodb://Michal:<Mass1000>@productreviewer-shard-00-00-i8ukj.azure.mongodb.net:27017,productreviewer-shard-00-01-i8ukj.azure.mongodb.net:27017,productreviewer-shard-00-02-i8ukj.azure.mongodb.net:27017/test?ssl=true&replicaSet=productreviewer-shard-0&authSource=admin&retryWrites=true&w=majority")

# Object creation
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '<some secret key>'
CORS(app)

# Initialize Database
def create_mongodatabase():
    try:
        dbnames = connection.database_names()
        if 'cloud_native' not in dbnames:
            db = connection.cloud_native.users
            db_tweets = connection.cloud_native.tweets
            db_api = connection.cloud_native.apirelease

            db.insert({
            "email": "eric.strom@google.com",
            "id": 33,
            "fname": "Eric",
            "sname": "Stromberg",
            "password": "eric@123",
            "username": "eric.strom"
            })

            db_tweets.insert({
            "body": "New blog post,Launch your app with the AWS Startup Kit! #AWS",
            "id": 18,
            "timestamp": "2017-03-11T06:39:40Z",
            "username": "eric.strom"
            })

            db_api.insert( {
              "buildtime": "2017-01-01 10:00:00",
              "links": "/api/v1/users",
              "methods": "get, post, put, delete",
              "version": "v1"
            })
            db_api.insert( {
              "buildtime": "2017-02-11 10:00:00",
              "links": "api/v2/tweets",
              "methods": "get, post",
              "version": "2017-01-10 10:00:00"
            })
            print ("Database Initialize completed!")
        else:
            print ("Database already Initialized!")
    except:
        print ("Database creation failed!!")

# List users
def list_users():
    api_list=[]
    db = connection.cloud_native.users
    for row in db.find({}, {'_id':0}):
        api_list.append(row)
    # print (api_list)
    return jsonify({'user_list': api_list})

# List specific users
def list_user(user_id):
    print (user_id)
    api_list=[]
    db = connection.cloud_native.users
    for i in db.find({'id':user_id}):
        api_list.append(str(i))

    if api_list == []:
        abort(404)
    return jsonify({'user_details':api_list})

# List specific tweet
def list_tweet(user_id):
    print (user_id)
    db = connection.cloud_native.tweets
    api_list=[]
    tweet = db.find({'id':user_id})
    for i in tweet:
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    return jsonify({'tweet': api_list})

# Adding user
def add_user(new_user):
    api_list=[]
    print (new_user)
    db = connection.cloud_native.users
    user = db.find({'$or':[{"username":new_user['username']} ,{"email":new_user['email']}]})
    for i in user:
        print (str(i))
        api_list.append(str(i))

    # print (api_list)
    if api_list == []:
    #    print(new_user)
       db.insert(new_user)
       return "Success"
    else :
       abort(409)

# Deleting User
def del_user(del_user):
    db = connection.cloud_native.users
    api_list=[]
    for i in db.find({'username':del_user}):
        api_list.append(str(i))

    if api_list == []:
        abort(404)
    else:
       db.remove({"username":del_user})
       return "Success"


# List tweets
def list_tweets():
    api_list=[]
    db = connection.cloud_native
    for row in db.tweets.find({}, {'_id':0}):
        api_list.append(row)
    # print (api_list)
    return jsonify({'tweets_list': api_list})

# Adding tweets
def add_tweet(new_tweet):
    api_list=[]
    print (new_tweet)
    db_user = connection.cloud_native.users
    db_tweet = connection.cloud_native.tweets

    user = db_user.find({"username":new_tweet['username']})
    for i in user:
        api_list.append(str(i))
    if api_list == []:
       abort(404)
    else:
        db_tweet.insert(new_tweet)
        return render_template('index.html', show_predictions_madel=True)

def upd_user(user):
    api_list=[]
    print (user)
    db_user = connection.cloud_native.users
    users = db_user.find_one({"id":user['id']})
    for i in users:
        api_list.append(str(i))
    if api_list == []:
       abort(409)
    else:
        db_user.update({'id':user['id']},{'$set': user}, upsert=False )
        return "Success"

# API Routes
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('indexlogged.html', session = session['logged_in'])


@app.route('/signin')
def signin():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('indexlogged.html', session = session['logged_in'], show_predictions_modal=True)


@app.route('/shop')
def shop():
    if not session.get('logged_in'):
        return render_template('shop.html')
    else:
        return render_template('shoplogged.html', session = session['logged_in'])

@app.route('/item')
def item():
    if not session.get('logged_in'):
        return render_template('singleitem.html')
    else:
        return render_template('singleitemlogged.html', session = session['logged_in'])


@app.route('/index')
def index():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('indexlogged.html', session = session['logged_in'])


@app.route("/alreadysignup")
def alreadysignup():
    if not session.get('logged_in'):
        return render_template('signup.html')
    else:
        return render_template('signuplogged.html', session = session['logged_in'])


@app.route('/addname')
def addname():
  if request.args.get('yourname'):
    session['name'] = request.args.get('yourname')
    # Redirect to main
    return redirect(url_for('index'))
  else:
    # getting addname
    return render_template('addname.html', session=session)

@app.route('/clear')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('index'))

@app.route('/adduser')
def adduser():
    return render_template('adduser.html')

@app.route('/clearuser')
def clearuser():
    return render_template('main.html')

@app.route('/addtweets')
def addtweetjs():
    return render_template('addtweets.html')

@app.route("/api/v1/info")
def home_index():
    api_list=[]
    db = connection.cloud_native.apirelease
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'api_version': api_list}), 200



@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name',""),
        'password': request.json['password'],
        'id': random.randint(1,1000)
    }
    return jsonify({'status': add_user(user)}), 201

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user=request.json['username']
    return jsonify({'status': del_user(user)}), 200


@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    user['id']=user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    return jsonify({'status': upd_user(user)}), 200

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():

    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    user_tweet['username'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['timestamp']=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    user_tweet['id'] = random.randint(1,1000)

    return  jsonify({'status': add_tweet(user_tweet)}), 201

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
    return list_tweet(id)


@app.route('/login', methods=['POST'])
def do_admin_login():
    users = connection.cloud_native.users
    api_list=[]
    login_user = users.find({'username': request.form['username']})
    for i in login_user:
        api_list.append(i)
    print (api_list)
    if api_list != []:
            session['logged_in'] = api_list[0]['username']
            return redirect(url_for('index'))
    else:
        return render_template('login.html', show_predictions_mydel=True)

    return 'Invalid User!'



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        users = connection.cloud_native.users
        api_list=[]
        existing_user = users.find({'$or':[{"username":request.form['username']} ,{"email":request.form['email']}]})
        for i in existing_user:
            # print (str(i))
            api_list.append(str(i))

        # print (api_list)
        if api_list == []:
            users.insert({
            "email": (request.form['email']).lower(),
            "id": random.randint(1,1000),
            "fname": request.form['fname'],
            "sname": request.form['sname'],
            "password": bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt()),
            "username": request.form['username']
            })
            session['username'] = request.form['username']
            return render_template('signup.html', show_predictions_model=True)

        return render_template('signup.html', show_predictions_modyl=True)
    else :
        return render_template('signup.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route("/logoutt")
def logoutt():
    session['logged_in'] = False
    return redirect(url_for('signin'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method=='POST':
        users = connection.cloud_native.users
        api_list=[]
        existing_users = users.find({"username":session['username']})
        for i in existing_users:
            # print (str(i))
            api_list.append(str(i))
        user = {}
        print (api_list)
        if api_list != []:
            print (request.form['email'])
            user['email']=(request.form['email']).lower()
            user['fname']= request.form['fname']
            user['sname']= request.form['sname']
            user['password']=bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.update({'username':session['username']},{'$set': user} )
        else:
            return 'User not found!'
        return redirect(url_for('index'))
    if request.method=='GET':
        users = connection.cloud_native.users
        user=[]
        print (session['username'])
        existing_user = users.find({"username":session['username']})
        for i in existing_user:
            user.append(i)
        return render_template('profile.html', fname=user[0]['fname'], sname=user[0]['sname'], username=user[0]['username'], password=user[0]['password'], email=user[0]['email'])


# Error handling
@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)

@app.errorhandler(409)
def user_found(error):
    return make_response(jsonify({'error': 'Conflict! Record exist'}), 409)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

# Main Function
if __name__ == '__main__':
    create_mongodatabase()
    app.run(host='0.0.0.0', port=5000, debug=True)
