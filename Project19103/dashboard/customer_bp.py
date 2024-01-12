from flask import render_template, redirect, url_for, flash, session, Blueprint
from forms.models import Product, Order, db

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/customer/dashboard')
def customer_dashboard():
    car_parts = Product.query.all()
    return render_template('customerDashboard.html', car_parts=car_parts)

@customer_bp.route('/customer/place_order/<int:product_id>', methods=['GET', 'POST'])
def place_order(product_id):
    from forms import PlaceOrderForm  # Import PlaceOrderForm locally in the function

    form = PlaceOrderForm()

    if form.validate_on_submit():
        product = Product.query.get(product_id)
        if not product:
            flash('Product not found', 'danger')
            return redirect(url_for('customer_bp.customer_dashboard'))

        quantity = form.quantity.data
        if quantity > product.quantity:
            flash('Not enough stock available', 'danger')
            return redirect(url_for('customer_bp.customer_dashboard'))

        new_order = Order(user_id=session['user_id'])
        new_order.products.append(product)
        db.session.add(new_order)
        db.session.commit()

        flash('Order placed successfully', 'success')
        return redirect(url_for('customer_bp.customer_dashboard'))

    return render_template('orders/place_order.html', form=form, product=product)
