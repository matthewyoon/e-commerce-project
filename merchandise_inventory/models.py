from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash #check_password_hash for use in routes later

import secrets

from flask_login import LoginManager, UserMixin

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    product = db.relationship('Product', backref = 'owner', lazy = True)
    
    def __init__(self,email,first_name = '', last_name = '', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'Your username/email: {self.email} has been created and added to database!'

class Product(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, comics_appeared_in, super_power, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = comics_appeared_in
        self.user_token = user_token

    def __repr__(self):
        return f'The following character has been added: {self.name}.'

    def set_id(self):
        return secrets.token_urlsafe()

class ProductSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'price']

product_schema = ProductSchema()
products_schema = ProductSchema(many = True)