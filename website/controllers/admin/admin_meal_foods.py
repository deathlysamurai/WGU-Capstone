from ...decorators import requires_access_level
from ...models import ACCESS,MealFood
from flask_login import current_user
from flask import render_template, Blueprint

admin_meal_foods = Blueprint('admin_meal_foods', __name__)

@admin_meal_foods.route('/', methods=['GET'])
@requires_access_level(ACCESS['admin'])
def meal_foods():
    mealFoods = MealFood.query.all()
    table_columns = MealFood.table_columns(self=MealFood())
    display_relationship = {}

    return render_template("admin/mealFoods.html", display_relationship=display_relationship, table_columns=table_columns, user=current_user, items=mealFoods, table_title="Meal Foods", admin_route=True, page="meal foods")