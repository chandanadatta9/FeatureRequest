from flask import Flask, flash, redirect, session, url_for, request, render_template,jsonify, Blueprint
from flask_login import login_user,logout_user, current_user, login_required, LoginManager
from ...extensions import db, ma, login_manager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ...database_initialize import Users,Clients, Projects, Requests
import base64
from ...common.schemas import user_schema

user = Blueprint('user',__name__, url_prefix='/api/user')

@user.route('/',methods = ['GET','POST'])
def loginAuthenticate():
	if request.method == 'GET':        		#/api/user/login?username=chandana&password=chandana
		return jsonify({"message":"this is json"})
	elif request.method == 'POST':
		if request.json.get('method') == 'login':
		    #/api/user/login?username=chandana&password=chandana
			user = db.session.query(Users).filter(Users.username == request.json.get('username')).first()
			if user is not None:
				if user.verify_password(request.json.get('password')) is True:
					user.authenticated = True
					db.session.add(user)
					db.session.commit()
					login_user(user, remember = True)

					output = jsonify({"isAuthenticated":1,
						 	 "isAdmin": user.isAdmin,
							  })
					output.status_code = 200
					return output
				else:
					output = jsonify({"isAuthenticated":0,
						 	 "isAdmin": user.isAdmin,
						 	 })
					output.status_code = 400
					return output
			else:
				resp = jsonify({'message':'user not found'})
				resp.status_code = 400
				return resp
		elif request.json.get('method') == 'register':
			username = request.json.get('username')
			password = request.json.get('password')
			if username is None or password is None:
				if username is None and password is not None:
					resp = jsonify({'message':'username required'})
					resp.status_code = 400
					return resp
				elif username is not None and password is None:
					resp = jsonify({'message':'password required'})
					resp.status_code = 400
					return resp
				else:
					resp = jsonify({'message': 'username password required'})
					resp.status_code = 400
					return resp
			if Users.query.filter(Users.username == username).first() is not None:
				resp = jsonify({'message':'username already exists'})
				resp.status_code = 400
				return resp
			newUser = Users(username = username)
			newUser.hash_password(password)
			if request.json.get('isAdmin') is not None:
				newUser.isAdmin = request.json.get('isAdmin')
			db.session.add(newUser)
			db.session.commit()
			resp = jsonify({'message' : 'user created'})
			resp.status_code = 201
			return resp
		else:
			resp = jsonify({'message':'please send a correct method for user api call'})
			resp.status_code = 400
			return resp

@user.route('/logout', methods = ['GET'])
@login_required
def logout():
	logout_user()
	resp = jsonify({'message':'user logged out'})
	resp.status_code = 200
	return resp