from flask import Blueprint, render_template
from flask_login import login_required, current_user

meals = Blueprint('meals', __name__)

@meals.route('/meals', methods=['GET', 'POST'])
@login_required
def meals_home():     
    return render_template("meals.html", user=current_user, page="meals")