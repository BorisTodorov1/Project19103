from forms.models import db, User
from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from forms.models import db, User  # Import the User model

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Assuming User is the model for user information
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.id
            if user.role == 'Admin' or user.role == "Employee":
                print("Admin login successful")
                return redirect(url_for('control_dashboard'))
            else:
                print("Customer login successful")
                return redirect(url_for('customer_dashboard'))
        else:
            print("Invalid email or password")
            flash('Invalid email or password')

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Assuming User is the model for user information
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered')
            return redirect(url_for('auth.register'))

        new_user = User(username=request.form['username'], email=email, password=password, role='customer')
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful')
        return redirect(url_for('auth.login'))

    return render_template('register.html')
