from ...decorators import requires_access_level
from ...models import ACCESS, Meal, Food, MealFood
from flask_login import current_user
from flask import render_template, Blueprint, request, redirect, url_for, flash, json
from ... import db
from sqlalchemy import func

admin_meals = Blueprint('admin_meals', __name__)

@admin_meals.route('/', methods=['GET'])
@requires_access_level(ACCESS['admin'])
def meals():
    meals = Meal.query.all()
    add_columns = Meal.add_columns(self=Meal())
    create_columns = add_columns[:]
    create_columns.append("foods")
    table_columns = Meal.table_columns(self=Meal())
    table_columns.append("Foods")
    display_relationship = {}
    for meal in meals:
        display_relationship[meal.id] = ''
        for i in range(len(meal.foods)):
            display_relationship[meal.id] = meal.foods[i].name if display_relationship[meal.id] == '' else display_relationship[meal.id] + ", " + meal.foods[i].name
    all_meals = Meal.query.all()
    meal_options = {}
    for meal in all_meals:
        meal_options[meal.name] = meal.id
    food_options = {}
    foods = Food.query.all()
    for food in foods:
        food_options[food.name] = food.id
    all_foods = []
    for food in foods:
        new_food = {}
        units = []
        for unit in food.units:
            units.append({"id":unit.id, "name":unit.name})
        new_food["id"] = food.id
        new_food["name"] = food.name
        new_food["units"] = units
        all_foods.append(new_food)

    return render_template("admin/meals.html", all_foods=json.dumps(all_foods), food_options=food_options, create_columns=create_columns, select_options=meal_options, json_select_options=json.dumps(meal_options), display_relationship=display_relationship, table_columns=table_columns, add_columns=add_columns, user=current_user, items=meals, table_title="Meals", admin_route=True, page="meals")

# @admin_meals.route('/add-meal', methods=['POST'])
# @requires_access_level(ACCESS['admin'])
# def add_meal():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         foods = request.form.getlist('foods')

#         meal_name = Meal.query.filter(func.lower(Meal.name) == name.lower()).first()

#         if meal_name:
#             flash('Meal already exists', category='error')
#         else:
#             add_foods = []
#             for i in range(len(foods)):
#                 add_food = Food.query.get(foods[i])
#                 if add_food:
#                     add_foods.append(add_food)
#             meal = Meal(name=name, foods=add_foods)
#             db.session.add(meal)
#             db.session.commit()
#             flash('Meal created.', category='success')

#     return redirect(url_for("admin_meals.meals"))

@admin_meals.route('/delete-meals', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def delete_meals():
    if request.method == 'POST':
        mealIDs = json.loads(request.form.get('delete-items'))
        for mealID in mealIDs:
            meal = Meal.query.get_or_404(mealID)
            db.session.delete(meal)

        try:
            db.session.commit()
            flash("Meals deleted successfully.", category='success')
        except:
            flash("Problem deleting meals.", category='error')

    return redirect(url_for("admin_meals.meals"))

@admin_meals.route('/update-meals', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def update_meals():
    if request.method == 'POST':
        successful_meals = 0
        update_meals = json.loads(request.form.get('update-items'))
        for update_meal in update_meals:
            for i in range(len(update_meal['Foods'])):
                update_meal['Foods'][i] = int(update_meal['Foods'][i])
            meal = Meal.query.get_or_404(update_meal['id'])
            name = update_meal['name'] if meal.name != update_meal['name'] else None
            foods = True if meal.foods != update_meal['Foods'] else None
            if name and name != '':
                meal.name = update_meal['name']
            if foods:
                for food in meal.foods[:]:
                    if food.id not in update_meal['Foods']:
                        meal.foods.remove(food)
                    else:
                        update_meal['Foods'].remove(food.id)
                for i in range(len(update_meal['Foods'])):
                    meal.foods.append(Food.query.get(update_meal['Foods'][i]))
            if foods or (name and name != ''):
                db.session.commit()
                successful_meals += 1
        
        if(successful_meals > 0):
            flash(str(successful_meals)+" meals updated successfully.", category="success")  

    return redirect(url_for("admin_meals.meals"))

@admin_meals.route('/create-meal', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def create_meal():
    if request.method == 'POST':
        name = request.form.get('name')
        foods = json.loads(request.form.get('chosenFoods'))
        
        for food in foods:
            if int(food["amount"]) <= 0:
                flash('Amount must be greater than 0.', category='error')
                return redirect(url_for("admin_meals.meals"))
            
        meal = Meal.query.filter(func.lower(Meal.name) == name.lower()).first()
        if meal:
            flash('Meal already exists.', category='error')
        else:
            new_meal = Meal(name=name)
            db.session.add(new_meal)
            db.session.commit()
            for food in foods:
                meal_food = MealFood(meal_id=new_meal.id, food_id=food["id"], amount=food["amount"], unit=food["unit"])
                db.session.add(meal_food)
                db.session.commit()
            flash('Meal created.', category='success')

    return redirect(url_for("admin_meals.meals"))

@admin_meals.route('/<meal_name>', methods=['GET'])
@requires_access_level(ACCESS['admin'])
def meal_page(meal_name):
    meal = Meal.query.filter(func.lower(Meal.name) == meal_name.lower()).first()
    foods = []
    meal_foods = MealFood.query.filter_by(meal_id=meal.id)
    foodIDs = []
    for meal_food in meal_foods:
        new_food = {}
        if meal_food.amount > 0:
            food = Food.query.filter_by(id=meal_food.food_id).first()
            units = []
            for unit in food.units: 
                units.append({"id": unit.id, "name": unit.name})
            foodIDs.append(food.id)
            new_food["id"] = food.id
            new_food["name"] = food.name
            new_food["unit"] = meal_food.unit
            new_food["units"] = units
            new_food["unitsJSON"] = json.dumps(units)
            new_food["amount"] = meal_food.amount
            foods.append(new_food)    
    foods_select = Food.query.all()
    all_foods = []
    for food in foods_select:
        if food.id not in foodIDs:
            new_food = {}
            units = []
            for unit in food.units: 
                units.append({"id": unit.id, "name": unit.name})
            new_food["id"] = food.id
            new_food["name"] = food.name
            new_food["units"] = units
            new_food["unitsJSON"] = json.dumps(units)
            all_foods.append(new_food)

    return render_template("admin/meal.html", admin_route=True, all_foods=all_foods, foodsJSON=json.dumps(foods), foods=foods, meal=meal, user=current_user)

@admin_meals.route('/update-meal', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def update_meal():
    if request.method == 'POST':
        update_meal = request.get_json()
        meal = Meal.query.filter_by(name=update_meal["meal_name"]).first()
        update_foods = []
        foodIDs = []
        for food in update_meal["foods"]:
            foodIDs.append(food["id"])
            update_foods.append(Food.query.get(food["id"]))
        for food in meal.foods[:]:
            if food.id not in foodIDs:
                meal.foods.remove(food)
            else:
                meal_food = MealFood.query.filter_by(meal_id=meal.id, food_id=food.id).first()
                meal_food_check = [update_food for update_food in update_meal['foods'] if update_food["id"] == food.id][0]
                if meal_food.amount != meal_food_check["amount"]: meal_food.amount = meal_food_check["amount"]
                if meal_food.unit != meal_food_check["unit"]: meal_food.unit = meal_food_check["unit"]
                update_meal['foods'] = [update_food for update_food in update_meal['foods'] if update_food["id"] != food.id]
        for food in update_meal['foods']:
            meal_food = MealFood(meal_id=meal.id, food_id=food["id"], amount=food["amount"], unit=food["unit"])
            db.session.add(meal_food)
        db.session.commit()

    return {}, 201, {'Content-Type': 'application/json'}