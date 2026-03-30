from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# creates sqlAlchemy instance
db = SQLAlchemy()

class Recipe(db.Model):
        recipe_titel = db.Column(db.String(200), primary_key=True)


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


    @app.route('/',methods = ['POST','GET'])
    def home():
        if request.method == 'POST':
            recipe_name = request.form['title']
            new_recipe = Recipe(recipe_titel = recipe_name)

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

