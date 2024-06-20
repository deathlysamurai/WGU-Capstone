import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website import create_app, db
from website.models import User, Food, Unit, Meal, UserFood, MealFood, UserMeal, MealEdit, FoodUnit, ShoppingItem
from datetime import date

# To run the tests, execute python -m unittest tests/test_app.py from your project directory. 

class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_create_user(self):
        # Create a user
        user = User(email='test', username='test', password='test')
        db.session.add(user)
        db.session.commit()

        # Retrieve the user from the database
        saved_user = User.query.filter_by(username='test').first()

        # Assert that the user was properly saved
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, 'test')
        self.assertEqual(saved_user.username, 'test')
        self.assertEqual(saved_user.password, 'test')

    def test_create_food(self):
        # Create a food
        food = Food(name='test')
        db.session.add(food)
        db.session.commit()

        # Retrieve the food from the database
        saved_food = Food.query.filter_by(name='test').first()

        # Assert that the food was properly saved
        self.assertIsNotNone(saved_food)
        self.assertEqual(saved_food.name, 'test')
        
    def test_create_unit(self):
        # Create a unit
        unit = Unit(name='test', abbreviation='t')
        db.session.add(unit)
        db.session.commit()

        # Retrieve the unit from the database
        saved_unit = Unit.query.filter_by(name='test').first()

        # Assert that the unit was properly saved
        self.assertIsNotNone(saved_unit)
        self.assertEqual(saved_unit.name, 'test')
        self.assertEqual(saved_unit.abbreviation, 't')

    def test_create_meal(self):
        # Create a meal
        meal = Meal(name='test')
        db.session.add(meal)
        db.session.commit()

        # Retrieve the meal from the database
        saved_meal = Meal.query.filter_by(name='test').first()

        # Assert that the meal was properly saved
        self.assertIsNotNone(saved_meal)
        self.assertEqual(saved_meal.name, 'test')
        
    def test_create_user_food(self):
        # Create a user food
        user = User(email='test', username='test', password='test')
        food = Food(name='test')
        db.session.add(user)
        db.session.add(food)
        db.session.commit()

        user_food = UserFood(user_id=user.id, food_id=food.id, amount=1, unit=1, expiration=date.today())
        db.session.add(user_food)
        db.session.commit()

        # Retrieve the user food from the database
        saved_user_food = UserFood.query.filter_by(user_id=user.id, food_id=food.id).first()

        # Assert that the user food was properly saved
        self.assertIsNotNone(saved_user_food)
        self.assertEqual(saved_user_food.amount, 1)
        self.assertEqual(saved_user_food.unit, 1)
        self.assertEqual(saved_user_food.expiration, date.today())

    def test_create_meal_food(self):
        # Create a meal food
        meal = Meal(name='test')
        food = Food(name='test')
        db.session.add(meal)
        db.session.add(food)
        db.session.commit()

        meal_food = MealFood(meal_id=meal.id, food_id=food.id, amount=1, unit=1)
        db.session.add(meal_food)
        db.session.commit()

        # Retrieve the meal food from the database
        saved_meal_food = MealFood.query.filter_by(meal_id=meal.id, food_id=food.id).first()

        # Assert that the meal food was properly saved
        self.assertIsNotNone(saved_meal_food)
        self.assertEqual(saved_meal_food.amount, 1)
        self.assertEqual(saved_meal_food.unit, 1)

    def test_create_user_meal(self):
        # Create a user meal
        user = User(email='test', username='test', password='test')
        meal = Meal(name='test')
        db.session.add(user)
        db.session.add(meal)
        db.session.commit()

        user_meal = UserMeal(user_id=user.id, meal_id=meal.id)
        db.session.add(user_meal)
        db.session.commit()

        # Retrieve the user meal from the database
        saved_user_meal = UserMeal.query.filter_by(user_id=user.id, meal_id=meal.id).first()

        # Assert that the user meal was properly saved
        self.assertIsNotNone(saved_user_meal)
        self.assertEqual(saved_user_meal.user_id, user.id)
        self.assertEqual(saved_user_meal.meal_id, meal.id)

    def test_create_meal_edit(self):
        user = User(email='test', username='test', password='test')
        meal = Meal(name='test')
        db.session.add(user)
        db.session.add(meal)
        db.session.commit()

        # Create a user meal
        user_meal = UserMeal(user_id=user.id, meal_id=meal.id)
        db.session.add(user_meal)
        db.session.commit()

        food = Food(name='test')
        db.session.add(meal)
        db.session.add(food)
        db.session.commit()

        # Create a meal food
        meal_food = MealFood(meal_id=meal.id, food_id=food.id, amount=1, unit=1)
        db.session.add(meal_food)
        db.session.commit()

        # Create a meal edit
        meal_edit = MealEdit(user_meal_id=user_meal.id, meal_food_id=meal_food.id, amount=1, unit=1)
        db.session.add(meal_edit)
        db.session.commit()

        # Retrieve the meal edit from the database
        saved_meal_edit = MealEdit.query.filter_by(user_meal_id=user_meal.id, meal_food_id=meal_food.id).first()

        # Assert that the meal edit was properly saved
        self.assertIsNotNone(saved_meal_edit)
        self.assertEqual(saved_meal_edit.amount, 1)
        self.assertEqual(saved_meal_edit.unit, 1)

    def test_create_food_unit(self):
        # Create a food
        food = Food(name='test')
        db.session.add(food)
        db.session.commit()

        # Create a unit
        unit = Unit(name='test', abbreviation='t')
        db.session.add(unit)
        db.session.commit()

        # Create a food unit
        food_unit = FoodUnit(food_id=food.id, unit_id=unit.id)
        db.session.add(food_unit)
        db.session.commit()

        # Retrieve the food unit from the database
        saved_food_unit = FoodUnit.query.filter_by(food_id=food.id, unit_id=unit.id).first()

        # Assert that the food unit was properly saved
        self.assertIsNotNone(saved_food_unit)
        self.assertEqual(saved_food_unit.food_id, food.id)
        self.assertEqual(saved_food_unit.unit_id, unit.id)

    def test_create_shopping_item(self):
        # Create a shopping item
        user = User(email='test', username='test', password='test')
        food = Food(name='test')
        db.session.add(user)
        db.session.add(food)
        db.session.commit()

        shopping_item = ShoppingItem(user_id=user.id, food_id=food.id, amount=1, unit=1, bought=True)
        db.session.add(shopping_item)
        db.session.commit()

        # Retrieve the shopping item from the database
        saved_shopping_item = ShoppingItem.query.filter_by(user_id=user.id, food_id=food.id).first()

        # Assert that the shopping item was properly saved
        self.assertIsNotNone(saved_shopping_item)
        self.assertEqual(saved_shopping_item.amount, 1)
        self.assertEqual(saved_shopping_item.unit, 1)
        self.assertEqual(saved_shopping_item.bought, True)

if __name__ == '__main__':
    unittest.main()