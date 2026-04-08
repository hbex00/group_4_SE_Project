from flask import Flask, render_template, request, redirect, session



def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = 'stop_hacking_the_server_rudy'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from database.db import db
    db.init_app(app)

    # To access the routes add a .new_route and register blueprint
    from .routes.home import home_bp
    app.register_blueprint(home_bp)


    from .routes.create import create_bp
    app.register_blueprint(create_bp)

    from .routes.view import view_bp
    app.register_blueprint(view_bp)

    from .routes.login import login_bp
    app.register_blueprint(login_bp)


    # Create database
    with app.app_context():
        db.create_all()

    return app