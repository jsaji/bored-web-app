"""
models.py
- Data classes for the bored web app
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(INTEGER(unsigned=True), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    
    user_activities = relationship('UserActivity')

    def __init__(self, email, password, **kwargs):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
  
        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return {
            'user_id':self.user_id,
            'email':self.email
        }

class Activity(db.Model):
    __tablename__ = 'activities'

    activity_id = db.Column(INTEGER(unsigned=True), primary_key=True, unique=True)
    description = db.Column(db.String(500), nullable=False)
    activity_type = db.Column(db.String(255), nullable=False)
    participants = db.Column(db.Integer)
    accessibility = db.Column(db.Integer)
    price = db.Column(db.Integer)
    link = db.Column(db.String(500), nullable=True)

    user_activities = relationship('UserActivity')
    
    def __init__(self, activity_id, description, activity_type, participants, accessibility, price, link, **kwargs):
        self.activity_id = activity_id
        self.description = description
        self.activity_type = activity_type
        self.participants = participants
        self.accessibility = accessibility
        self.price = price
        self.link = link

    def to_dict(self):
        return {
            'activity_id':self.activity_id,
            'description':self.description,
            'activity_type':self.activity_type,
            'participants': self.participants,
            'accessibility':self.accessibility,
            'price':self.price,
            'link':self.link
        }


class UserActivity(db.Model):
    __tablename__ = 'userActivities'

    user_activity_id = db.Column(INTEGER(unsigned=True), primary_key=True)
    user_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('users.user_id'), nullable=False)
    activity_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('activities.activity_id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, activity_id, **kwargs):
        self.user_id = user_id
        self.activity_id = activity_id
    
    def to_dict(self):
        return {
            'user_id':self.user_id,
            'user_activity_id':self.user_activity_id,
            'activity_id': self.activity_id,
            'is_completed':self.is_completed,
            'date_added':self.date_added
        }

