from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from datetime import datetime
import pathlib
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname('__file__'))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SECRET_KEY'] = "\xb5\x9a\x80b\xbaC(\x0b\x82\xbd)\xfe\xe0\xb6\x7f\x83AI\xda\\\xda\x0f\xcf\x0c"

# db Init
db = SQLAlchemy(app)
# ma Init
ma = Marshmallow(app)
# bcrypt Init
bcrypt = Bcrypt(app)
# login required
login = LoginManager(app)


# user api register
from web.rest.user_routes import user
app.register_blueprint(user, url_prefix='/user')

# auth api register
from web.rest.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

# pms api register
from web.rest.pms_routes import pms
app.register_blueprint(pms, url_prefix='/pms')

# site register
from web.site.routes import site
app.register_blueprint(site, url_prefix='/')

app.config['CONF_FILE'] = os.path.join(basedir, 'constrain.json')
# watch file modification
def get_hashed():
    from hashlib import md5    
    initial_hasher = md5()            
    with open(app.config['CONF_FILE'], 'rb') as f:        
        buf = f.read()
        initial_hasher.update(buf)
        initial_hashed = initial_hasher.hexdigest()

    return initial_hashed

app.config['INIT_HASH_FILE'] = get_hashed()

# CONFIG FILE Modified datetime
file_name = pathlib.Path(app.config['CONF_FILE'])
app.config['CONF_MODIFIED_ON'] = datetime.fromtimestamp(file_name.stat().st_mtime)

# use python script to create databasee
# python from pms dir
# from web import db
# db.drop_all()
# db.create_all()