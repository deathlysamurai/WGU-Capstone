from flask import Blueprint, render_template
from flask_login import current_user

general = Blueprint('general', __name__)

@general.route('/home', methods=['GET', 'POST'])
def home():     
    return render_template("home.html", user=current_user, page="home")