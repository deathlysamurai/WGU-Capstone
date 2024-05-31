from flask import Blueprint, render_template
from flask_login import login_required, current_user

pantry = Blueprint('pantry', __name__)

@pantry.route('/pantry', methods=['GET', 'POST'])
@login_required
def pantry_home():     
    return render_template("pantry.html", user=current_user, page="pantry")