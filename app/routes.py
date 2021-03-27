from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from flask import render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import re
from models import User, Company, Event, Order


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/user_auth', methods=['GET', 'POST'])
def user_auth():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    user_age = request.form.get('user_age')
    user_email = request.form.get('user_email')

    pattern = r"^[a-zA-Z0-9]{1,100}[@][a-z]{2,6}\.[a-z]{2,4}"
    email_re = re.compile(pattern)

    if request.method == 'POST':
        if not (login or password or password2 or user_age or user_email):
            flash('Пожалуйста заполните все поля!')
        elif password != password2:
            flash('Пароли не совпадают!')
        elif not email_re.findall(user_email):
            flash('Неверный формат Email')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, user_age=int(user_age), user_email=user_email)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('user_auth.html')


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Логин или пароль некорректны')
    else:
        flash('Пожалуйста, заполните поля "Логин" и "Пароль"')

    return render_template('user_login.html')


@app.route('/company_auth', methods=['GET', 'POST'])
def company_auth():
    company_name = request.form.get('company_name')
    company_password = request.form.get('company_password')
    company_password2 = request.form.get('company_password2')
    email = request.form.get('email')

    pattern = r"^[a-zA-Z0-9]{1,100}[@][a-z]{2,6}\.[a-z]{2,4}"
    email_re = re.compile(pattern)

    if request.method == 'POST':
        if not (company_name or company_password or company_password2 or email):
            flash('Пожалуйста заполните все поля!')
        elif company_password != company_password2:
            flash('Пароли не совпадают!')
        elif not email_re.findall(email):
            flash('Неверный формат Email')
        else:
            company_hash_pwd = generate_password_hash(company_password)
            new_company = Company(company_name=company_name, company_password=company_hash_pwd, email=email)

            db.session.add(new_company)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('company_auth.html')


@app.route('/company_login', methods=['GET', 'POST'])
def company_login():
    comp_login = request.form.get('comp_login')
    comp_password = request.form.get('comp_password')

    if comp_login and comp_password:
        company = Company.query.filter_by(company_name=comp_login).first()
        if company and check_password_hash(company.company_password, comp_password):
            login_user(company)
            return redirect(url_for('index'))
        else:
            flash('Логин или пароль некорректны')
    else:
        flash('Пожалуйста, заполните поля "Логин" и "Пароль"')

    return render_template('company_login.html')