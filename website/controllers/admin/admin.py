from flask import render_template, Blueprint
from ...models import ACCESS
from ...decorators import requires_access_level
from flask_login import current_user

admin = Blueprint('admin', __name__)

@admin.route('/', methods=['GET'])
@requires_access_level(ACCESS['admin'])
def home():

    return render_template("admin/home.html", user=current_user, admin_route=True, page="admin_home")