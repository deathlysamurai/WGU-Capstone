from flask import Blueprint, render_template, request, flash, redirect, url_for, json
from flask_login import login_required, current_user
from ..models import Food, User, UserFood, Unit
from .. import db
from sqlalchemy import func
from datetime import date

pantry = Blueprint('pantry', __name__)

@pantry.route('/', methods=['GET', 'POST'])
@login_required
def pantry_home(): 
    userFoods = UserFood.query.filter_by(user_id=current_user.id).all()
    foods = []
    for userFood in userFoods:
        new_food = {}
        unit = Unit.query.filter_by(id=userFood.unit).first()
        new_food["id"] = userFood.id
        new_food["name"] = Food.query.get(userFood.food_id).name
        new_food["amount"] = userFood.amount
        new_food["unit"] = unit.name if unit else None
        new_food["expiration"] = userFood.expiration
        foods.append(new_food)
    add_columns = Food.add_columns(self=Food())
    for col in UserFood.pantry_add_columns(self=UserFood()):
        add_columns.append(col)
    table_columns = Food.table_columns(self=Food())
    for col in UserFood.pantry_add_columns(self=UserFood()):
        table_columns.append(col)
    unit_options = {}
    units = Unit.query.all()
    for unit in units:
        unit_options[unit.name] = unit.id

    return render_template("pantry.html", select_options=unit_options, json_select_options=json.dumps(unit_options), table_columns=table_columns, add_columns=add_columns, user=current_user, items=foods, table_title="Foods", page="pantry")

@pantry.route('/add-food', methods=['POST'])
@login_required
def add_food():
    if request.method == 'POST':
        name = request.form.get('name')
        amount = request.form.get('amount')
        unit_name = request.form.get('unit')
        expiration_form = request.form.get('expiration')

        exp_split = expiration_form.split('-')
        year = int(exp_split[0])
        month = int(exp_split[1])
        day = int(exp_split[2])
        expiration = date(year, month, day)

        if int(amount) <= 0:
            flash('Amount must be greater than 0.', category='error')
        else:
            unit = Unit.query.filter(func.lower(Unit.name) == unit_name.lower()).first()
            if not unit:
                unit = Unit(name=unit_name, abbreviation=unit_name)
                db.session.add(unit)
                db.session.commit()
            food = Food.query.filter(func.lower(Food.name) == name.lower()).first()
            if not food:
                units = [unit]
                food = Food(name=name, units=units)
                db.session.add(food)
                db.session.commit()
            pantry = UserFood(user_id=current_user.id, food_id=food.id, amount=amount, unit=unit.id, expiration=expiration)
            db.session.add(pantry)
            db.session.commit()
            flash('Pantry item created.', category='success')

    return redirect(url_for("pantry.pantry_home"))

@pantry.route('/delete-foods', methods=['POST'])
@login_required
def delete_foods():
    if request.method == 'POST':
        userFoodIDs = json.loads(request.form.get('delete-items'))
        for userFoodID in userFoodIDs:
            userFood = UserFood.query.get_or_404(userFoodID)
            db.session.delete(userFood)

        try:
            db.session.commit()
            flash("Pantry items deleted successfully.", category='success')
        except:
            flash("Problem deleting pantry items.", category='error')

    return redirect(url_for("pantry.pantry_home"))

@pantry.route('/update-foods', methods=['POST'])
@login_required
def update_foods():
    if request.method == 'POST':
        successful_foods = 0
        update_foods = json.loads(request.form.get('update-items'))
        for update_food in update_foods:
            userFood = UserFood.query.get_or_404(update_food['id'])
            amount = update_food['amount'] if userFood.amount != update_food['amount'] else None
            unit = update_food['unit'] if userFood.unit != update_food['unit'] else None
            exp_split = update_food['expiration'].split('-')
            year = int(exp_split[0])
            month = int(exp_split[1])
            day = int(exp_split[2])
            expiration = date(year, month, day)
            expiration = expiration if userFood.expiration != expiration else None
            if amount and int(amount) > 0:
                userFood.amount = update_food['amount']
            if unit:
                unit = Unit.query.get(unit)
                if unit:
                    userFood.unit = unit.id
            if expiration:
                userFood.expiration = expiration
            if (amount and int(amount) > 0) or unit or expiration:
                db.session.commit()
                successful_foods += 1
        
        if(successful_foods > 0):
            flash(str(successful_foods)+" foods updated successfully.", category="success")  

    return redirect(url_for("pantry.pantry_home"))