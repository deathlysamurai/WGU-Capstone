from ...decorators import requires_access_level
from ...models import ACCESS, UserFood
from flask_login import current_user
from flask import render_template, Blueprint

admin_user_foods = Blueprint('admin_user_foods', __name__)

@admin_user_foods.route('/', methods=['GET'])
@requires_access_level(ACCESS['admin'])
def user_foods():
    userFoods = UserFood.query.all()
    table_columns = UserFood.table_columns(self=UserFood())
    display_relationship = {}

    return render_template("admin/userFoods.html", display_relationship=display_relationship, table_columns=table_columns, user=current_user, items=userFoods, table_title="User Foods", admin_route=True, page="user foods")