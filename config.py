import os

# Flask settings
FLASK_DEBUG = True

# SQLAlchemy settings
SQLALCHEMY_DB_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = True


# SECRET KEY
# import os os.urandom(24)
# KEY = "\xb5\x9a\x80b\xbaC(\x0b\x82\xbd)\xfe\xe0\xb6\x7f\x83AI\xda\\\xda\x0f\xcf\x0c"
# stored in environment variable
SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
