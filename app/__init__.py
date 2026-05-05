from flask import Flask, render_template, request, redirect, session



def create_app(URI):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    app.secret_key = 'stop_hacking_the_server_rudy'

    app.config['SQLALCHEMY_DATABASE_URI'] = URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #new for profilepics
    app.config['UPLOAD_FOLDER'] = 'static/bilder/profile_pics'
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  

    from database.db import db
    db.init_app(app)

    # To access the routes add a .new_route and register blueprint
    from .routes.home import home_bp
    app.register_blueprint(home_bp)

    from .routes.create import create_bp
    app.register_blueprint(create_bp)

    from .routes.view import view_bp
    app.register_blueprint(view_bp)

    from .routes.register import register_bp
    app.register_blueprint(register_bp)

    from .routes.logout import logout_bp
    app.register_blueprint(logout_bp)

    from .routes.login import login_bp
    app.register_blueprint(login_bp)
    
    from .routes.user import userpage_bp
    app.register_blueprint(userpage_bp)

    from .routes.comment import comment_bp
    app.register_blueprint(comment_bp)

    from .routes.review import review_bp
    app.register_blueprint(review_bp)
    
    from .routes.modify import modify_bp
    app.register_blueprint(modify_bp)

    from .routes.delete import delete_bp
    app.register_blueprint(delete_bp)

    from .routes.search import search_bp
    app.register_blueprint(search_bp)

    # Create database
    with app.app_context():
        db.create_all()

    return app