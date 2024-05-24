from flask import Blueprint, render_template
from flask_login import login_required, current_user

general = Blueprint('general', __name__)

@general.route('/home', methods=['GET', 'POST'])
@login_required
def home():     
    return render_template("home.html", user=current_user, page="home")