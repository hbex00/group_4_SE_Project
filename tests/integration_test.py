import pytest 
from flask import request
from app import create_app
from database.db import db
from app.services.models import *

@pytest.fixture
def app():
    app = create_app(
        # using a separate database for the tests
        URI='sqlite:///Test.db'
    )
    app.config.update({"TESTING":False})

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_register_page_loads(client):
    response = client.get("/register")
    assert response.status_code == 200

def test_register_user(client):
    email = "lars.larsson@larsson.se"
    response = client.post("/register", data = {"f_name": "Lars",
                                     "l_name": "Larsson",
                                     "email": email,
                                     "password1": "lars1",
                                     "password2": "lars1"}, follow_redirects=True)
    
    assert response.status_code == 200
    assert response.request.path == '/' 
    
    with client:
        user = User.query.filter_by(email=email).first()
        assert user.email == email
