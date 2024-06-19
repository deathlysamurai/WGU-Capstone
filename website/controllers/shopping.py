from flask import Blueprint, render_template, json, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import ShoppingItem, Food, Unit, convertUnits
from .. import db
from sqlalchemy import func

shopping = Blueprint('shopping', __name__)

@shopping.route('/', methods=['GET', 'POST'])
@login_required
def shopping_home():     
    user_shopping_items = ShoppingItem.query.filter_by(user_id=current_user.id).all()
    shopping_items = []
    for shopping_item in user_shopping_items:
        new_shopping_item = {}
        food = Food.query.filter_by(id=shopping_item.food_id).first()
        unit = Unit.query.filter_by(id=shopping_item.unit).first()
        new_shopping_item["id"] = shopping_item.id
        new_shopping_item["name"] = food.name
        new_shopping_item["amount"] = shopping_item.amount
        new_shopping_item["unit"] = unit.name
        new_shopping_item["bought"] = shopping_item.bought
        shopping_items.append(new_shopping_item)

    add_columns = Food.add_columns(self=Food())
    for col in ShoppingItem.add_columns(self=ShoppingItem()):
        add_columns.append(col)
    table_columns = Food.table_columns(self=Food())
    for col in ShoppingItem.add_columns(self=ShoppingItem()):
        table_columns.append(col)
    table_columns.append("bought")

    unit_options = {}
    units = Unit.query.all()
    for unit in units:
        unit_options[unit.name] = unit.id

    foods = Food.query.all()
    food_options = {}
    for food in foods:
        food_options[food.name] = food.id

    return render_template("shopping.html", food_options=food_options, select_options=unit_options, json_select_options=json.dumps(unit_options), table_columns=table_columns, add_columns=add_columns, items=shopping_items, table_title="Shopping", user=current_user, page="shopping")

@shopping.route('/add-shopping-item', methods=['POST'])
@login_required
def add_shopping_item(from_meals=False, name=None, amount=None, unit_id=None):  
    if request.method == 'POST':
        if not name:
            name = request.form.get('name')
        if not amount:
            amount = request.form.get('amount')
        if not unit_id:
            unit_id = request.form.get('unit')

        food = Food.query.filter(func.lower(Food.name) == name.lower()).first()
        unit = Unit.query.get(unit_id)

        if not food:
            flash('Food not found.', category='error')
        elif not unit:
            flash('Unit not found.', category='error')
        elif not from_meals and not amount.isdigit():
            flash('Amount must be be a number.', category='error')
        elif int(amount) <= 0:
            flash('Amount must be greater than 0.', category='error')
        else:
            user_shopping_items = ShoppingItem.query.filter_by(user_id=current_user.id).all()
            old_shopping_item = None
            for shopping_item in user_shopping_items:
                if shopping_item.food_id == food.id:
                    old_shopping_item = shopping_item
            if old_shopping_item:
                new_amount = int(amount)
                if old_shopping_item.unit != unit_id:
                    old_unit = Unit.query.get(old_shopping_item.unit)
                    new_amount = convertUnits(unit.name.lower(), old_unit.name.lower(), int(amount))
                if new_amount:
                    old_shopping_item.amount += new_amount
                    if not from_meals:
                        flash('Shopping item updated.', category='success')
                else:
                    old_shopping_item = None
            if not old_shopping_item:
                new_shopping_item = ShoppingItem(user_id=current_user.id, food_id=food.id, amount=amount, unit=unit.id)
                db.session.add(new_shopping_item)
                if not from_meals:
                    flash('Shopping item created.', category='success')
                
            db.session.commit()
    if from_meals:
        return
    else:
        return redirect(url_for("shopping.shopping_home"))
    
@shopping.route('/remove-shopping-items', methods=['POST'])
@login_required
def remove_shopping_items():  
    if request.method == 'POST':
        shopping_item_ids = json.loads(request.form.get('delete-items'))

        for shopping_item_id in shopping_item_ids:
            shopping_item = ShoppingItem.query.get_or_404(shopping_item_id)
            db.session.delete(shopping_item)

        try:
            db.session.commit()
            flash("Shoppings items removed successfully.", category='success')
        except:
            flash("Problem removing Shopping items.", category='error')

    return redirect(url_for("shopping.shopping_home"))

@shopping.route('/update-shopping-items', methods=['POST'])
@login_required
def update_shopping_items(from_meals=False, food_id=None, meal_food_amount=None, meal_food_unit=None):  
    if request.method == 'POST':
        successful_shopping_items = 0
        items_removed = 0
        if from_meals:
            udpate_shopping_items = []
            shopping_items = ShoppingItem.query.filter_by(user_id=current_user.id, food_id=food_id).all()
            for item in shopping_items:
                new_amount = meal_food_amount
                if item.unit != meal_food_unit:
                    from_unit = Unit.query.get(meal_food_unit)
                    to_unit = Unit.query.get(item.unit)
                    new_amount = convertUnits(from_unit.name.lower(), to_unit.name.lower(), int(amount))
                if new_amount:
                    item.amount -= new_amount   
                if item.amount > 0:
                    food = Food.query.get(food_id)
                    udpate_shopping_items.append({"id":item.id, "name":food.name, "amount":item.amount, "unit":item.unit})
                else:
                    db.session.delete(item)
                    db.session.commit()
                    items_removed += 1
        else:
            udpate_shopping_items = json.loads(request.form.get('update-items'))

        for update_shopping_item in udpate_shopping_items:
            shopping_item = ShoppingItem.query.get_or_404(update_shopping_item['id'])
            amount = update_shopping_item['amount'] if shopping_item.amount != update_shopping_item['amount'] else None

            if not from_meals and not amount.isdigit():
                flash('Amount must be be a number.', category='error')
            elif not from_meals and int(amount) <= 0:
                flash('Amount must be greater than 0.', category='error')
            else:
                if amount:
                    shopping_item.amount = update_shopping_item['amount']
                if amount and int(amount) > 0:
                    db.session.commit()
                    successful_shopping_items += 1
        
        if(successful_shopping_items > 0):
            flash(str(successful_shopping_items)+" shopping items updated successfully.", category="success")
        if(items_removed > 0):
            flash(str(items_removed)+" shopping items removed.", category="success")

    if from_meals:
        return
    else:
        return redirect(url_for("shopping.shopping_home"))
    
@shopping.route('/update-bought', methods=['POST'])
@login_required
def update_bought():  
    if request.method == 'POST':
        shopping_item_info = request.get_json()
        
        shopping_item = ShoppingItem.query.get_or_404(shopping_item_info["id"])
        shopping_item.bought = shopping_item_info["bought"]

        db.session.commit()

    return {}, 201, {'Content-Type': 'application/json'}