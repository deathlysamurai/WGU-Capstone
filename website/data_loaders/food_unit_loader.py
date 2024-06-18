from ..models import FoodUnit

def load_food_units(app, db):
    with app.app_context():
        for food_unit in food_units:
            db.session.add(food_unit)
        db.session.commit()
        print('Food units created.')

food_units = [
    FoodUnit(food_id='1', unit_id='1'),
    FoodUnit(food_id='1', unit_id='3'),
    FoodUnit(food_id='1', unit_id='4'),
    FoodUnit(food_id='2', unit_id='2'),
    FoodUnit(food_id='2', unit_id='4'),
    FoodUnit(food_id='2', unit_id='5'),
    FoodUnit(food_id='3', unit_id='4'),
    FoodUnit(food_id='3', unit_id='5'),
    FoodUnit(food_id='4', unit_id='4'),
    FoodUnit(food_id='5', unit_id='4'),
    FoodUnit(food_id='6', unit_id='2'),
    FoodUnit(food_id='6', unit_id='4'),
    FoodUnit(food_id='7', unit_id='1'),
    FoodUnit(food_id='7', unit_id='3'),
    FoodUnit(food_id='7', unit_id='4'),
    FoodUnit(food_id='8', unit_id='1'),
    FoodUnit(food_id='8', unit_id='3'),
    FoodUnit(food_id='8', unit_id='4'),
    FoodUnit(food_id='9', unit_id='1'),
    FoodUnit(food_id='9', unit_id='2'),
    FoodUnit(food_id='9', unit_id='3'),
    FoodUnit(food_id='9', unit_id='4'),
    FoodUnit(food_id='9', unit_id='5'),
    FoodUnit(food_id='10', unit_id='1'),
    FoodUnit(food_id='10', unit_id='4'),
    FoodUnit(food_id='11', unit_id='1'),
    FoodUnit(food_id='11', unit_id='4'),
]