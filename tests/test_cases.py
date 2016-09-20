from tests import AppTestCase
import unittest
from flask import jsonify, json
import sys
import base64
import json
class TestCases(AppTestCase):
	def test_adminUserRegister(self):
		with self.app.test_request_context('/api/user/',
				method = 'POST',
				data = json.dumps({'username':'adminUser1', 'password':'password', 'isAdmin':1, 'method':'register'}), 
				headers = {'Content-Type':'application/json'}):
			res = self.app.full_dispatch_request()
			json_res = json.loads(res.data)
			self.assertEquals(json_res['message'], 'user created')

	def test_userRegister(self):
		with self.app.test_request_context('/api/user/',
				method = 'POST',
				data = json.dumps({'username':'user1', 'password':'password', 'isAdmin':0, 'method':'register'}), 
				headers = {'Content-Type':'application/json'}):
			res = self.app.full_dispatch_request()
			json_res = json.loads(res.data)
			self.assertEquals(res.status_code, 201)

	def test_adminUserLogin(self):
		with self.app.test_request_context('/api/user/',
				method = 'POST',
				data = json.dumps({'username':self.test_adminUser.username, 'password':'password','method':'login'}), 
				headers = {'Content-Type':'application/json'}):
			res = self.app.full_dispatch_request()
			json_res = json.loads(res.data)
			self.assertEquals(json_res['isAdmin'], 1)

	def test_userLogin(self):
		with self.app.test_request_context('/api/user/',
				method = 'POST',
				data = json.dumps({'username':self.test_user.username, 'password':'password','method':'login'}), 
				headers = {'Content-Type':'application/json'}):
			res = self.app.full_dispatch_request()
			json_res = json.loads(res.data)
			self.assertEquals(json_res['isAuthenticated'], 1)
			self.assertEquals(res.status_code, 200)

	def test_WrongUserLogin(self):
		with self.app.test_request_context('/api/user/',
				method = 'POST',
				data = json.dumps({'username':self.test_user.username, 'password':'password1', 'isAdmin':self.test_user.isAdmin, 'method':'login'}), 
				headers = {'Content-Type':'application/json',
							'Authorization':'Basic '+base64.b64encode(self.test_user.username+':'+'password')}):
			res = self.app.full_dispatch_request()
			json_res = json.loads(res.data)
			print json_res
			self.assertEquals(json_res['isAuthenticated'], 0)
			self.assertEquals(res.status_code, 400)

	#the below test case will check if the new Feature Requests are being inserted into the table
	#and also will check if the client priorities are being reordered correctly based on the new request priority
	#this will also check if all of the requests are being retrieved correctly to display to the user
	def test_featureRequestCreate(self):
		ticketURLCreated = ''
		with self.app.test_request_context('/api/user/',
				method = 'POST',
				data = json.dumps({'username':self.test_user.username, 'password':'password','isAdmin':self.test_user.isAdmin,'method':'register'}), 
				headers = {'Content-Type':'application/json'}):
			res = self.app.full_dispatch_request()
		with self.app.test_request_context('/api/request', 
				method = 'POST', 
				data = json.dumps({'requestTitle':'request 1', 'clientPriority':1, 'clientname':'client A', 'productArea':'project 1'}),
				headers = {'Content-Type':'application/json',
							'Authorization':'Basic '+base64.b64encode(self.test_user.username+':'+'password')}):
			res = self.app.full_dispatch_request()
			json_res = json.loads(res.data)
		with self.app.test_request_context('/api/request', 
				method = 'POST', 
				data = json.dumps({'requestTitle':'request 2', 'clientPriority':2, 'clientname':'client A', 'productArea':'project 1'}),
				headers = {'Content-Type':'application/json',
							'Authorization':'Basic '+base64.b64encode(self.test_user.username+':'+'password')}):
			res = self.app.full_dispatch_request()
			json_res = json.loads(res.data)
			print json_res
			ticketURLCreated = json_res['requestURL']
		with self.app.test_request_context('/api/request', 
				method = 'POST', 
				data = json.dumps({'requestTitle':'request 3', 'clientPriority':2, 'clientname':'client A', 'productArea':'project 1'}),
				headers = {'Content-Type':'application/json',
							'Authorization':'Basic '+base64.b64encode(self.test_user.username+':'+'password')}):
			res = self.app.full_dispatch_request()
			json_res = json.loads(res.data)
		with self.app.test_request_context(ticketURLCreated, 
				method = 'GET', 
				data = json.dumps({'requestTitle':'request 2', 'clientPriority':2, 'clientname':'client A', 'productArea':'project 1'}),
				headers = {'Content-Type':'application/json',
							'Authorization':'Basic '+base64.b64encode(self.test_user.username+':'+'password')}):
			res = self.app.full_dispatch_request()
			json_res = json.loads(res.data)
			self.assertEquals(json_res['clientPriority'],3)
		with self.app.test_request_context('/api/request', 
				method = 'GET', 
				data = json.dumps({'requestTitle':'request 2', 'clientPriority':2, 'clientname':'client A', 'productArea':'project 1'}),
				headers = {'Content-Type':'application/json',
							'Authorization':'Basic '+base64.b64encode(self.test_user.username+':'+'password')}):
			res = self.app.full_dispatch_request()
			json_res = json.loads(res.data)
			self.assertEquals(len(json_res[0]),3)

	def test_projectCreate(self):
		with self.app.test_request_context('/api/user/',
				method = 'POST',
				data = json.dumps({'username':self.test_adminUser.username, 'password':'password','isAdmin':self.test_adminUser.isAdmin,'method':'register'}), 
				headers = {'Content-Type':'application/json'}):
			res = self.app.full_dispatch_request()
		with self.app.test_request_context('/api/admin/project',
				method = 'POST',
				data = json.dumps({'projectname':'project A'}),
				headers = {'Content-Type':'application/json',
							'Authorization':'Basic '+base64.b64encode(self.test_adminUser.username+':'+'password')}):
			res = self.app.full_dispatch_request()
			self.assertEquals(res.status_code,201)
		with self.app.test_request_context('/api/admin/project',
				method = 'GET',
				data = json.dumps({'projectname':'project A'}),
				headers = {'Content-Type':'application/json',
							'Authorization':'Basic '+base64.b64encode(self.test_adminUser.username+':'+'password')}):
			res = self.app.full_dispatch_request()
			json_res = json.loads(res.data)
			print json_res
			self.assertEquals(json_res[0][0]['projectname'],'project A')
#if __name__ == '__main__':
#	unittest.main()