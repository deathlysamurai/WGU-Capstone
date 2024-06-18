from .user_loader import load_users
from .unit_loader import load_units
from .food_loader import load_foods
from .food_unit_loader import load_food_units
from .meal_loader import load_meals
from .user_food_loader import load_user_foods
from .meal_food_loader import load_meal_foods
from .user_meal_loader import load_user_meals
from .meal_edit_loader import load_meal_edits

def run_data_loaders(app, db):
    load_users(app, db)
    load_units(app, db)
    load_foods(app, db)
    load_food_units(app, db)
    load_user_foods(app, db)
    load_meals(app, db)
    load_meal_foods(app, db)
    load_user_meals(app, db)    
    load_meal_edits(app, db)