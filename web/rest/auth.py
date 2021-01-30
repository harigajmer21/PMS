from flask import Blueprint, request, jsonify,  redirect, url_for, session
from flask.helpers import make_response
from web.model.models import User, user_schema, users_schema, BlacklistToken
from .helper.auth_helper import token_required
from .helper.config_helper import PasswordValidation, UsernameValidation, dog_watch
from web import db, bcrypt
from flask import request


# from .SessionCheck import is_authenticated

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['POST'])
def index():
    return redirect(url_for('auth.login'))
    # return 'click here to login'
    
@auth.route('/login', methods=['POST'])
def login():
    credientials = request.get_json()
    username = credientials['username']
    password = credientials['password']            
    
    try:
        user = User.authenticate(username, password)
        # check if the user actually exists
        if not user:
            responseObject = {
                'status': 'authentication failed',
                'message': 'username or password don\'t match.',                
            }
            return make_response(jsonify(responseObject)), 200        
        auth_token = user.encode_auth_token(user.id, user.is_admin)
        print(password)
        if auth_token:
            # check if any credition config has been changes respect to update_on
            usernameValid = UsernameValidation(username)
            passwordValid = PasswordValidation(password)
            passwordValid.check_all()
            usernameValid.check_all()            
                         
            if not dog_watch() or (user.updated_on > usernameValid.last_update()):
                notice = {}                                   
                if any(usernameValid.error_msg.values()):
                    notice['username'] = usernameValid.error_msg
                if any(passwordValid.error_msg.values()):
                    notice['password'] = passwordValid.error_msg
                
                responseObject = {       
                    'status': 'success',                 
                    'message': 'Successfully logged in. but',
                    'auth_token': auth_token.decode(),
                    'config_file_modified': dog_watch(),
                    'update_info': notice
                }
                
                return make_response(jsonify(responseObject)), 200

                
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token.decode()
            }        
            return make_response(jsonify(responseObject)), 200
    except Exception as e:
        print(e)  
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500

@auth.route('/check', methods=['POST'])
@token_required(id=None)
def check():
    auth_token = request.headers.get('Authorization')    
    resp = User.decode_auth_token(auth_token)    
    try:
        if isinstance(resp['id'], int):            
            user = User.query.filter_by(id=resp['id'], is_active=True).first()
            responseObject = {
                'status': 'success',
                'id': user.id,
                'first_name': user.first_name,
                'username': user.username
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401
    except Exception as e:
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401            

@auth.route('/logout' , methods=['POST'])
@token_required(id=None)
def logout():             
    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)
    print(type(resp['id']))
    if isinstance(resp['id'], int):
        # mark the token as blacklisted        
        try:
            blacklist_token = BlacklistToken(token=auth_token)
            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': e
            }
            return make_response(jsonify(responseObject)), 200        
    else:
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401    

@auth.route('/refresh', methods=['POST'])
@token_required(id=None)
def refresh():
    # Extend the time us jwt in user_routes: get_user/s, update
    # It takes time so 
    # Work on PMS part > Login > CRUD credientials

    auth_token = request.headers.get('Authorization')
    resp = User.decode_auth_token(auth_token)

    responseObject = {
        'status': 'success',
        'message': resp
    }
    return make_response(jsonify(responseObject)), 200

