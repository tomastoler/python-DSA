from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False) # role enaum { "ADMIN", "CLIENT" }
    certificates = db.relationship('Certificate')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }