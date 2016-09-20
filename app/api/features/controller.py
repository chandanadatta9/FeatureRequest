from flask import Flask, flash, redirect, session, url_for, request, render_template,jsonify, Blueprint, current_app
from flask_login import login_user,logout_user, current_user, login_required, LoginManager
from ...extensions import db, ma, login_manager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ...database_initialize import Users,Clients, Projects, Requests
import base64
from ...common.schemas import request_schema,requests_schema,requesting_schema,client_schema, clients_schema, project_schema, projects_schema

features = Blueprint('features', __name__ , url_prefix = '/api')
@features.route('/request/<int:requestID>', methods = ['GET'])
@login_required
def get_request(requestID):
	if request.method == 'GET':
		#user = current_user    ### these two commented lines check if the current user is admin or not
		#if user.isAdmin
		requestGiven = Requests.query.filter(Requests.requestID == requestID).first_or_404()
		return requesting_schema.jsonify(requestGiven)

@features.route('/request', methods = ['GET','POST','PUT'])
@login_required
def requestProcess():
	if request.method == 'GET':
		requests = Requests.query.all()
		resp = jsonify(requests_schema.dump(requests))
		resp.status_code = 201
		return resp
	elif request.method == 'POST':
		if request.json.get('clientname') is not None and db.session.query(Requests).filter(Requests.clientname == request.json.get('clientname')).first() :
			priorities = db.session.query(Requests).filter(Requests.clientname == request.json.get('clientname')).filter(Requests.clientPriority >= request.json.get('clientPriority'))
			currentPriorities = []
			idsForPriorities = []
			currentPrioritiesSorted = []
			idsForPrioritiesSorted = []
			for priority in priorities:
				currentPriorities.append(priority.clientPriority)
				idsForPriorities.append(priority.requestID)
			currentPrioritiesSorted = [currentPrioritiesTemp for currentPrioritiesTemp, idsForPrioritiesTemp in sorted(zip(currentPriorities,idsForPriorities))]
			idsForPrioritiesSorted = [idsForPrioritiesTemp for currentPrioritiesTemp,idsForPrioritiesTemp in sorted(zip(currentPriorities,idsForPriorities))]
			hasInserted = 0
			newClientPriority = 0
			newPriorityRequested = request.json.get('clientPriority')
			if len(currentPriorities) == 0:
				requestValues, errors = request_schema.load(request.get_json())
				if errors:
					current_app.logger.info('error occured while creating the request ')
					resp = jsonify(errors)
					resp.status_code = 400
					return resp
				db.session.add(requestValues)
				db.session.flush()
				requestValues.ticketURL = url_for('features.get_request', requestID = requestValues.requestID)
				db.session.add(requestValues)
				db.session.commit()
				
				resp = jsonify({"message":"Request Created",
								"requestID":requestValues.requestID,
								"requestURL":requestValues.ticketURL})
				#location = url_for("get_request", requestID = requestValues.requestId)
				#resp.headers["Location"] = location
				resp.status_code = 201
				return resp
			else:
				resp = jsonify({})
				for i in range(0,len(currentPrioritiesSorted)):
					if newPriorityRequested == currentPrioritiesSorted[i]:
						newClientPriority = currentPrioritiesSorted[i] + 1
						updateRequest = db.session.query(Requests).filter(Requests.requestID == idsForPrioritiesSorted[i]).first()
						updateRequest.clientPriority = newClientPriority
						db.session.add(updateRequest)
						db.session.commit()
						if hasInserted == 0:
							requestValues, errors = request_schema.load(request.get_json())
							if errors:
								current_app.logger.info('error occured while creating the request ' )
								resp = jsonify(errors)
								resp.status_code = 400
								return resp
							db.session.add(requestValues)
							db.session.flush()
							requestValues.ticketURL = url_for('features.get_request',requestID = requestValues.requestID)
							db.session.add(requestValues)
							db.session.commit()
							resp = jsonify({"message":"Request Created",
											"requestID":requestValues.requestID,
											"requestURL":requestValues.ticketURL})
							resp.status_code = 201
							hasInserted = 1
						newPriorityRequested = newClientPriority
					elif newPriorityRequested < currentPrioritiesSorted[i]:
						if hasInserted == 0:
							requestValues, errors = request_schema.load(request.get_json())
							if errors:
								current_app.logger.info('error occured while creating the request ' )
								resp = jsonify(errors)
								resp.status_code = 400
								return resp
							db.session.add(requestValues)
							db.session.flush()
							requestValues.ticketURL = url_for('features.get_request',requestID = requestValues.requestID)
							db.session.add(requestValues)
							db.session.commit()
							resp = jsonify({"message":"Request Created",
											"requestID":requestValues.requestID,
											"requestURL":requestValues.ticketURL})
							resp.status_code = 201
							hasInserted = 1
						else:
							pass
					elif newPriorityRequested > currentPrioritiesSorted[i]:
						if i == len(currentPrioritiesSorted):
							if hasInserted == 0:
								requestValues, errors = request_schema.load(request.get_json())
								if errors:
									current_app.logger.info('error occured while creating the request ' )
									resp = jsonify(errors)
									resp.status_code = 400
									return resp
								db.session.add(requestValues)
								db.session.flush()
								requestValues.ticketURL = url_for('features.get_request',requestId = requestValues.requestID)
								db.session.add(requestValues)
								db.session.commit()
								resp = jsonify({"message":"Request Created",
												"requestID":requestValues.requestID,
												"requestURL":requestValues.ticketURL})
								resp.status_code = 201
								hasInserted = 1
						else:
							pass
				
				#resp = jsonify({"message":"Request Created"})
				#resp.status_code = 201
				#location = url_for("get_request", requestID = requestValues.requestId)
				#resp.headers["Location"] = location
				return resp
		else:
			requestValues, errors = request_schema.load(request.get_json())
			if errors:
				current_app.logger.info('error occured while creating the request')
				resp = jsonify(errors)
				resp.status_code = 400
				return resp
			db.session.add(requestValues)
			db.session.flush()
			requestValues.ticketURL = url_for('features.get_request', requestID = requestValues.requestID)
			db.session.add(requestValues)
			db.session.commit()
			resp = jsonify({"message":"Request Created",
							"requestID":requestValues.requestID,
							"requestURL":requestValues.ticketURL})
			#location = url_for("get_request", requestID = requestValues.requestId)
			#resp.headers["Location"] = location
			resp.status_code = 201
			return resp