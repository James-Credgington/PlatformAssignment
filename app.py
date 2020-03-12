from flask import Flask, render_template, request, jsonify, redirect, session
from flask import abort
from flask_cors import CORS, cross_origin
from flask import make_response, url_for
import json
import random
from pymongo import MongoClient
from time import gmtime, strftime
import sqlite3
##from pymongo import Binary
from datetime import datetime
connection = MongoClient("mongodb://localhost:27017/")

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key='<some secret key>'
CORS(app)


def create_database():

    try:
        dbnames = connection.database_names()
        if 'db_viewProducts' not in dbnames:
            db_reviews = connection.db_viewProducts.reviews
            db_products = connection.db_viewProducts.products
            db_images = connection.db_viewProducts.images
            db_users = connection.db_viewProducts.users
            db_api = connection.db_viewProducts.apireleases

            db_users.insert( {
                "id": 0,
                "name": "James Credgington",
                "username": "james.credgington",
                "emailAddress": "381775@students.chesterfield.ac.uk",
                "password": "P@55w0rd",
                "phoneNumber": "02343 234234"
                
            })
       
            db_products.insert( {
                "id": 0,
                "name": "2015 Lenovo B50-80 Laptop",
                "description": "12GB RAM, 500GB HDD, Intel(R) Core(TM)i5-5200U CPU @ 2.20GHz",
                "manufacturer": "Lenovo",
                "averageRating": "3",
                "video": "https://www.youtube.com/watch?v=TBO4KITGL-s",
                "price": "£250", 
                "shippingPrice": "£7.50" })
            db_products.insert( {
                "id": 1,
                "name": "2019 Samsung Galaxy A20e Mobile Phone",
                "description": "2.95GHz Octo-Core CPU, 3GB RAM, 32GB Internal Storage, Android 9.0 Pie, 4G ",
                "manufacturer": "Samsung",
                "averageRating": "0",
                "video": "https://www.youtube.com/watch?v=BdCdv3NJcWQ",
                "price": "£90",
                "shippingPrice": "£1.20"
            })

            db_images.insert( {
                "id": 0,
                "imageUrl": "~\PlatformAssignment\camera pics\DSCF6940.JPG",
                "productId": "0"
            })

            
            db_reviews.insert( {
                "id": 0,
                "dateAndTimeSent": datetime.now(),
                "title": "Good",
                "comment": "It is incredible, very reliable and a general better allrounder than any Macbook Pro", 
                "rating": 5,
                "like": 0,
                "dislike": 0,
                "productId": "0"

            })

            db_api.insert( {
                "buildtime": datetime.now(),
                "links": "/api/v1/users",
                "methods": "get, post, put, delete",
                "version": "v1"})
            db_api.insert( {

              "buildtime": datetime.now(),
              "links": "api/v2/reviews",
              "methods": "get, post",
              "version": "v2"})
            
            db_api.insert( {
              "buildtime": datetime.now(),
              "links": "api/v3/images",
              "methods": "get, post",
              "version": "v3" })
            
            db_api.insert( {
            
              "buildtime": datetime.now(),
              "links": "api/v4/products",
              "methods": "get, post",
              "version": "v4"

            })
            
            print("Database has been created");

        else:
            print("Database has already been created");

    except:
        print("The database has not been created. Try again!");


def list_reviews():
    review_list=[]
    db = connection.db_viewProducts.reviews
    for row in db.find():
        review_list.append(str(row))

    return jsonify({'review_list': review_list})

def list_review(review_id):
    print(review_id)
    review_list=[]
    db = connection.db_viewProducts.reviews
    for row in db.find({'id':review_id}):
        review_list.append(str(row))
    if review_list == []:
        abort(404)
    return jsonify({'review_details':review_list})

def list_products():
    product_list=[]
    db = connection.db_viewProducts.products
    for row in db.find():
        product_list.append(str(row))

    return jsonify({'product_list': product_list})

def list_product(product_id):
    print(product_id)
    product_list=[]
    db = connection.db_viewProducts.products
    for row in db.find({'id':product_id}):
        product_list.append(str(row))
    if product_list == []:
        abort(404)
    return jsonify({'product_details':product_list})

def list_images():
    image_list=[]
    db = connection.db_viewProducts.images
    for row in db.find():
        image_list.append(str(row))
    return jsonify({'image_list': image_list})

def list_image(image_id):
    print(image_id)
    image_list=[]
    db = connection.db_viewProducts.images
    for row in db.find({'id':image_id}):
        image_list.append(str(row))
    if image_list == []:
        abort(404)
    return jsonify({'image_details':image_list})

def list_users():
    user_list=[]
    db = connection.db_viewProducts.users
    for row in db.find():
        user_list.append(str(row))
    return jsonify({'user_list': user_list})

def list_user(user_id):
    print(user_id)
    user_list=[]
    db = connection.db_viewProducts.users
    for row in db.find({'id':user_id}):
        user_list.append(str(row))
    if user_list == []:
        abort(404)
    return jsonify({'user_details':user_list})

def add_review(add_review):
    review_list=[]
    print(add_review)
    db = connection.db_viewProducts.reviews
    user = db.find({'$or':[{'id':add_review['id']}, {"DateAndTimeSent: ":add_review['dateAndTimeSent']}, {"title: ":add_review['title']},
                           {"Comment: ":add_review['comment']}, {"Rating: ":add_review['rating']}, {"Like: ":add_review['like']}, {"Dislike: ":add_review['dislike']},
                           {"Product Id: ":add_review['productId']}]})
    for i in review:
        print (str(i))
        review_list.append(str(i))

    if review_list == []:
        db.insert(add_review)
        return "Review of a certain product has been created"
    else:
        abort(409)
        
def add_product(add_product):
    product_list=[]
    print(add_product)
    db = connection.db_viewProducts.products
    product = db.find({'$or':[{'id':add_product['id']}, {"Name: ":add_product['name']}, {"Email Address: ":add_product['emailAddress']},
                           {"Phone Number: ":add_product['phoneNumber']}, {"Password: ":add_product['password']}]})
    for i in product:
        print (str(i))
        product_list.append(str(i))

    if product_list == []:
        db.insert(add_product)
        return "Product has been added"
    else:
        abort(409)
        
def add_image(add_image):
    image_list=[]
    print(add_image)
    db = connection.db_viewProducts.images
    image = db.find({'$or':[{'id':add_image['id']}, {"Name: ":add_image['name']}, {"Email Address: ":add_image['emailAddress']},
                           {"Phone Number: ":add_image['phoneNumber']}, {"Password: ":add_image['password']}]})
    for i in image:
        print (str(i))
        image_list.append(str(i))

    if image_list == []:
        db.insert(add_image)
        return "Image has been added"
    else:
        abort(409)
        
def add_user(add_user):
    user_list=[]
    print(add_user)
    db = connection.db_viewProducts.users
    user = db.find({'$or':[ {"id":add_user['id']}, {"name":add_user['name']}, {"username":add_user['username']}, {"emailAddress":add_user['emailAddress']}, {"password":add_user['password']}, {"Phone Number: ":add_user['phoneNumber']}]})
    for i in user:
        print (str(i))
        user_list.append(str(i))

    if user_list == []:
        db.insert(add_user)
        return "User has been created"
    else:
        abort(409)

   


 

def upd_review(review_id):
    review_list=[]
    print(review_id)
    db = connection.db_viewProducts.reviews
    review = db.find_one({"Title":review['title']})
    for i in reviews:
        review_list.append(str(i))
    if review_list == []:
       abort(409)
    else:
        db.update({'id':review['id']},{'$set': review_id}, upsert=False )
        return "Updating the review"

def upd_product(product_id):
    product_list=[]
    print(product_id);
    db = connection.db_viewProducts.products
    product = db.find_one({"Name":product['name']})
    for i in products:
        product_list.append(str(i))
    if product_list == []:
       abort(409)
    else:
        db.update({'id':product['id']},{'$set': product_id}, upsert=False )
        return "Updating the review"
    
def upd_image(image_id):
    image_list=[]
    print(image_id)
    db = connection.db_viewProducts.images
    review = db_user.find_one({"id":image_id['id']})
    for i in users:
        image_list.append(str(i))
    if image_list == []:
       abort(409)
    else:
        db.update({'id':image['id']},{'$set': image_id}, upsert=False )
        return "Updating the review"
    
def upd_user(user):
    user_list=[]
    print (user)
    db_user = connection.db_viewProducts.users
    users = db_user.find_one({"id":user['id']})
    for i in users:
        user_list.append(str(i))
    if user_list == []:
       abort(409)
    else:
        db_user.update({'id':user['id']},{'$set': user}, upsert=False )
        return "Updated the User"

@app.route("/api/v1/info")

def home_index():
    api_list=[]
    db = connection.db_api.apireleases
    for row in db.find:
        api_list.append(str(row))
    return jsonify({'api_version':api_list}), 200

@app.route('/api/v1/reviews', methods=['GET'])
def get_reviews():
    return list_reviews()

@app.route('/api/v1/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    return list_review(review_id)

@app.route('/api/v1/products', methods=['GET'])
def get_products():
    return list_products()

@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return list_product(product_id)

@app.route('/api/v1/images', methods=['GET'])
def get_images():
    return list_images()

@app.route('/api/v1/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    return list_image(image_id)

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    ##if not request.json or not 'username' in request.json or not 'emailAddress' in request.json or not 'password' in request.json:
      ##  abort(400)
    user = {
        'id': request.json['id'],
        'name': request.json['name'],
        'username': request.json['username'],
        'emailAddress': request.json['emailAddress'],
        'password': request.json['password'],
        'phoneNumber': request.json['phoneNumber']
    }
    return jsonify({'status': add_user(user)}), 201




@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    user['id']=user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    return jsonify({'status': upd_user(user)}), 200

@app.route('/api/v1/products', methods=['POST'])
def add_products():

    add_product = {}

    if not request.json or not 'name' in request.json or not 'description' in request.json:
        abort(400)

    add_product['name'] = request.json['name']
    add_product['description'] = request.json['description']
    add_product['manufacturer']= request.json['producedBy']
    add_product['averageRating'] = request.json['averageRating']
    add_product['video'] = request.json['video']
    add_product['price'] = request.json['price']
    add_product['shoppingPrice'] = request.json['shoppingPrice']


    return  jsonify({'status': add_product(add_product)}), 201



@app.route('/api/v1/products/<int:product_id>', methods=['PUT'])
def update_products(product_id):
    product = {}
    if not request.json:
      abort(400)
    product['id']=product_id
    key_list = request.json.keys()
    for i in key_list:
        product[i] = request.json[i]
    print (product)
    return jsonify({'status': upd_product(product_id)})

@app.route('/api/v1/images', methods=['POST'])
def add_images():

    images = {}

    if not request.json or not 'imageUrl' in request.json:
        abort(400)

    images['imageUrl'] = request.json['imageUrl']
    images['productId'] = request.json['productId']

    return  jsonify({'status': add_image(add_image)}), 201



@app.route('/api/v1/images/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    image = {}
    if not request.json:
      abort(400)
    image['id']=image_id
    key_list = request.json.keys()
    for i in key_list:
        image[i] = request.json[i]
    print (image)
    return jsonify({'status': upd_image(image_id)})

@app.route('/api/v1/reviews', methods=['POST'])
def add_reviews():

    reviews = {}

    if not request.json or not 'title' in request.json or not 'dateAndTimeSent' in request.json:
        abort(400)

    reviews['dateAndTimeSent'] = request.json['dateAndTimeSent']
    reviews['title'] = request.json['title']

    return  jsonify({'status': add_review(add_review)}), 201


@app.route('/api/v1/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = {}
    if not request.json:
      abort(400)
    review['id']=review_id
    key_list = request.json.keys()
    for i in key_list:
        review[i] = request.json[i]
    print (review)
    return jsonify({'status': upd_review(review_id)})


##@app.route('/') 
##def main():
##    return render_template('main.html') #the login page it will load up first. There just their for now.
##@app.route('/adduser')
##def adduser():
##    return render_template('adduser.html')
##
##@app.route('/addreview')
##def addreview():
##    return render_template('addreview.html')
##
##@app.route('/addproduct')
##def addproduct():
##    return render_template('addproduct.html')
##
##@app.route('/addimage')
##def addimage():
##    return render_template('addproduct.html')
##
##@app.route('/clear')
##def clearsession():
##    session.clear();
##    return redirect(url_for('main'))

# Error handling
@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'HTTP 404 - Cannot be searched on the website'}), 404)

@app.errorhandler(409)
def product_found(error):
    return make_response(jsonify({'error':'HTTP 409 - You have already inserted the data into the database.'}), 409)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error':'HTTP 400 - The server does not recognise the page.'}), 400)

@app.errorhandler(500)
def unknown_error(error):
    return make_response(jsonify({'error':'HTTP 500 - Error is unknown'}), 500)

@app.errorhandler(503)
def service_unavailable(error):
    return make_response(jsonify({'error':'HTTP 503 - The web server is not available to host this website. '}), 503)

@app.errorhandler(504)
def gateway_timeout(error):
    return make_response(jsonify({'error':'HTTP 504 - It has taken too long for the website to be requested to be hosted on the web server. '}), 504)

@app.errorhandler(401)
def unauthorised_access(error):
    return make_response(jsonify({'error':'HTTP 401 - You have accessed this page failing the previous login attempt. Try logging in again.'}), 401)

if __name__ == '__main__':
    create_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
