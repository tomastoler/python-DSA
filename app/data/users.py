from .. import db
from ..models import User
from werkzeug.security import generate_password_hash

def add_user(*, name: str, email: str, password: str, role='ADMIN') -> User:
    hashed_password = generate_password_hash(password, method="scrypt")
    new_user = User(
                name=name,
                email=email,
                role=role,
                password=hashed_password
               )
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_email(email: str) -> User:
    return User.query.filter(email=email).first()

def get_user_by_id(id: int) -> User:
    return User.query.get(id)