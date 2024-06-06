from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..models import User
from .. import db
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

auth = Blueprint('auth', __name__)

def user_valid(username, email, password1 = None, password2 = None):
    username_check = User.query.filter(func.lower(User.username) == username.lower()).first() if username is not None else None
    email_check = User.query.filter(func.lower(User.email) == email.lower()).first() if email is not None else None

    if username_check:
        flash('Username ('+username+') already exists', category='error')
        return False
    elif username is not None and len(username) < 3:
        flash('Username must be greater than 2 characters', category='error')
        return False
    elif email_check:
        flash('Email ('+email+') already exists', category='error')
        return False
    elif email is not None and len(email) < 4:
        flash('Email must be greater than 3 characters.', category='error')
        return False
    elif password1 is not None and len(password1) < 7:
        flash('Password must be at least 7 characters.', category='error')
        return False
    elif password1 is not None and password1 != password2:
        flash('Passwords don\'t match.', category='error')
        return False
    else:
        return True

@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("CURRENT USER IS AUTHENTICATED")
        return redirect(url_for('general.home'))

    if request.method == 'POST':
        email_username = request.form.get("email-username")
        password = request.form.get('password')

        user = User.query.filter(func.lower(User.email) == email_username.lower()).first()
        if not user:
            user = User.query.filter(func.lower(User.username) == email_username.lower()).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                next = request.args.get('next')
                url = next if next else url_for('general.home')
                return redirect(url)
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email/Username does not exist', category='error')
            print('Not Found')

    return render_template("login.html", user=current_user, page="login")

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if user_valid(username, email, password1, password2):
            #add user to database
            user = User(username=username, email=email, password=generate_password_hash(password1))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created.', category='success')
            next = request.args.get('next')
            url = next if next else url_for('general.home')
            return redirect(url)

    return render_template("sign_up.html", user=current_user, page="sign_up")