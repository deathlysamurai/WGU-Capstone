from ..models import UserFood
from datetime import date

def load_user_foods(app, db):
    with app.app_context():
        for user_food in user_foods:
            db.session.add(user_food)
        db.session.commit()
        print('User foods created.')

user_foods = [
    UserFood(user_id=1, food_id=1, amount=100, unit=1, expiration=date.today()),
    UserFood(user_id=1, food_id=3, amount=100, unit=4, expiration=date.today()),
    UserFood(user_id=1, food_id=4, amount=100, unit=4, expiration=date.today()),
    UserFood(user_id=1, food_id=5, amount=100, unit=4, expiration=date.today()),
]