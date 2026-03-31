from flask import Flask, render_template, request, redirect

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from database.db import db
    db.init_app(app)

    # To access the routes add a .new_route and register blueprint
    from .routes.home import home_bp
    app.register_blueprint(home_bp)


    from .routes.create import create_bp
    app.register_blueprint(create_bp)


    # Create database
    with app.app_context():
        db.create_all()

    return app