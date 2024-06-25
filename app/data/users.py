from ..models import User
from werkzeug.security import generate_password_hash
from .. import db

def add_user(name: str, email: str, password: str, role: str = 'ADMIN') -> User:
    hashed_password = generate_password_hash(password, method="scrypt")
    new_user = User(
                name=name,
                email=email,
                password=hashed_password,
                role=role
               )
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_email(email: str) -> User | None:
    return User.query.filter_by(email=email).first()

def get_user_by_id(id: int) -> User:
    return User.query.get(id)