from flask import Blueprint, request
from ..models import User
from .. import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    hashed_password = generate_password_hash(password, method="scrypt")
    
    existing_user = User.query.filter_by(email=email).first()
    if not existing_user:
        new_user = User(
            name=name,
            email=email,
            role=role,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
    
        login_user(new_user, remember=True)
        return { "new user": new_user.to_dict() }

    return { "error": "email already taken" }


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user and check_password_hash(existing_user.password, password):
        login_user(existing_user, remember=True)
        return { "new user": existing_user.to_dict() }
    
    return '<p>Login</p>'


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return '<p>Logout</p>'


@auth.route('/unauthorized')
def unauthorized():
    return '<p>Unauthorized</p>'