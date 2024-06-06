from functools import wraps
from flask import url_for, redirect, flash
from .models import User
from flask_login import current_user

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                print("USER HAS NOT LOGGED IN YET!")
                flash('Please Login.', category='error')
                return redirect(url_for('auth.login'))

            user = User.query.get(current_user.id)
            if not user.allowed(access_level):
                flash('Higher access required.', category='error')
                return redirect(url_for('general.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator