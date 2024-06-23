from flask import Blueprint, request
from ..models import User
from .. import db
from ..data.users import add_user, get_user_by_email
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required


auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = "CLIENT"
    hashed_password = generate_password_hash(password, method="scrypt")
    
    print('len hashed-password -> ' + str(len(hashed_password)))
    
    existing_user = get_user_by_email(email)
    
    if existing_user:
        return { "error": "email or password mismatch"}, 400
    try: 
        if not existing_user:
            new_user: User = add_user(name, email, password, role)
        
            login_user(new_user, remember=True)
            return { "new user": new_user.to_dict() }
    except:
        return { "error": "error" }


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    existing_user = get_user_by_email(email)
    
    if existing_user and check_password_hash(existing_user.password, password):
        login_user(existing_user, remember=True)
        return { "new user": existing_user.to_dict() }
    
    return { "error": "error" }


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return '<p>Logout</p>'


@auth.route('/unauthorized')
def unauthorized():
    return '<p>Unauthorized</p>'