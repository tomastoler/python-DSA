from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user
from ..models import Certificate
from .. import db


notes = Blueprint('views', __name__)

@notes.route('/')
@login_required
def home():
    user_id = current_user.id
    notes = [certificate.to_dict() for certificate in Certificate.query.filter_by(user_id=user_id).all()]
    return { 'notes': notes }, 200


@notes.route('/add-certificate', methods=['POST'])
@login_required
def add_certificate():
    if not current_user['role'] == 'ADMIN':
        return redirect(url_for('/auth/unauthorized'))
    user_id = current_user['id']
    new_certificate = Certificate(user_id=user_id)
    db.session.add(new_certificate)
    db.session.commit()
    return { "message": "note created succesfully" }, 200

    
        