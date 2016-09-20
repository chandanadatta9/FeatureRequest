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
		requestUpdate = db.session.query(Requests).filter(Requests.requestID == requestID).first()
		requestUpdate, errors = request_schema.load(request.get_json(),instance = requestUpdate)
		if errors:
			resp = jsonify(errors)
			resp.status_code = 400
			return resp
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
		projectUpdate, errors = project_schema.load(request.get_json(), instance = projectUpdate)
		if errors:
			resp = jsonify(errors)
			resp.status_code = 400
			return resp
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
		clientUpdate, errors = client_schema.load(request.get_json(), instance = clientUpdate)
		if errors:
			resp = jsonify(errors)
			resp.status_code = 400
			return resp
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

