from flask import Blueprint, render_template
from flask_login import login_required, current_user

shopping = Blueprint('shopping', __name__)

@shopping.route('/shopping', methods=['GET', 'POST'])
@login_required
def shopping_home():     
    return render_template("shopping.html", user=current_user, page="shopping")