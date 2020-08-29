"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    """response_body = {
        "msg": "Hello, this is your GET /user response "
    }"""

    users= User.query.all()
    all_users= list(map(lambda x: x.serialize(), users))


    return jsonify(all_users), 200
    #return jsonify(response_body), 200


@app.route('/user', methods=['POST'])
def create_user():

    request_body_user=request.get_json()

    earth = User(first_name= request_body_user["first_name"], email=request_body_user["email"], password=request_body_user["password"])
    db.session.add(earth)
    db.session.commit()

    print(request_body_user)
    

    return jsonify(request_body_user), 200


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):

    request_body_user= request.get_json()

    user1 = User.query.get(person_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)

    if "username" in request_body_user:
        user1.username = body["username"]
    if "email" in request_body_user:
        user1.email = body["email"]
    if "first_name" in request_body_user:
        user1.first_name = body["first_name"]
    db.session.commit()

    return jsonify(request_body_user), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delate_user(user_id):

    

    user1 = User.query.get(person_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()

    return jsonify("ok"), 200

"""
@app.route('/cart', methods=['DELETE'])
def add_to_cart(user_id):

    request_body_user= request.get_json()
    product_id=request_body_user["product_id"]
    user_id=request_body_user["user_id"]

    record = ShoopinCart.query.filter_by(user_id=user_id,product_id)
    if record is None:
        record= ShopinCart(user_id= user_id, product_id=product_id,quantity=request_body_user["quantity"])
        db.session.add(record)
    else:
        record.quantity=request_body_user["quantity"]


    db.session.commit()

    return jsonify(record), 200
"""

   

   






# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
