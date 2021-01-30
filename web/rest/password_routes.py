from hashlib import new
from flask import Blueprint, request, jsonify, redirect, url_for, session
from flask.helpers import make_response
from sqlalchemy.ext.declarative import api
from web.model.models import User, PMS, Password, pwd_schema, pwds_schema
from web import db
from flask import request
from datetime import datetime
from .helper.auth_helper import token_required
from .helper.config_helper import dog_watch, PasswordValidation
import json
from .helper.pms_helper import pms_validation

pwd = Blueprint('pwd', __name__)

@pwd.route('/', methods=['POST'])
@token_required(id=None)
def add_password():
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)
    data = request.get_json()

    try:
        if PMS.find_by_id(data['pms_id']):
            if not Password.is_hibp(password=data['password']):
                passwordValid = PasswordValidation(data['password'])
                passwordValid.check_all()                

                if any(passwordValid.error_msg.values()):           
                    return make_response(jsonify(passwordValid.error_msg)), 406                
                
                new_pwd = Password(user_id=resp['id'], pms_id=data['pms_id'], password=data['password'])
                new_pwd.save()
                return pwd_schema.jsonify(new_pwd), 201
            else:
                return make_response(jsonify("Password is not secure, by HIBP database")), 406
        else:
            responseObject = {
                'status': 'Fail',
                'message': 'PMS don\'t exists.',                
            }
            return make_response(jsonify(responseObject)), 200 
    except Exception as e:
        print(e)
        return 'Server error'

@pwd.route('/get', methods=['POST'])
@token_required(id=None)
def get_password():
    data = request.get_json()
    try:        
        if PMS.find_by_id(data['pms_id']):            
            result = Password.find_by_id(data['id'])            
        
            password = Password.decrypt_message(result.password)            
            return pwd_schema.jsonify({'password': password.decode()}), 200
        else:
            responseObject = {
                'status': 'Fail',
                'message': 'PMS don\'t exists.',                
            }
            return make_response(jsonify(responseObject)), 200 
    except Exception as e:      
        print(e)  
        return 'Server error'


@pwd.route('/update', methods=['PUT'])
@token_required(id=None)
def update_password():
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)
    data = request.get_json()

    try:
        if PMS.find_by_id(data['pms_id']):
            if not Password.is_hibp(password=data['password']):
                passwordValid = PasswordValidation(data['password'])
                passwordValid.check_all()                

                if any(passwordValid.error_msg.values()):           
                    return make_response(jsonify(passwordValid.error_msg)), 406                
                
                old_data = Password.query.filter_by(id=data['id'], user_id=resp['id'], pms_id=data['pms_id'],  is_active=True).first()
                old_data.password = Password.encrypt_message(data['password'])
                old_data.note = ""#f"Updated by user id: {resp['id']}"                
                
                db.session.commit()

                return pwd_schema.jsonify(old_data)
            else:
                return make_response(jsonify("Password is not secure, by HIBP database")), 406
        else:
            responseObject = {
                'status': 'Fail',
                'message': 'PMS don\'t exists.',                
            }
            return make_response(jsonify(responseObject)), 200 
    except Exception as e:
        print(e)
        return 'Server error'