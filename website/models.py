from . import db
from flask_login import UserMixin
from sqlalchemy.orm import class_mapper, ColumnProperty

ACCESS = {
    'user': 0,
    'admin': 1
}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    access = db.Column(db.Integer, default=0, nullable=False)
    foods = db.relationship('Food', secondary='userFoods', back_populates='users')

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

# userFoods = db.Table('userFoods',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
#     db.Column('amount', db.Integer, unique=True, nullable=False),
#     db.Column('unit', db.Integer, nullable=False),
#     db.Column('expiration', db.DateTime)
# )

foodUnits = db.Table('foodUnits',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
    db.Column('unit_id', db.Integer, db.ForeignKey('unit.id'))    
)