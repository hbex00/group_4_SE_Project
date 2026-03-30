from database.db import db
#Put all tables in this file.

# Table for recipe, Has a foreign key to one user
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_title = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    ingredients = db.relationship('Ingredient', back_populates='recipe')

# Table for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

# Table for Inredient, Each ingredient has a foreign key to a recipe
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    name = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    unit = db.Column(db.String(10))

    recipe = db.relationship('Recipe', back_populates='ingredients')