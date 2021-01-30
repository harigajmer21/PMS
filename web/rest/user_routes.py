from flask import Blueprint, json, request, jsonify, redirect, url_for, session
from flask.helpers import make_response
from sqlalchemy.ext.declarative import api
from web.model.models import User, user_schema, users_schema
from web import db
from flask import request
from datetime import datetime
from .helper.auth_helper import token_required
from .helper.config_helper import dog_watch, UsernameValidation, PasswordValidation
import json

user = Blueprint('user', __name__)

@user.route('/', methods=['POST'])
def add_user():    
    data = request.get_json()    
    user = User.find_by_username(data['username']) 
    # check if username exists then return to login url
    if not user:         

        # Checking required fields
        required = ['first_name', 'last_name', 'username', 'password']
        if not all(field in data for field in required):
            return 'Missing values', 400

        # validation based on constrain file
        usernameValid = UsernameValidation(data['username'])
        passwordValid = PasswordValidation(data['password'])
        passwordValid.check_all()
        usernameValid.check_all()            
        notice = {}
        if any(usernameValid.error_msg.values()) or any(usernameValid.error_msg.values()):
            notice['status'] = 'Fail'
            notice['username'] = usernameValid.error_msg
            notice['password'] = passwordValid.error_msg
            return make_response(jsonify(notice)), 401

        # default note = "" 
        if 'note' not in data:
            data['note'] = ""
            
        now = datetime.utcnow()

        new_user = User(first_name=data['first_name'], last_name=data['last_name'], username=data['username'],
                        password=data['password'].encode('utf-8'), note=data['note'], created_on=now, updated_on=now)
            
        try:
            new_user.save()               
            # generate auth token
            # generate the auth token            
            auth_token = new_user.encode_auth_token(new_user.id, new_user.is_admin)
            print(type(auth_token))
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(responseObject)), 201
            # return user_schema.jsonify(new_user)
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202

# showing all users to only authorized request
# @sc.is_admin
@user.route('/', methods=['GET'])
@token_required(id=None)
def get_users():
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)         
    try:
        if resp['is_admin']:            
            users = User.query.filter_by(is_active=True).all()
            responseObject = {
                'status': 'success',
                'data': users_schema.dump(users)
            }
        else:
            user = User.query.filter_by(id=resp['id'], is_active=True).first()
            responseObject = {
                'status': 'success',
                'message': user_schema.dump(user)
            }            
        return make_response(jsonify(responseObject)), 200    
    except Exception as e:
        return 'Server errores'           
    
# Get single user
# only is_admin can see this url
@user.route('/<id>', methods=['GET'])
@token_required(id)
def get_user(id): 
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)
    if resp['is_admin']:
        try:            
            user = User.query.filter_by(id=id, is_active=True).first()    
            return user_schema.jsonify(user)
        except Exception as e:
            print(e)
            return 'Server error'
    else:
        return 'No access right'
            
    
# update user
# is_admin or 
# update only logged in user data
@user.route('/<id>', methods=['PUT'])
@token_required(id)
def update_user(id):    
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)
    try:
        data = request.get_json()
        # Checking required fields
        required = ['first_name', 'last_name', 'username', 'password']
        if not all(field in data for field in required):
            return 'Missing values', 400
        
        usernameValid = UsernameValidation(data['username'])
        passwordValid = PasswordValidation(data['password'])
        passwordValid.check_all()
        usernameValid.check_all()            
        notice = {}
        if any(usernameValid.error_msg.values()) or any(usernameValid.error_msg.values()):
            notice['status'] = 'Fail'
            notice['username'] = usernameValid.error_msg
            notice['password'] = passwordValid.error_msg
            return make_response(jsonify(notice)), 401

        if resp['is_admin']:
            old_data = User.query.filter_by(id=id, is_active=True).first()
        else:
            old_data = User.query.filter_by(id=resp['id'], is_active=True).first()
        
        # if data exists:
        if old_data:
            # default note = "" 
            if 'note' not in data:
                data['note'] = "Information updated by userid "+str(resp['id'])

            old_data.first_name = data['first_name']
            old_data.last_name = data['last_name']
            old_data.username = data['username']
            old_data.password = User.hash_pwd(data['password'])
            old_data.note = data['note']        
            old_data.updated_on = datetime.utcnow()
            
            db.session.commit()

            return user_schema.jsonify(old_data)
        return 'return Data doesn\'s not exists'
    except Exception as e:
        print(e)
        return 'error'

# Delete user or deactivate user
# is_admin or 
# update only logged in user data
@user.route('/<id>', methods=['DELETE'])
@token_required(id)
def delete_product(id):
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)    
    try:            
        if resp['is_admin']:
            # admin can delete any user
            deleted_data = User.query.filter_by(id=id, is_active=True).first()
        else:
            deleted_data = User.query.filter_by(id=resp['id'], is_active=True).first()
        
        # if data exist
        if deleted_data:
            deleted_data.note = "PMS deactivated by {} and current status {}".format(resp['id'], resp['is_admin'])
            deleted_data.updated_on = datetime.utcnow()
            deleted_data.is_active = False        

            db.session.commit()
                
            return user_schema.jsonify(deleted_data)    
        return 'Data doesn\'s not exists'
        
    except Exception as e:
        print(e)
        return 'Server error'

@user.route('/file')
def file_check():
    username = "asfL"
    valid = UsernameValidation(username)
    valid.check_all()
    print(type(valid.last_update()))
    return {"is": dog_watch(), "error": valid.error_msg}