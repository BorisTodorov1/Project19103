from flask import render_template, redirect, url_for, flash, session, Blueprint
from sqlalchemy import func
from models import Product, Order, db, Category
from forms.forms import PlaceOrderForm

customer_bp = Blueprint('customer_bp', __name__)


import time
import random

@customer_bp.route('/customer/dashboard')
def customer_dashboard():
    # Fetch all available products from the database
    categories = Category.query.all()
    products = Product.query.all()
    if 'user_id' not in session:
        flash('Unauthorized access. Please log in.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('customerDashboard.html', car_parts=products, categories=categories)



# Modify the place_order route to include additional information
@customer_bp.route('/customer/place_order/<int:product_id>', methods=['GET', 'POST'])
def place_order(product_id):
    form = PlaceOrderForm()
    product = Product.query.get(product_id)

    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('customer_bp.customer_dashboard'))

    if form.validate_on_submit():
        # Ensure 'user_id' is present in the session
        if 'user_id' not in session:
            flash('User not authenticated', 'danger')
            return redirect(url_for('customer_bp.customer_dashboard'))
        
        order_number = random.randint(0, 10000)

        # Create a new order with the necessary information
        new_order = Order(
            user_id=session['user_id'],
            products=[product],
            ordered_quantity=form.quantity.data,
            deliver_location=form.location.data,
            payment_method=form.payment_method.data,
            order_number = order_number
            # ... other columns
        )

        db.session.add(new_order)
        db.session.commit()

        flash(f'Order placed successfully', 'success')
        return redirect(url_for('customer_bp.customer_dashboard'))

    return render_template('place_order.html', form=form, product=product)

