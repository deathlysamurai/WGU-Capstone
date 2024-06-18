from ..models import Meal

def load_meals(app, db):
    with app.app_context():
        for meal in meals:
            db.session.add(meal)
        db.session.commit()
        print('Meals created.')

meals = [
    Meal(name='Peanut Butter and Jelly'),
    Meal(name='Spaghetti and Meatballs'),
    Meal(name='Spaghetti'),
    Meal(name='Cheese Pizza'),
    Meal(name='Pepperoni Pizza'),
    Meal(name='Grilled Cheese'),
    Meal(name='Peanut Butter Sandwich'),
]