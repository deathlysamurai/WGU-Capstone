from ...decorators import requires_access_level
from ...models import ACCESS, User
from flask import render_template, request, flash, redirect, url_for, json, Blueprint
from flask_login import current_user
from werkzeug.security import generate_password_hash
from ..auth import user_valid
from ... import db
from sqlalchemy import func

admin_users = Blueprint('admin_users', __name__)

def get_users():
    users = User.query.all()
    for user in users:
        user.access = list(ACCESS.keys())[list(ACCESS.values()).index(user.access)]

    return users

@admin_users.route('/', methods=['GET'])
@requires_access_level(ACCESS['admin'])
def users():
    users = get_users()
    add_columns = User.add_columns(self=User())
    table_columns = User.table_columns(self=User())

    return render_template("admin/users.html", table_columns=table_columns, add_columns=add_columns, user=current_user, items=users, table_title="Users", admin_route=True, page="users", select_options=ACCESS, json_select_options=json.dumps(ACCESS), clickable=True)

@admin_users.route('/add-user', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        access = request.form.get("access")

        if access.isdigit():
            access = int(access)

        if access not in ACCESS.values():
            access = 0

        user_username = User.query.filter(func.lower(User.username) == username.lower()).first()
        user_email = User.query.filter_by(func.lower(User.email) == email.lower()).first()

        if user_username:
            flash('Username already exists', category='error')
        elif len(username) < 3:
            flash('Username must be greater than 2 characters', category='error')
        elif user_email:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            user = User(username=username, email=email, password=generate_password_hash(password), access=access)
            db.session.add(user)
            db.session.commit()
            flash('Account created.', category='success')

    return redirect(url_for("admin_users.users"))

@admin_users.route('/delete-users', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def delete_users():
    if request.method == 'POST':
        userIDs = json.loads(request.form.get('delete-items'))
        for userID in userIDs:
            user = User.query.get_or_404(userID)
            db.session.delete(user)

        try:
            db.session.commit()
            flash("Users deleted successfully.", category='success')
        except:
            flash("Problem deleting users.", category='error')

    return redirect(url_for("admin_users.users"))

@admin_users.route('/update-users', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def update_users():
    if request.method == 'POST':
        successful_users = 0
        update_users = json.loads(request.form.get('update-items'))
        for update_user in update_users:
            user = User.query.get_or_404(update_user['id'])
            username = update_user['username'] if user.username != update_user['username'] else None
            email = update_user['email'] if user.email != update_user['email'] else None
            if user_valid(username, email):
                user.email = update_user['email']
                user.username = update_user['username']
                user.access = update_user['access']
                db.session.commit()
                successful_users += 1
        
        if(successful_users > 0):
            flash(str(successful_users)+" users updated successfully.", category="success")  

    return redirect(url_for("admin_users.users"))