from ..models import MealEdit

def load_meal_edits(app, db):
    with app.app_context():
        for meal_edit in meal_edits:
            db.session.add(meal_edit)
        db.session.commit()
        print('Meal edits created.')

meal_edits = [
    MealEdit(user_meal_id='1', meal_food_id='2', amount=300, unit=4),
]