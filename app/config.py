import os
from .constants import INSTANCE_FOLDER_PATH

class BaseConfig(object):
	PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
	PROJECT = 'app'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hanuman@localhost/datta'
	SQLALCHEMY_TRACK_MODIFICATIONS= False
	SECRET_KEY = 'application_key_secret'
	DEBUG = True
	PROD = False
	TESTING = False
	SECRET_KEY = 'DEFAULT_SECRET_KEY'
	try:
		if not os.path.exists(INSTANCE_FOLDER_PATH):
			os.mkdir(INSTANCE_FOLDER_PATH)
	except Exception,e:
		raise e
class DevelopmentConfig(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hanuman@localhost/development'
	SECRET_KEY = 'application_development_key_secret'

class LocalConfig(DevelopmentConfig):
	pass

class StagingConfig(DevelopmentConfig):
	pass

class ProdConfig(DevelopmentConfig):
	DEBUG = False
	PROD = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hanuman@localhost/datta'
	SQLALCHEMY_TRACK_MODIFICATIONS= False

class TestConfig(BaseConfig):
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hanuman@localhost/test'
	#SQLALCHEMY_DATABASE_URI = ''

def load_config(MODE):
	config_mode = {'LOCAL':LocalConfig,'TESTING':TestConfig, 'DEVELOPMENT':DevelopmentConfig,'STAGING':StagingConfig,'PRODUCTION':ProdConfig}
	return config_mode[MODE]