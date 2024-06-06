from ...decorators import requires_access_level
from ...models import ACCESS, Food, Unit, UserFood
from flask_login import current_user
from flask import render_template, Blueprint, request, redirect, url_for, flash, json
from ... import db
from sqlalchemy import func

admin_foods = Blueprint('admin_foods', __name__)

@admin_foods.route('/', methods=['GET'])
@requires_access_level(ACCESS['admin'])
def foods():
    foods = Food.query.all()
    add_columns = Food.add_columns(self=Food())
    add_columns.append("units")
    table_columns = Food.table_columns(self=Food())
    table_columns.append("Unit Options")
    display_units = {}
    for food in foods:
        display_units[food.id] = ''
        for i in range(len(food.units)):
            display_units[food.id] = food.units[i].name if display_units[food.id] == '' else display_units[food.id] + ", " + food.units[i].name
    unit_options = {}
    units = Unit.query.all()
    for unit in units:
        unit_options[unit.name] = unit.id

    return render_template("admin/foods.html", display_units=display_units, select_options=unit_options, json_select_options=json.dumps(unit_options), table_columns=table_columns, add_columns=add_columns, user=current_user, items=foods, table_title="Foods", admin_route=True, page="foods")

@admin_foods.route('/add-food', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def add_food():
    if request.method == 'POST':
        name = request.form.get('name')
        units = request.form.getlist('units')

        food_name = Food.query.filter(func.lower(Food.name) == name.lower()).first()

        if food_name:
            flash('Food already exists', category='error')
        else:
            add_units = []
            for i in range(len(units)):
                add_unit = Unit.query.get(units[i])
                if add_unit:
                    add_units.append(add_unit)
            food = Food(name=name, units=add_units)
            db.session.add(food)
            db.session.commit()
            flash('Food created.', category='success')

    return redirect(url_for("admin_foods.foods"))

@admin_foods.route('/delete-foods', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def delete_foods():
    if request.method == 'POST':
        foodIDs = json.loads(request.form.get('delete-items'))
        for foodID in foodIDs:
            food = Food.query.get_or_404(foodID)
            db.session.delete(food)

        try:
            db.session.commit()
            flash("Foods deleted successfully.", category='success')
        except:
            flash("Problem deleting foods.", category='error')

    return redirect(url_for("admin_foods.foods"))

@admin_foods.route('/update-foods', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def update_foods():
    if request.method == 'POST':
        successful_foods = 0
        update_foods = json.loads(request.form.get('update-items'))
        for update_food in update_foods:
            for i in range(len(update_food['Unit Options'])):
                update_food['Unit Options'][i] = int(update_food['Unit Options'][i])
            food = Food.query.get_or_404(update_food['id'])
            name = update_food['name'] if food.name != update_food['name'] else None
            units = update_food['Unit Options'] if food.units != update_food['Unit Options'] else None
            print(update_food['Unit Options'])
            if name and name != '':
                food.name = update_food['name']
            if units:
                for unit in food.units:
                    if unit.id not in update_food['Unit Options']:
                        food.units.remove(unit)
                    else:
                        update_food['Unit Options'].remove(unit.id)
                for i in range(len(update_food['Unit Options'])):
                    food.units.append(Unit.query.get(update_food['Unit Options'][i]))
                print(food.units)
            if units or (name and name != ''):
                db.session.commit()
                successful_foods += 1
        
        if(successful_foods > 0):
            flash(str(successful_foods)+" foods updated successfully.", category="success")  

    return redirect(url_for("admin_foods.foods"))