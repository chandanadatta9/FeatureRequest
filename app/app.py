from flask import Flask, request, jsonify
import os
import base64
import config as Config
from constants import INSTANCE_FOLDER_PATH
from .api.admin.controller import admin
from logging import INFO, DEBUG, ERROR, handlers, Formatter
from .api.user.controller import user
from .api.features.controller import features 
from .extensions import db,login_manager, ma
from .database_initialize import Users

EXISTING_BLUEPRINTS = [user,admin,features]


def create_app(config = None, app_name = None, blueprints = None):
	if blueprints is None:
		blueprints = EXISTING_BLUEPRINTS
	if app_name is None:
		app_name = Config.DevelopmentConfig.PROJECT

	app = Flask(app_name)
	config_app(app,config)
	config_blueprints(app, blueprints)
	config_extensions(app)
	config_logging(app)
	config_errorhandlers(app)
	return app
	
def config_app(app, config = None):
	app.config.from_object(Config.LocalConfig)  ## this is the default config that will be loaded.
	if config:
		app.config.from_object(Config.load_config(config))
		return  #prod
def config_blueprints(app, blueprints):
	for blueprint in blueprints:
		app.register_blueprint(blueprint)

def config_extensions(app):
	db.init_app(app)
	login_manager.init_app(app)
	ma.init_app(app)
	with app.app_context():
		db.create_all()
		db.session.commit()
	@login_manager.request_loader
	def load_user(request):
		authorization = request.headers.get('Authorization')
		if authorization is None:
			return None
		
		decoded_authorization = base64.b64decode(authorization[authorization.find(' ')+1:])
		username = decoded_authorization[0:decoded_authorization.find(':')]
		password = decoded_authorization[decoded_authorization.find(':')+1 :]
		print username
		print password
		user = Users.query.filter(Users.username == username).first()
		if Users.verify_password(user,password):
			return Users.query.filter(Users.username == username).first()
		else:
			return None
	@login_manager.user_loader
	def userload(username):
		app.logger.info('Authenticating user')
		authorization = request.headers.get('Authorization')
		if authorization is None:
			return None
		else:
			#the format for authorization in headers is BASIC username:password in which username:password part of the header is base64 encoded
			decoded_authorization = base64.b64decode(authorization[authorization.find(' ')+1:])
			username = decoded_authorization[0:decoded_authorization.find(':')]
			password = decoded_authorization[decoded_authorization.find(':')+1 :]
			print username
			print password
			user = Users.query.filter(Users.username == username).first()
			if Users.verify_password(user,password):
				return Users.query.filter(Users.username == username).first()
			else:
				return None

def config_errorhandlers(app):
	@app.errorhandler(404)
	def server_error(error):
		resp = jsonify({'message':'please check the value sent'})
		resp.status_code = 404
		return resp
	@app.errorhandler(401)
	def unauthorized(error):
		resp = jsonify({"error":"unauthorized"})
		resp.status_code = 401
		return resp

def config_logging(app):
	if app.debug or app.testing:
		return
	app.logger.setLevel(DEBUG)

	log_location = os.path.join(app.config['LOG_FOLDER'],'appLog.log')
	info_file_handler = handlers.RotatingFileHandler(log_location, maxBytes = 1024*1024*100, backupCount = 10)
	info_file_handler.setLevel(DEBUG)
	info_file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
		'[in %(pathname)s:%(lineno)d]'))
	app.logger.addHandler(info_file_handler)
	app.logger.info('LOGGER')