import os
from .constants import INSTANCE_FOLDER_PATH

class BaseConfig(object):
	PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
	PROJECT = 'app'
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
	LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH,'logs')
	try:
		if not os.path.exists(LOG_FOLDER):
			os.mkdir(LOG_FOLDER)
	except Exception,e:
		raise e
class DevelopmentConfig(BaseConfig):
	DEBUG = True
	DATABASE_NAME = os.environ.get('DATABASE_DEVELOPMENT_NAME','')
	DATABASE_USER = os.environ.get('DATABASE_USER','')
	DATABASE_HOST = os.environ.get('DATABASE_HOST','')
	DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD','')
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+DATABASE_USER+':'+DATABASE_PASSWORD+'@'+DATABASE_HOST+'/'+DATABASE_NAME
	SQLALCHEMY_TRACK_MODIFICATIONS= False
	SECRET_KEY = 'application_development_key_secret'

class LocalConfig(BaseConfig):
	DATABASE_NAME = os.environ.get('DATABASE_LOCAL_NAME','')
	DATABASE_USER = os.environ.get('DATABASE_USER','')
	DATABASE_HOST = os.environ.get('DATABASE_HOST','')
	DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD','')
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+DATABASE_USER+':'+DATABASE_PASSWORD+'@'+DATABASE_HOST+'/'+DATABASE_NAME
	SQLALCHEMY_TRACK_MODIFICATIONS= False

class ProdConfig(DevelopmentConfig):
	DEBUG = False
	PROD = True
	DATABASE_NAME = os.environ.get('DATABASE_PRODUCTION_NAME','')
	DATABASE_USER = os.environ.get('DATABASE_USER','')
	DATABASE_HOST = os.environ.get('DATABASE_HOST','')
	DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD','')
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+DATABASE_USER+':'+DATABASE_PASSWORD+'@'+DATABASE_HOST+'/'+DATABASE_NAME
	SQLALCHEMY_TRACK_MODIFICATIONS= False

class TestConfig(BaseConfig):
	TESTING = False
	DATABASE_NAME = os.environ.get('DATABASE_TEST_NAME','')
	DATABASE_USER = os.environ.get('DATABASE_USER','')
	DATABASE_HOST = os.environ.get('DATABASE_HOST','')
	DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD','')
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+DATABASE_USER+':'+DATABASE_PASSWORD+'@'+DATABASE_HOST+'/'+DATABASE_NAME
	SQLALCHEMY_TRACK_MODIFICATIONS = False

def load_config(MODE):
	config_mode = {'LOCAL':LocalConfig,'TESTING':TestConfig, 'DEVELOPMENT':DevelopmentConfig,'PRODUCTION':ProdConfig}
	return config_mode[MODE]