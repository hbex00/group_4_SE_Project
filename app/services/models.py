from database.db import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
#Put all tables in this file.

# Table for recipe, Has a foreign key to one user
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_title = db.Column(db.String(50))
    description = db.Column(db.String(150))
    portions = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    ingredients = db.relationship('Ingredient', back_populates='recipe')
    steps = db.relationship('Step', back_populates='recipe')
    user = db.relationship('User', back_populates='recipies')
    comments = db.relationship('Comment', back_populates='recipe')
    reviews = db.relationship('Review', back_populates='recipe')
    tags = db.relationship('RecipeTag', back_populates='recipe')

    def review_rating(self):
        review_count = len(self.reviews)
        total_rating = 0

        for review in self.reviews:
            total_rating += review.rating

        if review_count > 0:
            return round(total_rating / review_count, 2)
        else:
            return 0


# Table for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))

    recipies = db.relationship('Recipe', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')

    def check_email_format(self, email : str):
        if email.__contains__('@') and email.__contains__('.'):
            return True
        return False
    def set_hashed_password(self, password : str):
        self.password = generate_password_hash(password)
    def check_hashed_password(self, hashed_password : str):
        return check_password_hash(self.password,hashed_password)


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


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(250))

    recipe = db.relationship('Recipe', back_populates='comments')
    user = db.relationship('User', back_populates='comments')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)

    recipe = db.relationship('Recipe', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    unit = db.Column(db.String(75))
    

    recipetags = db.relationship('RecipeTag', back_populates='tag')

class RecipeTag(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
   tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

   tag = db.relationship('Tag', back_populates='recipetags')
   recipe = db.relationship('Recipe', back_populates='tags')