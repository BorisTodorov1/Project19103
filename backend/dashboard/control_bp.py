from flask import Blueprint, abort, render_template, redirect, url_for, flash, request, session
from forms.forms import AddProductForm, EditProductForm, AddCategoryForm, DeleteCategoryForm
from models import db, Product, Order, Category, create_app, User 
from werkzeug.utils import secure_filename
import os

control_bp = Blueprint('control_bp', __name__)

app = create_app()


@control_bp.route('/control/dashboard')
def control_dashboard():
    
    
    if 'user_id' not in session:
        flash('Unauthorized access. Please log in.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    if user.role == 'Admin' and user.role == 'Employee':
        return redirect(url_for('control_bp.control_dashboard'))
   
    orders = Order.query.all()  
    products = Product.query.all()
    categories = Category.query.all()
    
    return render_template('controlDashboard.html', orders=orders, products=products, categories=categories)



@control_bp.route('/control/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        # Handle image upload
        image = form.image.data
        if image:
            filename = secure_filename(image.filename)
            image.save=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_path = os.path.join('images', filename).replace("\\", "/")
        else:
            image_path = None

        # Create a new product
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            quantity=form.quantity.data,
            category_id=form.category.data,
            image=image_path
        )

        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully', 'success')
        return redirect(url_for('control_bp.control_dashboard'))

    return render_template('add_product.html', form=form)

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

    return render_template('edit_product.html', form=form, product=product)

@control_bp.route('/control/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully', 'success')

    return redirect(url_for('control_bp.control_dashboard'))


@control_bp.route('/control/process_order/<int:order_id>', methods=['GET', 'POST'])
def process_order(order_id):
    order = Order.query.get(order_id)

    if not order:
        flash('Order not found', 'danger')
        return redirect(url_for('control_bp.control_dashboard'))

    if order.status != 'Processed' and request.method == 'POST':
        # Update order with additional information
        order.additional_info = request.form.get('additional_info')
        order.status = 'Processed'
        db.session.commit()

        flash(f'Order {order_id} processed successfully', 'success')
        return redirect(url_for('control_bp.control_dashboard'))

    return render_template('process_order.html', order=order)

@control_bp.route('/control/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get(order_id)

    if order:
        db.session.delete(order)
        db.session.commit()
        flash(f'Order {order_id} deleted successfully', 'success')

    return redirect(url_for('control_bp.control_dashboard'))


@control_bp.route('/control/add_category', methods=['GET', 'POST'])
def add_category():
    form = AddCategoryForm()

    if form.validate_on_submit():
        new_category = Category(name=form.name.data, definition=form.definition.data)
        db.session.add(new_category)
        db.session.commit()
        flash(f'Category "{form.name.data}" added successfully', 'success')
        return redirect(url_for('control_bp.control_dashboard'))

    return render_template('add_category.html', form=form)


@control_bp.route('/control/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    form = DeleteCategoryForm()

    if category:
        db.session.delete(category)
        db.session.commit()
        flash(f'Category {category_id} deleted successfully', 'success')

    return redirect(url_for('control_bp.control_dashboard'))
