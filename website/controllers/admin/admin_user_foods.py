from ...decorators import requires_access_level
from ...models import ACCESS, Food, Unit, UserFood
from flask_login import current_user
from flask import render_template, Blueprint, json

admin_user_foods = Blueprint('admin_user_foods', __name__)

@admin_user_foods.route('/', methods=['GET'])
@requires_access_level(ACCESS['admin'])
def user_foods():
    userFoods = UserFood.query.all()
    table_columns = UserFood.table_columns(self=UserFood())
    display_units = {}
    # for userFood in userFoods:
    #     display_units[food.id] = ''
    #     for i in range(len(food.units)):
    #         display_units[food.id] = food.units[i].name if display_units[food.id] == '' else display_units[food.id] + ", " + food.units[i].name
    # unit_options = {}
    # units = Unit.query.all()
    # for unit in units:
    #     unit_options[unit.name] = unit.id

    return render_template("admin/foods.html", display_units=display_units, table_columns=table_columns, user=current_user, items=userFoods, table_title="User Foods", admin_route=True, page="user foods")