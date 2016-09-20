import os


class BaseConfig(object):
	PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
	PROJECT = 'app'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hanuman@localhost/datta'
	SQLALCHEMY_TRACK_MODIFICATIONS= False
	SECRET_KEY = 'application_key_secret'
	DEBUG = True
	TESTING = False

class DevelopmentConfig(BaseConfig):
	DEBUG = True

	SECRET_KEY = 'application_development_key_secret'

class LocalConfig(DevelopmentConfig):
	pass

class StagingConfig(DevelopmentConfig):
	pass

class ProdConfig(DevelopmentConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hanuman@localhost/datta'
	SQLALCHEMY_TRACK_MODIFICATIONS= False

class TestConfig(BaseConfig):
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hanuman@localhost/test'
	#SQLALCHEMY_DATABASE_URI = ''

def load_config(MODE):
	config_mode = {'LOCAL':LocalConfig,'TESTING':TestConfig, 'DEVELOPMENT':DevelopmentConfig,'STAGING':StagingConfig,'PRODUCTION':ProdConfig}
	return config_mode[MODE]