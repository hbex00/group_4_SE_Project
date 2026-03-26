from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app = Flask(__name__, template_folder="../templates", static_folder="../static")

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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# creates sqlAlchemy instance
db = SQLAlchemy(app)


class Recipe(db.Model):
    recipe_titel = db.Column(db.String(200), primary_key=True)


if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations
        db.create_all()      # Creates the database and tables
    app.run(debug=True)