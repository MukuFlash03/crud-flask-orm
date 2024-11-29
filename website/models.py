from . import db, bcrypt
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(150), unique=True, nullable=False)
	password = db.Column(db.String(150), nullable=False)
	first_name = db.Column(db.String(150), nullable=False)
	notes = db.relationship('Note')

	def __init__(self, email, password, first_name):
		self.email = email
		self.password = bcrypt.generate_password_hash(password).decode('utf-8')
		self.first_name = first_name

	def __repr__(self):
			return f"User('{self.email}', '{self.first_name}')"

class Note(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	data = db.Column(db.String(10000))
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, data, user_id):
		self.data = data
		self.user_id = user_id

	def __repr__(self):
		return f"Note('{self.data[:50]}...', date: {self.date}, user_id: {self.user_id})"
