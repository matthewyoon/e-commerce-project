from flask import Blueprint, request, jsonify
from merchandise_inventory.helpers import token_required
from merchandise_inventory.models import User, Product, product_schema, products_schema, db

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/products', methods = ['POST'])
@token_required
def create_product(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    owner = current_user_token.token

    product = Product(name,description,price,user_token = owner)

    db.session.add(product)
    db.session.commit()

    response = product_schema.dump(product)
    return jsonify(response) 



@api.route('/products', methods = ['GET'])
@token_required
def get_products(current_user_token):
    owner = current_user_token.token
    products = Product.query.filter_by(user_token = owner).all()
    response = products_schema.dump(products)
    return jsonify(response)


@api.route('/products/<id>', methods = ['GET'])
@token_required
def get_product(current_user_token, id):
    product = Product.query.get(id)
    response = product_schema.dump(product)
    return jsonify(response)



@api.route('/products/<id>', methods = ['POST', 'PUT'])
@token_required
def update_product(current_user_token, id):
    product = Product.query.get(id) 

    product.name = request.json['name']
    product.description = request.json['description']
    product.price = request.json['price']
    product.user_token = current_user_token.token

    db.session.commit()
    response = product_schema.dump(product)
    return jsonify(response)



@api.route('/products/<id>', methods = ['DELETE'])
@token_required
def delete_product(current_user_token, id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    response = product_schema.dump(product)
    return jsonify(response)
