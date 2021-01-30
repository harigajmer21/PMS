from flask import Blueprint, request, jsonify, redirect, url_for, session
from flask.helpers import make_response
from sqlalchemy.ext.declarative import api
from web.model.models import User, PMS, pms_schema, pmss_schema
from web import db
from flask import request
from datetime import datetime
from .helper.auth_helper import token_required
from .helper.pms_helper import pms_validation
from .helper.config_helper import dog_watch


pms = Blueprint('pms', __name__)

@pms.route('/', methods=['POST'])
@token_required(id=None)
@pms_validation
def add_credential():
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)
    data = request.get_json()        
    now = datetime.utcnow()
    if 'note' not in data:
        data['note'] = "By user "+str(resp['id'])
    try:
        new_pms = PMS(user_id=resp['id'], site_url=data['url'], username=data['username'], password=data['password'],
                        created_on=now, updated_on=now, note=data['note']
                    )
        new_pms.save()    
        return pms_schema.jsonify(new_pms)
    except Exception as e:
        print(e)
        return 'Server error'

@pms.route('/', methods=['GET'])
@token_required(id=None)
def get_all_pms():
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)
    if resp['is_admin']:            
        try:                    
            pms = PMS.query.filter_by(is_active=True).all()            
            responseObject = {
                'status': 'success',
                'data': pmss_schema.dump(pms)
            }
            return make_response(jsonify(responseObject)), 200    
        except Exception as e:
            print(e)
            return 'Server errores'           
    else: 
        try:               
            pms = PMS.query.filter_by(user_id=resp['id'], is_active=True).all()
            print(pms)
            responseObject = {
                'status': 'success',
                'message': pmss_schema.dump(pms)
            }
            return make_response(jsonify(responseObject)), 202  
        except Exception as e:
            print(e)
            return 'Server error'      

@pms.route('/<id>', methods=['GET'])
@token_required(id)
def get_pms_by_id(id):
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)
    if resp['is_admin']:
        try:            
            pms = PMS.query.filter_by(id=id, is_active=True).first()    
            return pms_schema.jsonify(pms)
        except Exception as e:
            print(e)
            return 'Server error'
    else:
        try:            
            pms = PMS.query.filter_by(id=id, user_id=resp['id'], is_active=True).first()    
            return pms_schema.jsonify(pms)
        except Exception as e:
            print(e)
            return 'Server error'        

@pms.route('/<id>', methods=['PUT'])
@token_required(id)
def update_pms(id):
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)
    try:
        data = request.get_json()

        # admin can all the data
        if resp['is_admin']:
            old_data = PMS.query.filter_by(id=id, is_active=True).first()

        else:
            old_data = PMS.query.filter_by(id=id, user_id=resp['id'], is_active=True).first()    
        
        if old_data:            
            if 'note' not in data:
                data['note'] = "Information updated by userid "+str(resp['id'])

            old_data.site_url = data['url']        
            old_data.username = data['username']
            old_data.password = data['password']
            old_data.note = data['note']        
            old_data.updated_on = datetime.utcnow()
            
            db.session.commit()

            return pms_schema.jsonify(old_data)
        return 'Data doesn\'s not exists'
    except Exception as e:
        print(e)
        return 'Server error'

@pms.route('/<id>', methods=['DELETE'])
@token_required(id)
def delete_pms(id):    
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)
    try:            
        if resp['is_admin']:
            # admin can delete any pms
            deleted_data = PMS.query.filter_by(id=id, is_active=True).first()
        else:
            deleted_data = PMS.query.filter_by(id=id, user_id=resp['id'], is_active=True).first()
        
        # if data exist
        if deleted_data:
            deleted_data.note = "PMS deactivated by {} and current status {}".format(resp['id'], resp['is_admin'])
            deleted_data.updated_on = datetime.utcnow()
            deleted_data.is_active = False        

            db.session.commit()
                
            return pms_schema.jsonify(deleted_data)    
        return 'Data doesn\'s not exists'

    except Exception as e:
        print(e)
        return 'Server error'


@pms.route('/file')
def file_check():
    print(dog_watch())
    return {"is": dog_watch()}