import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, DateTime
#from sqlalchemy.ext.decalarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask import Flask
from .extensions import db
import datetime
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context


class Users(db.Model):
	__tablename__ = 'Users'
	username = db.Column(String(255), nullable = False, primary_key = True, index = True)
	#password = db.Column(String(255), nullable = False)
	pwd_hash = db.Column(String(255),nullable = False)
	authenticated = db.Column(Boolean, default = False)
	isAdmin = db.Column(Boolean, default = False)

	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def get_id(self):
		return unicode(self.username)
	def hash_password(self,password):
		self.pwd_hash = pwd_context.encrypt(password)
	
	def is_anonymous(self):
		return False
	def verify_password(self,password):
		return pwd_context.verify(password, self.pwd_hash)

class Clients(db.Model):
	__tablename__ = 'Clients'
	clientid = db.Column(Integer, primary_key = True)
	clientname = db.Column(String(255), nullable = False)
	email = db.Column(String(255))
	#implement autoincrement

class Projects(db.Model):
	__tablename__ = 'Projects'
	projectid = db.Column(Integer, primary_key = True)
	projectname =  db.Column(String(255),nullable = False)

class Requests(db.Model):
	__tablename__ = 'Requests'
	requestID = db.Column(Integer, primary_key = True, index = True)
	requestTitle = db.Column(String(255))
	requestDescription = db.Column(String(500))
	clientname = db.Column(String(255), nullable = False)
	clientPriority = db.Column(Integer)
	requestDate = db.Column(DateTime, default = datetime.datetime.utcnow)
	targetDate = db.Column(Date)
	productArea = db.Column(String(255))
	ticketURL = db.Column(String(255))
	#request = relationship(Projects)

