from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from flask import render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash

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

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста заполните все поля!')
        elif password != password2:
            flash('Пароли не совпадают!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, user_age=int(user_age))

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('user_auth.html')

