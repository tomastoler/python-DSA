from flask import Blueprint, request
from ..models import User
from .. import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['POST'])
def sign_up():
    
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    hashed_password = generate_password_hash(password, method="scrypt")
    
    existing_user = User.query.filter_by(email=email).first()
    if not existing_user:
        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
    
        login_user(new_user, remember=True)
    
        return { "new user": new_user.to_dict() }

    return { "error": "email already taken" }

@auth.route('/login')
def login():
    return '<p>Login</p>'


@auth.route('/logout')
def logout():
    return '<p>Logout</p>'



@auth.route('/unauthorized')
def unauthorized():
    return '<p>Unauthorized</p>'