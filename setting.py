# importing libraries
from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
# creating an instance of the flask app
app = Flask(__name__)
#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pmsproject.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initializing our database
db = SQLAlchemy(app)

