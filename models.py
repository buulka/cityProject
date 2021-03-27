from app import login_manager, db
import config

from flask_login import UserMixin


class Company(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False, unique=True)
    company_password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    description = db.Column(db.String(255), nullable=False)


@login_manager.user_loader
def load_user(u_id):
    return Company.query.get(u_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String, nullable=False, unique=True)
    event_date = db.Column(db.String, nullable=False)
    event_address = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    tag = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    vacancy = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    company_id = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)