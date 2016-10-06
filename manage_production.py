import os
from flask_script import Manager,Shell, Server
from flask import current_app
from app.extensions import db
import app.database_initialize as database_initialize
from app import create_app
from app.config import DevelopmentConfig

def create_my_app(config = None):
	return create_app(config = 'PRODUCTION')

manager = Manager(create_my_app)

manager.add_option('-c','--config',dest = 'config', required = False, help='config [LOCAL, DEVELOPMENT, PRODUCTION]')
	
@manager.command
def initdb():
	db.drop_all()
	db.create_all()

	user = database_initialize.Users(username = u'AdminUser',
									 isAdmin = 1)
	user.hash_password('AdminPassword')
	db.session.add(user)
	db.session.commit()

if __name__ == '__main__':
	manager.run()
