from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from flask import render_template, request, redirect, flash, url_for, session
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

            return redirect(url_for('user_login'))

    return render_template('user_auth.html')


@app.route('/company_auth', methods=['GET', 'POST'])
def company_auth():
    company_name = request.form.get('company_name')
    company_password = request.form.get('company_password')
    company_password2 = request.form.get('company_password2')
    email = request.form.get('email')
    description = request.form.get('description')

    pattern = r"^[a-zA-Z0-9]{1,100}[@][a-z]{2,6}\.[a-z]{2,4}"
    email_re = re.compile(pattern)

    if request.method == 'POST':
        if not (company_name or company_password or company_password2 or email or description):
            flash('Пожалуйста заполните все поля!')
        elif company_password != company_password2:
            flash('Пароли не совпадают!')
        elif not email_re.findall(email):
            flash('Неверный формат Email')
        else:
            company_hash_pwd = generate_password_hash(company_password)
            new_company = Company(company_name=company_name, company_password=company_hash_pwd, email=email, description=description)

            db.session.add(new_company)
            db.session.commit()

            return redirect(url_for('company_login'))

    return render_template('company_auth.html')


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('user_profile'))
        else:
            flash('Логин или пароль некорректны')
    else:
        flash('Пожалуйста, заполните поля "Логин" и "Пароль"')

    return render_template('user_login.html')


@app.route('/company_login', methods=['GET', 'POST'])
def company_login():
    comp_login = request.form.get('comp_login')
    comp_password = request.form.get('comp_password')

    if comp_login and comp_password:
        company = Company.query.filter_by(company_name=comp_login).first()
        if company and check_password_hash(company.company_password, comp_password):
            session['id'] = company.id
            login_user(company)
            return redirect(url_for('company_profile'))
        else:
            flash('Логин или пароль некорректны')
    else:
        flash('Пожалуйста, заполните поля "Логин" и "Пароль"')

    return render_template('company_login.html')


@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    event_name = request.form.get('event_name')
    event_date = request.form.get('event_date')
    event_address = request.form.get('event_address')
    capacity = request.form.get('capacity')
    tag = request.form.get('tag')
    age = request.form.get('age')
    info = request.form.get('info')

    company_event = Company.query.filter_by(id=session['id']).first()
    email_event = company_event.email
    if request.method == 'POST':
        if not (event_name or event_date or event_address or tag or capacity or age or info):
            flash('Пожалуйста заполните все поля!')
        else:
            new_event = Event(event_name=event_name, event_date=event_date, event_address=event_address, info=info, tag=tag, capacity=capacity, vacancy=capacity, age=int(age), event_email=email_event, company_id=session['id'])
            db.session.add(new_event)
            db.session.commit()
            # return redirect(url_for('company_profile'))
            company_events = Event.query.filter_by(company_id=session['id']).all()
            company = Company.query.filter_by(id=session['id']).first()
            return render_template('company_profile.html', user=session['id'], data=company_events, company_name=company.company_name)

    return render_template('add_event.html')


@app.route('/company_profile', methods=['GET', 'POST'])
def company_profile():
    company_events = Event.query.filter_by(company_id=session['id']).all()
    company = Company.query.filter_by(id=session['id']).first()
    return render_template('company_profile.html', data=company_events, user=session['id'], company_name=company.company_name)


@app.route('/delete_event/<event_id>')
def event_id(event_id):
    Event.query.filter_by(id=event_id).delete()
    Order.query.filter_by(event_id=event_id).delete()
    db.session.commit()
    return redirect(url_for('company_profile'))


@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    return render_template('user_profile.html')


@app.route('/show/<tag>',  methods=['GET', 'POST'])
def show(tag):
    b = []
    tag_event = Event.query.filter_by(tag=tag).all()
    for i in tag_event:
        if current_user.user_age >= i.age:
            b.append(i)
    return render_template('user_profile.html', data=b)


@app.route('/enroll/<event_idd>', methods=['GET', 'POST'])
def enroll(event_idd):
    new_order = Order(event_id=event_idd, user_id=current_user.id)
    db.session.add(new_order)

    # count = Event.query.filter_by(id=event_idd).first()
    # vac_new = Event.query.filter_by(id=event_idd).update({'vacancy': count.vacancy - 1})
    db.session.commit()

    return redirect(url_for('user_profile'))


@app.route('/user_events', methods=['GET', 'POST'])
def user_events():
    a = []
    user_events = Order.query.filter_by(user_id=current_user.id).all()
    for i in user_events:
        event = Event.query.filter_by(id=i.event_id).first()
        a.append(event)

    return render_template('user_events.html', data=a)


@app.route('/unsubscribe/<event_id>', methods=['GET', 'POST'])
def unsubscribe(event_id):
    del_event = Order.query.filter_by(event_id=event_id).delete()
    count = Event.query.filter_by(id=event_id).first().vacancy
    vac_new = Event.query.filter_by(id=event_id).update({'vacancy': count + 1})
    db.session.commit()

    return redirect(url_for('user_events'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))
