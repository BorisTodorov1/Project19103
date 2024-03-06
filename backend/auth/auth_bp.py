# Import necessary libraries and modules
from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from models import db, User  # Assuming you have your User model in the 'models' module
import bcrypt

# Create a Blueprint for authentication
auth = Blueprint('auth', __name__)

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.id
            session['user_role'] = user.role
            if user.role == 'Admin' or user.role == "Employee":
                flash('Admin login successful!', 'success')
                return redirect(url_for('control_bp.control_dashboard'))
            else:
                flash('Customer login successful!', 'success')
                return redirect(url_for('customer_bp.customer_dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

# Registration route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered')
            return redirect(url_for('auth.register'))

        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(len(hashed_password))

        new_user = User(username=request.form['new-username'], email=email, password=hashed_password, role='customer')
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

# Logout route
@auth.route('/logout')
def logout():
    # Clear the session, effectively logging the user out
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))
