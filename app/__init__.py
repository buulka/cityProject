from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'hello'

app.debug = True

app.config['SECRET_KEY'] = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///city13.db'
app.config['SQLALCHEMY_TRASK_MODIFICATIONS'] = False

login_manager = LoginManager(app)

db = SQLAlchemy(app)

from app import routes
