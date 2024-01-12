from flask import session, render_template
from dashboard.control_bp import control_bp
from dashboard.customer_bp import customer_bp
from forms.models import User, create_app
from auth.auth_bp import auth

app = create_app()



@app.route('/')
def home():
    return render_template('home.html')

@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
    return dict(User=user)



app.register_blueprint(auth)
app.register_blueprint(control_bp)
app.register_blueprint(customer_bp)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
