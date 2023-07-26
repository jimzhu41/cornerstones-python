import base64
import json
import os
import jwt
from time import time
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import Serializer as Serializer
from flask import request,url_for, current_app
from flask_login import UserMixin, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from app import db,login_manager

class Roles(db.Model):
  __table_name__='roles'
  id=db.Column(db.Integer, primary_key=True)
  name=db.Column(db.String(64),unique=True)
  user = db.relationship('User',backref='Roles')

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password=db.Column(db.String(284),index=True)
    active=db.Column(db.Boolean,default=True)
    token=db.Column(db.String(128),unique=True, index=True)
    token_expiration=db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    address = db.relationship('Address',backref='User')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self,password):
        self.password=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password,password)

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def get_reset_password_token(self, expire_in=3600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time()+expire_in},
            current_app.config['SECRET_KEY'],algorithm='HS256')

    def get_token(self,expire_in=3600):
        now=datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token=base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration=now + timedelta(seconds=expire_in)
        db.session.add(self)
        return self.token


    @staticmethod
    def check_token(token):
        user=User.query.filty_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    @staticmethod
    def verify_reset_password_token(token):
        try:
           id = jwt.decode(token,current_app.config['SECRET_KEY'],
                           algorithm=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Address(db.Model):
    __table_name__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    address1 = db.Column(db.String(120))
    address2 = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(20))
    zipcode = db.Column(db.String(10))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
