from flask import Blueprint, render_template, request, flash, redirect, url_for, json, make_response
from flask_login import login_required, current_user
from ..models import Meal, UserMeal, Food, MealFood, MealEdit, UserFood
from .. import db
from sqlalchemy import func
from datetime import date
import calendar
from .shopping import add_shopping_item, update_shopping_items

meals = Blueprint('meals', __name__)

@meals.route('/', methods=['GET', 'POST'])
@login_required
def meals_home(): 
    userMeals = UserMeal.query.filter_by(user_id=current_user.id).all()
    meals = []
    for userMeal in userMeals:
        new_meal = {}
        meal = Meal.query.filter_by(id=userMeal.meal_id).first()
        new_meal["id"] = userMeal.id
        new_meal["name"] = meal.name
        meals.append(new_meal)
    add_columns = Meal.add_columns(self=Meal())
    create_columns = add_columns[:]
    create_columns.append("foods")
    table_columns = Meal.table_columns(self=Meal())
    all_meals = Meal.query.all()
    meal_options = {}
    for meal in all_meals:
        meal_options[meal.name] = meal.id
    open_meal_modal = request.cookies.get("open_meal_modal")
    new_meal_name = request.cookies.get("new_meal_name")
    foods = Food.query.all()
    food_options = {}
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
    today = date.today().weekday()
    weekly_meals = []
    days = []
    for day in range(7):
        day_name = calendar.day_name[day]
        meal = Meal.query.get(getattr(current_user, day_name[:3].lower()+"Meal"))
        weekly_meals.append(meal)
        days.append(day_name)

    resp = make_response(render_template("meals.html", days=days, weekly_meals=weekly_meals, today=today, all_foods=json.dumps(all_foods), create_columns=create_columns, food_options=food_options, new_meal_name=new_meal_name, open_meal_modal=open_meal_modal, select_options=meal_options, json_select_options=json.dumps(meal_options), table_columns=table_columns, add_columns=add_columns, user=current_user, items=meals, table_title="Meals", page="meals"))
    resp.set_cookie("open_meal_modal", "", expires=0)
    resp.set_cookie("new_meal_name", "", expires=0)
    return resp

@meals.route('/add-meal', methods=['POST'])
@login_required
def add_meal():
    if request.method == 'POST':
        name = request.form.get('name')

        meal = Meal.query.filter(func.lower(Meal.name) == name.lower()).first()

        if not meal:
            new_route = redirect(url_for("meals.meals_home"))
            new_route.set_cookie("open_meal_modal", "true")
            new_route.set_cookie("new_meal_name", name)
            return new_route
        else:
            user_meal = UserMeal(user_id=current_user.id, meal_id=meal.id)
            db.session.add(user_meal)
            db.session.commit()
            flash('Meal item added.', category='success')

    return redirect(url_for("meals.meals_home"))

@meals.route('/delete-meals', methods=['POST'])
@login_required
def delete_meals():
    if request.method == 'POST':
        userMealIDs = json.loads(request.form.get('delete-items'))
        for userMealID in userMealIDs:
            userMeal = UserMeal.query.get_or_404(userMealID)
            db.session.delete(userMeal)

        try:
            db.session.commit()
            flash("Meal items deleted successfully.", category='success')
        except:
            flash("Problem deleting meal items.", category='error')

    return redirect(url_for("meals.meals_home"))

@meals.route('/create-meal', methods=['POST'])
@login_required
def create_meal():
    if request.method == 'POST':
        name = request.form.get('name')
        foods = json.loads(request.form.get('chosenFoods'))
        
        for food in foods:
            if int(food["amount"]) <= 0:
                flash('Amount must be greater than 0.', category='error')
                return redirect(url_for("meals.meals_home"))
            
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
            user_meal = UserMeal(user_id=current_user.id, meal_id=new_meal.id)
            db.session.add(user_meal)
            db.session.commit()
            flash('Meal created.', category='success')

    return redirect(url_for("meals.meals_home"))

@meals.route('/<meal_name>', methods=['GET'])
@login_required
def meal_page(meal_name):
    meal = Meal.query.filter(func.lower(Meal.name) == meal_name.lower()).first()
    foods = []
    meal_foods = MealFood.query.filter_by(meal_id=meal.id)
    foodIDs = []
    for meal_food in meal_foods:
        user_meal = UserMeal.query.filter_by(user_id=current_user.id, meal_id=meal.id).first()
        meal_food_check = MealFood.query.filter_by(meal_id=meal.id, food_id=meal_food.food_id).first()
        meal_edit = MealEdit.query.filter_by(user_meal_id=user_meal.id, meal_food_id=meal_food_check.id).first()
        new_food = {}
        amount_check = meal_edit.amount > 0 if meal_edit else meal_food.amount > 0
        if amount_check:
            food = Food.query.filter_by(id=meal_food.food_id).first()
            units = []
            for unit in food.units: 
                units.append({"id": unit.id, "name": unit.name})
            foodIDs.append(food.id)
            new_food["id"] = food.id
            new_food["name"] = food.name
            new_food["unit"] = meal_edit.unit if meal_edit else meal_food.unit
            new_food["units"] = units
            new_food["unitsJSON"] = json.dumps(units)
            new_food["amount"] = meal_edit.amount if meal_edit else meal_food.amount
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

    return render_template("meal.html", all_foods=all_foods, foodsJSON=json.dumps(foods), foods=foods, meal=meal, user=current_user)

@meals.route('/update-meal', methods=['POST'])
@login_required
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
            user_meal = UserMeal.query.filter_by(user_id=current_user.id, meal_id=meal.id).first()
            meal_food = MealFood.query.filter_by(meal_id=meal.id, food_id=food.id).first()
            meal_edit = MealEdit.query.filter_by(user_meal_id=user_meal.id, meal_food_id=meal_food.id).first()
            if food.id not in foodIDs:
                if meal_edit:
                    meal_edit.amount = 0
                else:
                    meal_edit = MealEdit(user_meal_id=user_meal.id, meal_food_id=meal_food.id, amount=0, unit=1)
                    db.session.add(meal_edit)
            else:
                meal_food_check = [update_food for update_food in update_meal['foods'] if update_food["id"] == food.id][0]
                amount_check = meal_food_check["amount"] != meal_edit.amount if meal_edit else meal_food.amount != meal_food_check["amount"]
                unit_check = meal_food_check["unit"] != meal_edit.unit if meal_edit else meal_food.unit != meal_food_check["unit"]
                new_meal_edit = MealEdit(user_meal_id=user_meal.id, meal_food_id=meal_food.id, amount=meal_food_check["amount"], unit=meal_food_check["unit"])
                new_meal_edit_change = False
                if amount_check: 
                    if meal_edit:
                        meal_edit.amount = meal_food_check["amount"]
                    else:
                        new_meal_edit_change = True
                        
                if unit_check: 
                    if meal_edit:
                        meal_edit.unit = meal_food_check["unit"]
                    else:
                        new_meal_edit_change = True
                if new_meal_edit_change:
                    db.session.add(new_meal_edit)
                update_meal['foods'] = [update_food for update_food in update_meal['foods'] if update_food["id"] != food.id]
        for food in update_meal['foods']:
            user_meal = UserMeal.query.filter_by(user_id=current_user.id, meal_id=meal.id).first()
            meal_food = MealFood.query.filter_by(meal_id=meal.id, food_id=food["id"]).first()
            if not meal_food:
                meal_food = MealFood(meal_id=meal.id, food_id=food["id"], amount=0, unit=food["unit"])
                db.session.add(meal_food)
                db.session.commit()
            meal_edit = MealEdit(user_meal_id=user_meal.id, meal_food_id=meal_food.id, amount=food["amount"], unit=food["unit"])
            db.session.add(meal_edit)
        db.session.commit()

    return {}, 201, {'Content-Type': 'application/json'}

@meals.route('/update-weekly-meal', methods=['POST'])
@login_required
def update_weekly_meal():
    if request.method == 'POST':
        weekday = request.form.get('weekday')
        meal_id = request.form.get('weekly-meal-select')
        calendar_page = request.form.get('calendar_page')

        meal = Meal.query.get(meal_id)
        if meal:
            meal_foods = MealFood.query.filter_by(meal_id=meal_id).all()
            for meal_food in meal_foods:
                food = Food.query.get(meal_food.food_id)
                add_shopping_item(True, food.name, meal_food.amount, meal_food.unit)
            setattr(current_user, calendar.day_name[int(weekday)][:3].lower()+"Meal", meal_id)
            db.session.commit()
            flash('Meal added to calendar.', category='success')
        else:
            flash('Meal not found.', category='error')

    if calendar_page:
        return redirect(url_for("meals.edit_calendar"))
    else:
        return redirect(url_for("meals.meals_home"))

@meals.route('/edit-calendar', methods=['GET'])
@login_required
def edit_calendar():
    userMeals = UserMeal.query.filter_by(user_id=current_user.id).all()
    meal_options = []
    for userMeal in userMeals:
        new_meal = {}
        meal = Meal.query.filter_by(id=userMeal.meal_id).first()
        new_meal["id"] = userMeal.id
        new_meal["name"] = meal.name
        meal_options.append(new_meal)

    today = date.today().weekday()
    weekly_meals = []
    days = []
    weekly_meal_ids = []
    for day in range(7):
        day_name = calendar.day_name[day]
        meal_id = getattr(current_user, day_name[:3].lower()+"Meal")
        if meal_id:
            weekly_meal_ids.append(meal_id)
        meal = Meal.query.get(meal_id)
        weekly_meals.append(meal)
        days.append(day_name)
    table_columns = Meal.table_columns(self=Meal())
        
    food_ids = [id for id, in db.session.query(UserFood.food_id).filter_by(user_id=current_user.id).all()]
    meal_ids = [id for id, in db.session.query(MealFood.meal_id).filter(MealFood.food_id.not_in(food_ids)).all()]
    for id in weekly_meal_ids:
        meal_ids.append(id)
    meals = Meal.query.filter(Meal.id.not_in(meal_ids)).all()

    return render_template("calendar.html", page='edit-calendar', meal_options=meal_options, table_columns=table_columns, table_title="Recommendations", items=meals, days=days, weekly_meals=weekly_meals, today=today, user=current_user)

@meals.route('/reset-weekly-meal', methods=['POST'])
@login_required
def reset_weekly_meal():
    if request.method == 'POST':
        weekday = request.form.get('weekday')

        meal = Meal.query.get(getattr(current_user, calendar.day_name[int(weekday)][:3].lower()+"Meal"))
        meal_foods = MealFood.query.filter_by(meal_id=meal.id).all()
        for meal_food in meal_foods:
            update_shopping_items(True, meal_food.food_id, meal_food.amount, meal_food.unit)

        setattr(current_user, calendar.day_name[int(weekday)][:3].lower()+"Meal", None)
        db.session.commit()
        flash('Meal reset.', category='success')

    return redirect(url_for("meals.edit_calendar"))

@meals.route('/update-calendar-day', methods=['POST'])
@login_required
def update_calendar_day():
    if request.method == 'POST':
        meal_name = request.form.get('selectedMealName')
        weekday = request.form.get('day-select')

        meal = Meal.query.filter_by(name=meal_name).first()
        if meal:
            meal_foods = MealFood.query.filter_by(meal_id=meal.id).all()
            for meal_food in meal_foods:
                food = Food.query.get(meal_food.food_id)
                add_shopping_item(True, food.name, meal_food.amount, meal_food.unit)
            userMeal = UserMeal.query.filter_by(user_id=current_user.id, meal_id=meal.id).first()
            if not userMeal:
                userMeal = UserMeal(user_id=current_user.id, meal_id=meal.id)
                db.session.add(userMeal)
            setattr(current_user, calendar.day_name[int(weekday)][:3].lower()+"Meal", meal.id)
            db.session.commit()
            flash('Meal added to calendar.', category='success')
        else:
            flash('Meal not found.', category='error')

        return redirect(url_for("meals.edit_calendar"))