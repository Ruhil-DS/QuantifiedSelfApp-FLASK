from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Application.database import db

# Creating the flask app variable
app = Flask(__name__)

# Initialising the DB using SQLAlchemy, pushing content to the app
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.sqlite3'
db.init_app(app)
app.app_context().push()

# Importing the code from the Application module which contains all the necessary code!

from Application.controller_index import *
from Application.controller_dash import *

# Running the app
app.run(debug=True)
