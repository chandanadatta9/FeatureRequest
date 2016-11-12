from flask import Flask, flash, redirect, session, url_for, request, render_template,jsonify, Blueprint
from flask_login import login_user,logout_user, current_user, login_required, LoginManager
from ...extensions import db, ma, login_manager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ...database_initialize import Users,Clients, Projects, Requests
import base64
from ...common.schemas import request_schema,requests_schema,requesting_schema,client_schema, clients_schema, project_schema, projects_schema

admin = Blueprint('admin',__name__, url_prefix = '/api/admin')

@admin.route('/request/<int:requestID>', methods = ['PUT'])
@login_required
def update_request(requestID):
	if request.method == 'PUT':
		if (request.json.get('clientPriority') is not None):
			print "******************************"
			print Requests.requestID
			requestUpdate = db.session.query(Requests).filter(Requests.requestID == requestID).first()
			print requestUpdate.clientname
			priorities = db.session.query(Requests).filter(Requests.clientname == requestUpdate.clientname)
			currentPriorities = []
			idsForPriorities = []
			currentPrioritiesSorted = []
			idsForPrioritiesSorted = []
			for priority in priorities:
				currentPriorities.append(priority.clientPriority)
				idsForPriorities.append(priority.requestID)
			currentPrioritiesSorted = [currentPrioritiesTemp for currentPrioritiesTemp, idsForPrioritiesTemp in sorted(zip(currentPriorities,idsForPriorities))]
			idsForPrioritiesSorted = [idsForPrioritiesTemp for currentPrioritiesTemp,idsForPrioritiesTemp in sorted(zip(currentPriorities,idsForPriorities))]
			print currentPrioritiesSorted
			print idsForPrioritiesSorted
			hasInserted = 0
			newClientPriority = 0
			newPriorityRequested = request.json.get('clientPriority')
			if len(currentPriorities) == 0:
				requestUpdate, errors = request_schema.load(request.get_json(),instance = requestUpdate)
				if errors:
					resp = jsonify(errors)
					resp.status_code = 400
					return resp
				db.session.add(requestUpdate)
				db.session.commit()
				resp = jsonify({"message":"updated"})
				resp.status_code = 200
				return resp
			else:
				resp = jsonify({})
				for i in range(0,len(currentPrioritiesSorted)):
					if (idsForPrioritiesSorted[i] == requestUpdate.requestID):
						continue
					if newPriorityRequested == currentPrioritiesSorted[i]:
						print 'entered this loop'
						newClientPriority = currentPrioritiesSorted[i] + 1
						updateRequest = db.session.query(Requests).filter(Requests.requestID == idsForPrioritiesSorted[i]).first()
						updateRequest.clientPriority = newClientPriority
						db.session.add(updateRequest)
						db.session.commit()
						
						if hasInserted == 0:
							#requestUpdate, errors = request_schema.load(request.get_json(),instance = requestUpdate)
							#if errors:
							#	resp = jsonify(errors)
							#	resp.status_code = 400
							#	return resp
							if request.json.get('requestTitle') is not None:
								requestUpdate.requestTitle = request.json.get('requestTitle')
							if request.json.get('requestDescription') is not None:
								requestUpdate.requestDescription = request.json.get('requestDescription')
							if request.json.get('clientname') is not None:
								requestUpdate.clientname = request.json.get('clientname')
							if request.json.get('clientPriority') is not None:
								requestUpdate.clientPriority = request.json.get('clientPriority')
							if request.json.get('requestDate') is not None:
								requestUpdate.requestDate = request.json.get('requestDate')
							if request.json.get('targetDate')  is not None:
								requestUpdate.targetDate = request.json.get('targetDate')
							if request.json.get('productArea') is not None:
								requestUpdate.productArea = request.json.get('productArea')
							db.session.add(requestUpdate)
							db.session.commit()
							resp = jsonify({"message":"updated"})
							resp.status_code = 200
							hasInserted = 1
						newPriorityRequested = newClientPriority
					elif newPriorityRequested < currentPrioritiesSorted[i]:
						if hasInserted == 0:
							
							if request.json.get('requestTitle') is not None:
								requestUpdate.requestTitle = request.json.get('requestTitle')
							if request.json.get('requestDescription') is not None:
								requestUpdate.requestDescription = request.json.get('requestDescription')
							if request.json.get('clientname') is not None:
								requestUpdate.clientname = request.json.get('clientname')
							if request.json.get('clientPriority') is not None:
								requestUpdate.clientPriority = request.json.get('clientPriority')
							if request.json.get('requestDate') is not None:
								requestUpdate.requestDate = request.json.get('requestDate')
							if request.json.get('targetDate')  is not None:
								requestUpdate.targetDate = request.json.get('targetDate')
							if request.json.get('productArea') is not None:
								requestUpdate.productArea = request.json.get('productArea')
							db.session.add(requestUpdate)
							db.session.commit()
							resp = jsonify({"message":"updated"})
							resp.status_code = 200
							hasInserted = 1
						else:
							pass
					elif newPriorityRequested > currentPrioritiesSorted[i]:
						if i == len(currentPrioritiesSorted):
							if hasInserted == 0:
								
								if request.json.get('requestTitle') is not None:
									requestUpdate.requestTitle = request.json.get('requestTitle')
								if request.json.get('requestDescription') is not None:
									requestUpdate.requestDescription = request.json.get('requestDescription')
								if request.json.get('clientname') is not None:
									requestUpdate.clientname = request.json.get('clientname')
								if request.json.get('clientPriority') is not None:
									requestUpdate.clientPriority = request.json.get('clientPriority')
								if request.json.get('requestDate') is not None:
									requestUpdate.requestDate = request.json.get('requestDate')
								if request.json.get('targetDate')  is not None:
									requestUpdate.targetDate = request.json.get('targetDate')
								if request.json.get('productArea') is not None:
									requestUpdate.productArea = request.json.get('productArea')
								db.session.add(requestUpdate)
								db.session.commit()
								resp = jsonify({"message":"updated"})
								resp.status_code = 200
								hasInserted = 1
						else:
							pass
				
				#resp = jsonify({"message":"Request Created"})
				#resp.status_code = 201
				#location = url_for("get_request", requestID = requestValues.requestId)
				#resp.headers["Location"] = location
				return resp
				#db.session.close()
				#session.bind.dispose()
		else:
			print "okay in this loop"
			requestUpdate = db.session.query(Requests).filter(Requests.requestID == requestID).first()
			
			if request.json.get('requestTitle') is not None:
				requestUpdate.requestTitle = request.json.get('requestTitle')
			if request.json.get('requestDescription') is not None:
				requestUpdate.requestDescription = request.json.get('requestDescription')
			if request.json.get('clientname') is not None:
				requestUpdate.clientname = request.json.get('clientname')
			if request.json.get('clientPriority') is not None:
				requestUpdate.clientPriority = request.json.get('clientPriority')
			if request.json.get('requestDate') is not None:
				requestUpdate.requestDate = request.json.get('requestDate')
			if request.json.get('targetDate')  is not None:
				requestUpdate.targetDate = request.json.get('targetDate')
			if request.json.get('productArea') is not None:
				requestUpdate.productArea = request.json.get('productArea')
			db.session.add(requestUpdate)
			db.session.commit()
			resp = jsonify({"message":"updated"})
			return resp

@admin.route('/project/<string:projectName>', methods = ['GET','POST','PUT'])
@login_required
def get_project(projectName):
	if request.method == 'GET':
		projectGiven = Projects.query.filter(Projects.projectname == projectName).first_or_404()
		return project_schema.jsonify(projectGiven)
	elif request.method == 'PUT':
		projectUpdate = db.session.query(Projects).filter(Projects.projectname == projectName).first()
		# projectUpdate, errors = project_schema.load(request.get_json(), instance = projectUpdate)
		# if errors:
		# 	resp = jsonify(errors)
		# 	resp.status_code = 400
		# 	return resp
		if request.json.get('projectname') is not None:
			projectUpdate.projectname = request.json.get('projectname')
		db.session.add(projectUpdate)
		db.session.commit()
		resp = jsonify({"message":"updated"})
		return resp

@admin.route('/client/<string:clientName>',methods = ['GET','POST','PUT'])
@login_required
def get_client(clientName):
	if request.method == 'GET':
		clientGiven = Clients.query.filter(Clients.clientname == clientName).first_or_404()
		return client_schema.jsonify(clientGiven)
	elif request.method == 'PUT':
		
		clientUpdate = db.session.query(Clients).filter(Clients.clientname == clientName).first()
		# clientUpdate, errors = client_schema.load(request.get_json(), instance = clientUpdate)
		# if errors:
		# 	resp = jsonify(errors)
		# 	resp.status_code = 400
		# 	return resp
		if request.json.get('clientname') is not None:
			clientUpdate.clientname = request.json.get('clientname')
		if request.json.get('email') is not None:
			clientUpdate.email = request.json.get('email')
		db.session.add(clientUpdate)
		db.session.commit()

		resp = jsonify({"message":"updated"})
		return resp

@admin.route('/project', methods = ['GET','POST','PUT'])
@login_required
def projectProcess():
	if request.method == 'GET':
		projects = Projects.query.all()
		return jsonify(projects_schema.dump(projects))
	elif request.method == 'POST':
		projectValues, errors = project_schema.load(request.get_json())
		if errors:
			resp = jsonify(errors)
			resp.status_code = 400
			return resp
		db.session.add(projectValues)
		db.session.commit()
		resp = jsonify({"message":"Project created"})
		resp.status_code = 201
		return resp

@admin.route('/client', methods = ['GET','POST','PUT'])
@login_required
def clientProcess():
	if request.method == 'GET':
		clients = Clients.query.all()
		return jsonify(clients_schema.dump(clients))

	elif request.method == 'POST':
		clientValues,errors = client_schema.load(request.get_json())
		if errors:
			resp = jsonify(errors)
			resp.status_code = 400
			return resp
		db.session.add(clientValues)
		db.session.commit()
		resp = jsonify({"message":"Client created"})
		resp.status_code = 201
		return resp

