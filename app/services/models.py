from database.db import db
#Put all tables in this file.

# Table for recipe, Has a foreign key to one user
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_title = db.Column(db.String(50))
    description = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    ingredients = db.relationship('Ingredient', back_populates='recipe')
    steps = db.relationship('Step', back_populates='recipe')
    user = db.relationship('User', back_populates='recipies')


# Table for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    #email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))

    recipies = db.relationship('Recipe', back_populates='user')


# Table for Inredient, Each ingredient has a foreign key to a recipe
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    name = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    unit = db.Column(db.String(10))
    
    recipe = db.relationship('Recipe', back_populates='ingredients')

# Table for the steps that the recipes have
class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    name = db.Column(db.String(150))

    recipe = db.relationship('Recipe', back_populates='steps')