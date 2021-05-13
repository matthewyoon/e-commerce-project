from flask import Blueprint, request, jsonify
from merchandise_inventory.helpers import token_required
from merchandise_inventory.models import User, Product, product_schema, products_schema, db

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/products', methods = ['POST'])
@token_required
def create_character(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    owner = current_user_token.token

    character = Product(name,description,price,user_token = owner)

    db.session.add(character)
    db.session.commit()

    response = product_schema.dump(character)
    return jsonify(response) 



@api.route('/products', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    products = Product.query.filter_by(user_token = owner).all()
    response = products_schema.dump(products)
    return jsonify(response)


@api.route('/products/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    product = Product.query.get(id)
    response = product_schema.dump(product)
    return jsonify(response)



@api.route('/products/<id>', methods = ['POST', 'PUT'])
@token_required
def update_character(current_user_token, id):
    product = Product.query.get(id) 

    product.name = request.json['name']
    product.description = request.json['description']
    product.comics_appeared_in = request.json['comics_appeared_in']
    product.super_power = request.json['super_power']
    product.user_token = current_user_token.token

    db.session.commit()
    response = product_schema.dump(product)
    return jsonify(response)



@api.route('/products/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    response = product_schema.dump(product)
    return jsonify(response)
