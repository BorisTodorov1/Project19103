# models.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, inspect

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/autohub'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        inspector = inspect(db.engine)
        try:
            tables_exist = all(inspector.has_table(table_name) for table_name in ['category', 'order', 'order_products', 'product', 'user'])
        except Exception as e:
            print(f"An error occurred while checking table existence: {e}")
            tables_exist = False

        if not tables_exist:
            db.create_all()

    return app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100))
    role = db.Column(Enum('Customer', 'Admin', 'Employee', 'Courier', name='roles'), nullable=False)
    current_order_id = db.Column(db.Integer)
    orders = db.relationship('Order', backref='user', lazy=True)



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    ordered_quantity = db.Column(db.Integer, nullable=False)
    deliver_location = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.String(20)) 
    delivery_time = db.Column(db.TIMESTAMP)
    products = db.relationship('Product', secondary='order_products', backref='orders')
    status = db.Column(db.String(20))




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


if __name__ == "__main__":
    # Access the tables_exist variable to resolve the Pylance issue
    app = create_app()
    print(app.tables_exist)
    app.run()