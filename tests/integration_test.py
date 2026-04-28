import pytest 
from flask import request, session
from app import create_app
from database.db import db
from app.services.models import *
from app.utils.tag import *

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

def test_user_page_loads(client):
    response = client.get("/user")
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
    client.post("/logout")
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

def test_comment_route(client):
    with client.session_transaction() as session:
        session['id'] = 1
    
    test_user = User(name = 'Björk',
                    last_name = 'Lukasson',
                    email = 'cba@321.com',
                    password = 'Bj123')
    
    db.session.add(test_user)
    db.session.commit()
    
    test_recipe = Recipe(recipe_title = 'Not that good of a recipe',
                        description = 'Decent recipe description',
                        portions = 5,
                        user_id = 1)
    
    db.session.add(test_recipe)
    db.session.commit

    comment_response_1 = client.post("/comment", data = {  "recipe_id": "1",
                                                "comment": "This recipe is really useful!"}, follow_redirects=True)
    
    assert comment_response_1.status_code == 200
    assert comment_response_1.request.path == '/'
    
    comment_response_2 = client.post("/comment", data = {  "recipe_id": "1",
                                                "comment": ""}, follow_redirects=True)
    
    assert comment_response_2.status_code == 200
    assert comment_response_2.request.path == '/'

    with client:
        comment_1 = Comment.query.filter_by(id=1).first()
        comment_2 = Comment.query.filter_by(id=2).first() 

        assert comment_1.content == "This recipe is really useful!"
        assert comment_2 is None

def test_comment_route_errors(client):
    error_no_session_id = client.post("/comment", data = {  "recipe_id": "1",
                                                "comment": "Good recipe!"}, follow_redirects=True)
    
    assert error_no_session_id.status_code == 200
    assert error_no_session_id.request.path == '/login' 

    with client.session_transaction() as session:
        session['id'] = 1

    error_no_recipe_id = client.post("/comment", data = {  "recipe_id": "",
                                                "comment": "Not to my taste"}, follow_redirects=True)
    
    assert error_no_recipe_id.status_code == 200 
    assert error_no_recipe_id.data == b'invalid recipe ID'

    error_not_found_id = client.post("/comment", data = {  "recipe_id": "1",
                                                "comment": "Hello from sweden"}, follow_redirects=True)
    
    assert error_not_found_id.status_code == 200
    assert error_not_found_id.data == b'Recipe with this ID not found'

def test_comment_get(client):
    with client.session_transaction() as session:
        session['id'] = 1

    response = client.get("/comment")
    assert response.status_code == 200
        
def test_edit_user(client):
    email = "Gunnar@student.ju.se"
    password = "123"
    register_response = client.post("/register", data = {"f_name": "gunnar",
                                     "l_name":"",
                                     "email": email,
                                     "password1": password,
                                     "password2": password}, follow_redirects=True)
    
    assert register_response.status_code == 200
    assert register_response.request.path == '/' 
    
    client.post("/logout", follow_redirects=True)
    with client:
        client.post("/login", data = {"email": email.lower(),
                                      "password": password}, follow_redirects=True)
        assert session['id'] == 1

        client.post("/user",follow_redirects=True)
        assert session['id'] == 1
        assert session['first_name'] == "Gunnar"

        new_email = "Eriksson@student.ju.se"
        new_second_email = "Eriksson2@student.ju.se"
        wrong_email = "Erikssonson@nodot"
        new_password = "Abc"
        wrong_password = "abc"
        new_name = "erik"
        new_surname = "Eriksson"
        
        wrong_password = client.post("/user/edit", data = {"email_address": new_email,
                                          "first_name" : new_name,
                                          "last_name" : new_surname,
                                          "password1": new_password,
                                          "password2": wrong_password}, follow_redirects=True)
        assert wrong_password.status_code == 200
        assert wrong_password.request.path == '/user/edit'
        assert session['id'] == 1
        assert session['first_name'] == "Gunnar"

        wrong_email = client.post("/user/edit", data = {"email_address": wrong_email,
                                          "first_name":"",
                                          "last_name":"",
                                          "password1":"",
                                          "password2":""},follow_redirects=True)
        assert wrong_email.status_code == 200
        assert wrong_email.request.path == '/user/edit'
        assert session['id'] == 1
        assert session['first_name'] == "Gunnar"

        email_test = client.post("/user/edit", data = {"email_address": new_email,
                                          "first_name":"",
                                          "last_name":"",
                                          "password1":"",
                                          "password2":""},follow_redirects=True)
        assert email_test.status_code == 200
        assert email_test.request.path == '/user'
        assert session['id'] == 1
        assert session['first_name'] == "Gunnar"

        password_test = client.post("/user/edit", data = {"email_address":"",
                                          "first_name":"",
                                          "last_name":"",
                                          "password1":new_password,
                                          "password2":new_password},follow_redirects=True)
        assert password_test.status_code == 200
        assert password_test.request.path == '/user'
        assert session['id'] == 1
        assert session['first_name'] == "Gunnar"
        
        existing_email = client.post("/user/edit", data = {"email_address": new_email,
                                          "first_name" : new_name,
                                          "last_name" : new_surname,
                                          "password1": new_password,
                                          "password2": new_password}, follow_redirects=True)
        
        assert existing_email.status_code == 200
        assert existing_email.request.path == '/user/edit'

        correct = client.post("/user/edit", data = {"email_address": new_second_email,
                                          "first_name" : new_name,
                                          "last_name" : new_surname,
                                          "password1": new_password,
                                          "password2": new_password}, follow_redirects=True)

        assert session['id'] == 1
        assert session['first_name'] == "Erik"
        assert session['last_name'] == "Eriksson"

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
    

def test_expected_content(client):
    response = client.get("/")

    assert b"<title>Homepage</title>" in response.data

    assert b"Search for recipe index..." in response.data

    assert b"value=\"Share Recipe\"" in response.data
    assert b"value=\"Review Recipe\"" in response.data
    assert b"value=\"Comment Recipe\"" in response.data


def test_create_tags(client):
    Create_Tags()

    tags = Tag.query.all()
    assert len(tags) > 0
