import unittest
from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.database_initialize import Users

class AppTestCase(unittest.TestCase):

	def setUp(self):
		self.app = create_app('TESTING')
		self.app_context = self.app.app_context()
		self.app_context.push()
		#self.app.login_manager.init_app(self.app)
		db.create_all()
		self.init_data()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()
	def init_data(self):

		testAdminUser = Users(username = 'testadmin', isAdmin = 1)
		testAdminUser.hash_password('password')
		db.session.add(testAdminUser)
		db.session.commit()
		self.test_adminUser = testAdminUser
		testuser = Users(username = 'testuser', isAdmin = 0)
		testuser.hash_password('password')
		db.session.add(testuser)
		db.session.commit()
		self.test_user = testuser
