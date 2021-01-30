from datetime import datetime, timedelta
import flask
import jwt
from flask import request
from web import app, db, ma, bcrypt
import pyhibp
from pyhibp import pwnedpasswords as pw
from cryptography.fernet import Fernet
# https://realpython.com/token-based-authentication-with-flask/
# user Class/Model
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True) # email
    password = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    note = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)    
    is_active = db.Column(db.Boolean, nullable=False)    

    def __init__(self, first_name, last_name, username, password,  created_on, updated_on, is_admin=False, note="", is_active=True):        
        self.first_name = first_name
        self.last_name = last_name
        self.username = username        
        self.password = self.hash_pwd(password)
        self.is_admin = is_admin
        self.note = note    
        self.created_on = created_on
        self.updated_on = updated_on
        self.is_active = is_active
    
    @classmethod
    def find_by_username(cls, username):
        if username:
            return cls.query.filter_by(username = username).first()
        return False
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def hash_pwd(cls, password):
        if password:
            hasPas = bcrypt.generate_password_hash(
                password, app.config.get('BCRYPT_LOG_ROUNDS')
            ).decode('utf-8')
            return hasPas
        return False
    #invoking this using User.authenticate()    
    # let's pass some username and some password 
    @classmethod    
    def authenticate(cls, username, password):
        found_user = cls.query.filter_by(username = username).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, password)
            if authenticated_user:
                return found_user
        return False
    
    def encode_auth_token(self, user_id, is_admin):        
        """Generates the Auth token, return: string"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=12000),
                'iat': datetime.utcnow(),
                'id': user_id,
                'is_admin': is_admin
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """        
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

# user Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'is_admin', 'note', 'created_on', 'updated_on', 'is_active')


# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
    
    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True  
        else:
            return False


class PMS(db.Model):
    __tablename__ = "pms"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    site_url = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))    
    note = db.Column(db.String(200))
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)    
    is_active = db.Column(db.Boolean)

    def __init__(self, user_id, site_url, username, password, note, created_on, updated_on, is_active=True):
        self.user_id = user_id
        self.site_url = site_url
        self.username = username
        self.password = password
        self.note = note        
        self.created_on = created_on                
        self.updated_on = updated_on
        self.is_active = is_active

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        if id:
            return cls.query.filter_by(id = id).first()
        return False

# pms schema
class PMSSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'site_url', 'username', 'password', 'note', 'created_on', 'updated_on', 'is_active')

pms_schema = PMSSchema()
pmss_schema = PMSSchema(many=True)


class Password(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pms_id = db.Column(db.Integer, db.ForeignKey('pms.id'))    
    password = db.Column(db.String(100))    
    note = db.Column(db.String(200))
    is_active = db.Column(db.Boolean)

    def __init__(self, user_id, pms_id, password, note="", is_active=True):
        self.user_id = user_id
        self.pms_id = pms_id
        self.password = self.encrypt_message(password)
        self.note = note        
        self.is_active = is_active

    @classmethod
    def hash_pwd(cls, password):
        if password:
            hasPas = bcrypt.generate_password_hash(
                password, app.config.get('BCRYPT_LOG_ROUNDS')
            ).decode('utf-8')
            return hasPas
        return False

    @classmethod
    def find_by_id(cls, id):
        if id:            
            return cls.query.filter_by(id = id).first()
        return False

    @staticmethod
    def is_hibp(password):
        # Required: A descriptive user agent must be set describing the application consuming
        #   the HIBP API
        pyhibp.set_user_agent(ua="PMS-Service")    
        # Check a password to see if it has been disclosed in a public breach corpus
        resp = pw.is_password_breached(password=password)
        if resp:
            #print("Password breached!")
            #print("This password was used {0} time(s) before.".format(resp))
            return True
        return False

    @classmethod
    def encrypt_message(cls, password):
        """
        Encrypts a message
        """
        key = app.config['ENCY_KEY']
        encoded_message = password.encode()        
        f = Fernet(key)
        return f.encrypt(encoded_message)        

    @staticmethod
    def decrypt_message(password):
        """
        Decrypts an encrypted message
        """
        key = app.config['ENCY_KEY']
        f = Fernet(key)
        return f.decrypt(password)   

    def save(self):
        db.session.add(self)
        db.session.commit()


# pms schema
class PasswordSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'pms_id', 'password', 'note', 'is_active')

pwd_schema = PasswordSchema()
pwds_schema = PasswordSchema(many=True)
    
    
