import pytest 
from flask import request, session
from app import create_app
from database.db import db
from app.services.models import *

@pytest.fixture
def app():
    app = create_app(
        # using a separate database for the tests
        URI='sqlite:///Test.db'
    )
    app.config.update({"TESTING":True})

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

def test_login_user(client):
    test_user = User(name = 'A',
                     last_name = 'B',
                     email = 'a@b.c',
                     password = 'ab')
    client.post("/register", data = {"f_name": test_user.name,
                                     "l_name": test_user.last_name,
                                     "email": test_user.email,
                                     "password1": test_user.password,
                                     "password2": test_user.password}, follow_redirects=True)
    with client:
        error_test = client.post("/login", data = {"email": test_user.email,
                                                    "password": "wrong"}, follow_redirects=True)
        assert 'id' not in session
        assert error_test.request.path == '/login'

    with client:
        result = client.post("/login", data = {"email": test_user.email,
                                               "password": test_user.password}, follow_redirects=True)
        assert session['id'] == 1 
        assert session['first_name'] == test_user.name
        test_logedin = client.post("/login", follow_redirects=True)
        assert test_logedin.request.path == '/'
    assert result.status_code == 200
    assert result.request.path == '/'

def test_reviews_full(client):
    with client.session_transaction() as session:
        session['id'] = 1
    
    test_user = User(name = 'Adam',
                    last_name = 'Eriksson',
                    email = 'abc@abc.com',
                    password = 'Adam123')
    
    db.session.add(test_user)
    db.session.commit()
    
    test_recipe = Recipe(recipe_title = 'My Good Title',
                        description = 'Book with a good Title',
                        portions = 2,
                        user_id = 1)
    
    db.session.add(test_recipe)
    db.session.commit
    
    review_response_1 = client.post("/review", data = {  "recipe_id": "1",
                                                "review": "5"}, follow_redirects=True)
    
    assert review_response_1.status_code == 200
    assert review_response_1.request.path == '/'
    
    review_response_2 = client.post("/review", data = {  "recipe_id": "1",
                                                "review": "4"}, follow_redirects=True)
    
    assert review_response_2.status_code == 200
    assert review_response_2.request.path == '/'
    
    with client:
        r1 = Review.query.filter_by(id=1).first()
        r2 = Review.query.filter_by(id=2).first() 

        assert r1.rating == 5
        assert r2.rating == 4

        recipe = Recipe.query.filter_by(id=1).first()

        assert recipe.review_rating() == 4.5

def test_logout_user(client):
    email = "lars.larsson@larsson.se"
    password = "123"


    response = client.post("/register", data = {"f_name": "Lars",
                                     "l_name": "Larsson",
                                     "email": email,
                                     "password1": password,
                                     "password2": password}, follow_redirects=True)
    
    assert response.status_code == 200
    assert response.request.path == '/' 

    with client:
        client.post("/login", data = {"email": email,
                                      "password": password}, follow_redirects=True)
        assert session['id'] == 1
        result2 = client.post("/logout", follow_redirects=True)
        assert 'id' not in session
        
    assert result2.status_code == 200
    assert result2.request.path == '/'
    
   