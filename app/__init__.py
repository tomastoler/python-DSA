from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os


load_dotenv()

db = SQLAlchemy()
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_DATABASE = os.getenv('POSTGRES_DB')
DB_HOST = os.getenv('POSTGRES_HOST')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qwertypoint'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_DATABASE}'
    
    print(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_DATABASE}')
    db.init_app(app)
    
    # routes
    from .routes.notes import notes
    from .routes.auth import auth
    
    app.register_blueprint(notes, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    
    # db
    from .models import User, Certificate
    
    with app.app_context():
        db.create_all()
    
    # authentication
    login_manager = LoginManager()
    login_manager.login_view = 'auth.unauthorized'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

