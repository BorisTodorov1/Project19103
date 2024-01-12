from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/autohub'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100))
    role = db.Column(Enum('Customer', 'Admin', 'Employee', 'Courier', name='roles'), nullable=False)  # Use name parameter for Enum
    current_order_id = db.Column(db.Integer)
    orders = db.relationship('Order', backref='user', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(30), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    delivery_time = db.Column(db.TIMESTAMP)
    deliver_location = db.Column(db.String(100))
    products = db.relationship('Product', secondary='order_products', backref='orders')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    definition = db.Column(db.String(50))
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

order_products = db.Table('order_products',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

# Run this only once to create tables in your database
# db.create_all()
