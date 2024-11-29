import os
from os import path
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()

DB_NAME = os.getenv('DB_NAME')

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

	db.init_app(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	from .views import views
	from .auth import auth

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	from .models import User, Note

	create_database(app)

	return app

def create_database(app):
	if not path.exists("instance/" + DB_NAME):
		with app.app_context():
			db.create_all()
		print("Created Database!")
