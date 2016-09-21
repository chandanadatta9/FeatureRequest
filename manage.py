import os
from flask_script import Manager,Shell, Server
from flask import current_app
from app.extensions import db
import app.database_initialize as database_initialize
from app import create_app
from app.config import DevelopmentConfig

def create_my_app(config = None):
	return create_app(config)

manager = Manager(create_my_app)

manager.add_option('-c','--config',dest = 'config', required = False, help='config [LOCAL, DEVELOPMENT, PRODUCTION]')

@manager.shell
def make_shell_context():
	return dict(app=current_app, db=db, models = database_initialize)

@manager.command
def run():
	"To run in the Local Machine"
	port = int(os.environ.get("PORT",5000))
	current_app.run(host='0.0.0.0',port = port, debug = True)

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
