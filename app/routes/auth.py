from flask import Blueprint, request
from ..models import User
from .. import db
from ..data.users import add_user, get_user_by_email
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = "CLIENT"
    
    # existing_user = get_user_by_email(email)
    existing_user = get_user_by_email(email)

    if existing_user:
        return { "error": "email taken"}, 400
    
    new_user: User = add_user(name, email, password, role)
    login_user(new_user, remember=True)
    return { "new user": new_user.to_dict() }

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    existing_user: User = get_user_by_email(email)
    
    if existing_user and check_password_hash(existing_user.password, password):
        login_user(existing_user, remember=True)
        return { "new user": existing_user.to_dict() }
    
    return { "error": "error" }

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return '<p>Logout</p>'

@auth.route('/upgrade', methods=['POST'])
@login_required
def upgrade():
    existing_user: User = User.query.filter_by(email=current_user.email).first()
    existing_user.role = 'ADMIN'
    db.session.commit()
    return { "message": "User updated successfully" }, 200

@auth.route('/unauthorized')
def unauthorized():
    return '<p>Unauthorized</p>'