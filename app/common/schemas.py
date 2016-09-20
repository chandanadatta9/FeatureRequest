
#Marshmallow integration
from ..database_initialize import Users, Clients, Projects, Requests
from ..extensions import ma

class UsersSchema(ma.ModelSchema):
	class Meta:
		model = Users
		#fields('isAuthenticated','isAdmin')
	#@pre_dump
	#def authentication(self, data):


class ClientsSchema(ma.ModelSchema):
	class Meta:
		model = Clients
		exclude = ['clientid']

class ProjectsSchema(ma.ModelSchema):
	class Meta:
		model = Projects

class RequestsSchema(ma.ModelSchema):
	class Meta:
		model = Requests

class RequestingSchema(ma.ModelSchema):
	class Meta:
		model = Requests
		exclude = ["requestID","ticketURL"]

user_schema = UsersSchema()
users_schema = UsersSchema(many = True)

client_schema = ClientsSchema()
clients_schema = ClientsSchema(many= True)

project_schema = ProjectsSchema()
projects_schema = ProjectsSchema(many = True)

request_schema = RequestsSchema()
requesting_schema = RequestingSchema()
requests_schema = RequestsSchema(many = True)