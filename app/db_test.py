from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# creates a SQLAlchemy instance 'db'
db = SQLAlchemy()

# Table for recipe, with a foreign key to a specified user
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

# Class for Ingredient, Creates a table for each ingredient with a foreign key to a recipe
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    name = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    unit = db.Column(db.String(10))

    recipe = db.relationship('Recipe', back_populates='ingredients')


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


    @app.route('/',methods = ['POST','GET'])
    def home():
        if request.method == 'POST':
            recipe_name = request.form['title']
            new_recipe = Recipe(recipe_title = recipe_name)

            try:
                db.session.add(new_recipe)
                db.session.commit()
                return redirect('/')
            except:
                return 'there was an error'

        else:
            recipe = Recipe.query.all()
            return render_template('addrecipe.html', recipies = recipe)
        
     # Create database
    with app.app_context():
        db.create_all()

    return app

