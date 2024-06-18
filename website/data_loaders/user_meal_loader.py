from ..models import UserMeal

def load_user_meals(app, db):
    with app.app_context():
        for user_meal in user_meals:
            db.session.add(user_meal)
        db.session.commit()
        print('User meals created.')

user_meals = [
    UserMeal(user_id=1, meal_id=1),
]