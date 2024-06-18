from ..models import Food

def load_foods(app, db):
    with app.app_context():
        for food in foods:
            db.session.add(food)
        db.session.commit()
        print('Foods created.')

foods = [
    Food(name='Spaghetti'),
    Food(name='Pizza'),
    Food(name='Bread'),
    Food(name='Peanut Butter'),
    Food(name='Jelly'),
    Food(name='Meatball'),
    Food(name='Flour'),
    Food(name='Cheese'),
    Food(name='Pepperoni'),
    Food(name='Pizza Sauce'),
    Food(name='Pasta Sauce'),
]