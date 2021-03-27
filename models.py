
from flask_login import UserMixin
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///city4.db'
app.config['SQLALCHEMY_TRASK_MODIFICATIONS'] = False

login_manager = LoginManager(app)

db = SQLAlchemy(app)

from app import routes


class Company(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False, unique=True)
    company_password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    events = db.relationship('Event', backref='сompany', lazy='dynamic')


@login_manager.user_loader
def load_company(company_id):
    return Company.query.get(company_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    user_age = db.Column(db.Integer, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.Integer, nullable=False, unique=True)
    event_date = db.Column(db.String, nullable=False)
    event_address = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    tag = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    vacancy = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('соmpany.id'))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)