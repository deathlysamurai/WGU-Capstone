from . import db
from flask_login import UserMixin
from sqlalchemy.orm import class_mapper, ColumnProperty

ACCESS = {
    'user': 0,
    'admin': 1
}

def convertUnits(from_unit, to_unit, value):
    result = None
    conversion_factor = {
        "ounce": {"pound":.0625, "gram":28.3495},
        "pound": {"ounce":16, "gram":453.592},
        "gram": {"ounce":0.03527, "pound":0.0022},
    }
    if from_unit in conversion_factor:
        if to_unit in conversion_factor[from_unit]:
            result = value * conversion_factor[from_unit][to_unit]
    
    return result

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    access = db.Column(db.Integer, default=0, nullable=False)
    monMeal = db.Column(db.Integer, default=None, nullable=True)
    tueMeal = db.Column(db.Integer, default=None, nullable=True)
    wedMeal = db.Column(db.Integer, default=None, nullable=True)
    thuMeal = db.Column(db.Integer, default=None, nullable=True)
    friMeal = db.Column(db.Integer, default=None, nullable=True)
    satMeal = db.Column(db.Integer, default=None, nullable=True)
    sunMeal = db.Column(db.Integer, default=None, nullable=True)
    foods = db.relationship('Food', secondary='userFoods', back_populates='users')
    meals = db.relationship('Meal', secondary='userMeals', back_populates='users')
    shopping_items = db.relationship('Food', secondary='shoppingItems', back_populates='users')

    def is_admin(self):
        return self.access == ACCESS['admin']
    
    def allowed(self, access_level):
        return self.access >= access_level
    
    def table_columns(self):
        hidden_props = ["id", "password"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]
    
    def add_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]
    
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    units = db.relationship('Unit', secondary='foodUnits', back_populates='foods')
    users = db.relationship('User', secondary='userFoods', back_populates='foods')
    meals = db.relationship('Meal', secondary='mealFoods', back_populates='foods')
    users = db.relationship('User', secondary='shoppingItems', back_populates='shopping_items')

    def table_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]

    def add_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    abbreviation = db.Column(db.String(50), nullable=False)
    foods = db.relationship('Food', secondary='foodUnits', back_populates='units')
    pantries = db.relationship('UserFood')
    meals = db.relationship('MealFood')
    shopping_items = db.relationship('ShoppingItem')

    def table_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]

    def add_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]
    
class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    foods = db.relationship('Food', secondary='mealFoods', back_populates='meals')
    users = db.relationship('User', secondary='userMeals', back_populates='meals')

    def table_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]

    def add_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]

class UserFood(db.Model):
    __tablename__ = "userFoods"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    amount = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Integer, db.ForeignKey('unit.id'))
    expiration = db.Column(db.Date)

    def table_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]

    def pantry_add_columns(self):
        hidden_props = ["id", "user_id", "food_id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]
    
class MealFood(db.Model):
    __tablename__ = "mealFoods"
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    amount = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Integer, db.ForeignKey('unit.id'))
    edits = db.relationship('UserMeal', secondary='mealEdits', back_populates='edits')

    def table_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]

    def add_columns(self):
        hidden_props = ["id", "meal_id", "food_id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]
    
class UserMeal(db.Model):
    __tablename__ = "userMeals"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    edits = db.relationship('MealFood', secondary='mealEdits', back_populates='edits')

    def table_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]

    def add_columns(self):
        hidden_props = ["id", "user_id", "meal_id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]
    
class MealEdit(db.Model):
    __tablename__ = "mealEdits"
    id = db.Column(db.Integer, primary_key=True)
    user_meal_id = db.Column(db.Integer, db.ForeignKey('userMeals.id'))
    meal_food_id = db.Column(db.Integer, db.ForeignKey('mealFoods.id'))
    amount = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Integer, db.ForeignKey('unit.id'))

    def table_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]

    def add_columns(self):
        hidden_props = ["id", "user_id", "meal_food_id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]

class FoodUnit(db.Model):
    __tablename__ = "foodUnits"
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))

class ShoppingItem(db.Model):
    __tablename__ = "shoppingItems"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    amount = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Integer, db.ForeignKey('unit.id'))
    bought = db.Column(db.Boolean, default=False, nullable=False)

    def table_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]

    def add_columns(self):
        hidden_props = ["id", "user_id", "food_id", "bought"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]