from ..models import MealFood

def load_meal_foods(app, db):
    with app.app_context():
        for meal_food in meal_foods:
            db.session.add(meal_food)
        db.session.commit()
        print('Meal foods created.')

meal_foods = [
    MealFood(meal_id=1, food_id=3, amount=200, unit=4),
    MealFood(meal_id=1, food_id=4, amount=200, unit=4),
    MealFood(meal_id=1, food_id=5, amount=200, unit=4),
    MealFood(meal_id=2, food_id=1, amount=300, unit=4),
    MealFood(meal_id=2, food_id=6, amount=5, unit=2),
    MealFood(meal_id=3, food_id=1, amount=300, unit=4),
    MealFood(meal_id=4, food_id=7, amount=200, unit=4),
    MealFood(meal_id=4, food_id=8, amount=100, unit=4),
    MealFood(meal_id=4, food_id=10, amount=50, unit=4),
    MealFood(meal_id=5, food_id=7, amount=200, unit=4),
    MealFood(meal_id=5, food_id=8, amount=100, unit=4),
    MealFood(meal_id=5, food_id=10, amount=50, unit=4),
    MealFood(meal_id=5, food_id=9, amount=12, unit=5),
    MealFood(meal_id=6, food_id=3, amount=1, unit=5),
    MealFood(meal_id=6, food_id=8, amount=100, unit=4),
    MealFood(meal_id=1, food_id=3, amount=200, unit=4),
    MealFood(meal_id=1, food_id=4, amount=200, unit=4),
]