# models.py
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

from app.main import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Integer, default=0)

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True)
    name = db.Column(db.String(255), nullable=False)

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.category_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)

    # Define foreign key relationships
    user = db.relationship('User', foreign_keys=[user_id])
    category = db.relationship('Category', foreign_keys=[category_id])
