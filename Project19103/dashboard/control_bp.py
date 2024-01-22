from flask import Blueprint, abort, render_template, redirect, url_for, flash, session
from forms.forms import AddProductForm, EditProductForm
from models import db, Product
from dashboard.customer_bp import place_order


control_bp = Blueprint('control_bp', __name__)

@control_bp.route('/control/dashboard')
def control_dashboard():
    orders = place_order.query.all()
    products = Product.query.all()
    return render_template('control/dashboard.html', orders=orders, products=products)

@control_bp.route('/control/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()

    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            quantity=form.quantity.data
        )
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully', 'success')
        return redirect(url_for('control_bp.control_dashboard'))

    return render_template('control/add_product.html', form=form)

@control_bp.route('/control/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        abort(404)

    form = EditProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        db.session.commit()

        flash('Product updated successfully', 'success')
        return redirect(url_for('control_bp.control_dashboard'))

    return render_template('control/edit_product.html', form=form, product=product)

@control_bp.route('/control/delete_product/<int:product_id>', methods=['GET'])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully', 'success')

    return redirect(url_for('control_bp.control_dashboard'))

@control_bp.route('/control/process_order/<int:order_id>', methods=['POST'])
def process_order(order_id):
    order = place_order.query.get(order_id)

    if not order:
        flash('Order not found', 'danger')
        return redirect(url_for('control_bp.control_dashboard'))

    order.status = 'Processed'
    db.session.commit()

    flash(f'Order {order_id} processed successfully', 'success')
    return redirect(url_for('control_bp.control_dashboard'))
