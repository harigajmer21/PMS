from flask import request, jsonify
import jwt
from web.model.models import BlacklistToken
from web import app
from functools import wraps
import os 
def token_required(id):
    def decorated(func):
        @wraps(func)
        def inner (*args, **kwargs):                        
            try: 
                
                auth_token = request.headers.get('Authorization')
                if auth_token != os.getenv(' ') and auth_token != None:
                    try:
                        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
                        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
                        if is_blacklisted_token:
                            return 'Token blacklisted. Please log in again.'
                        else:
                            return func(*args, **kwargs)
                    except jwt.ExpiredSignatureError:
                        return 'Signature expired. Please log in again.'
                    except jwt.InvalidTokenError:
                        return 'Invalid token. Please log in again.'
                else:
                    return 'Token required'
            except Exception as e:
                print(e)
                return 'An error occured'           
        return inner
    return decorated

