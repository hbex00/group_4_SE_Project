import pytest 
from flask import request, session
from app import create_app
from database.db import db
from app.services.models import *
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeMeta
from app.utils.tag import *
from app.utils.user import reset_password
from app.routes.search import SEARCH_TYPES, get_model_from_string
from collections import defaultdict

FILTER_TYPES = SEARCH_TYPES
FILTER_TAGS  = None

# loads existing tags
def build_tag_filters():
    filters = defaultdict(list)
    tags = db.session.execute(select(Tag.category, Tag.unit).distinct().order_by(Tag.category,Tag.unit)).all()

    for tag_category,tag_unit in tags:
        filters[tag_category].append(tag_unit)
    
    return dict(filters)

# Gets or gets and builds filters
# (By subsequently removing the filters, next get will update it.)
def get_tag_filters():
    global FILTER_TAGS
    if FILTER_TAGS is None:
        FILTER_TAGS = build_tag_filters()
    return FILTER_TAGS

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
                    password = 'Adam123',
                    profile_image = 'defualt.svg')
    
    db.session.add(test_user)
    db.session.commit()
    
    test_recipe = Recipe(recipe_title = 'My Good Title',
                        description = 'Book with a good Title',
                        portions = 2,
                        user_id = 1)
    
    db.session.add(test_recipe)
    db.session.commit
    
    #Add a review within valid range (0 < rating > 5)
    review_response_1 = client.post("/review", data = {  "recipe_id": "1",
                                                "review": "3"}, follow_redirects=True)
    
    assert review_response_1.status_code == 200
    assert review_response_1.request.path == '/'

    with client:
        review = Review.query.filter_by(id=1).first()
        assert review.rating == 3
    
    #User add new review which updates existed reviews rating
    review_response_2 = client.post("/review", data = {  "recipe_id": "1",
                                                "review": "2"}, follow_redirects=True)
    
    assert review_response_2.status_code == 200
    assert review_response_2.request.path == '/'

    with client:
        review = Review.query.filter_by(id=1).first()
        assert review.rating == 2

    #Add review below valid range (rating < 0)
    review_response_3 = client.post("/review", data = {  "recipe_id": "1",
                                                "review": "-555"}, follow_redirects=True)
    
    assert review_response_3.status_code == 200
    assert review_response_3.request.path == '/'

    with client:
        review = Review.query.filter_by(id=1).first()
        assert review.rating == 0
    
    #Add review above valid range (rating > 5)
    review_response_4 = client.post("/review", data = {  "recipe_id": "1",
                                                "review": "100"}, follow_redirects=True)
    
    assert review_response_4.status_code == 200
    assert review_response_4.request.path == '/'

    with client:
        review = Review.query.filter_by(id=1).first()
        assert review.rating == 5

    db.session.add(Review(recipe_id="1", rating="4"))
    db.session.commit()
    
    with client:
        review_1 = Review.query.filter_by(id=1).first()
        assert review_1.rating == 5
        review_2 = Review.query.filter_by(id=2).first()
        assert review_2.rating == 4


        recipe = Recipe.query.filter_by(id=1).first()
        assert recipe.review_rating() == 4.5

def test_comment_route(client):
    with client.session_transaction() as session:
        session['id'] = 1
    
    test_user = User(name = 'Björk',
                    last_name = 'Lukasson',
                    email = 'cba@321.com',
                    password = 'Bj123',
                    profile_image = 'defualt.svg'
                    )
    
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

def post_example_user(client,user_arg=None):
    if not client:
        raise TypeError("Expected Client!")
    # Example User Details
    user_email      = "Ragnar@example.com"
    user_password   = "example"
    user_name       = "Ragnar"
    user_last_name  = "Vanheden"
    if user_arg and isinstance(user_arg,User):
        user_email     = user_arg.email
        user_password  = user_arg.password
        user_name      = user_arg.name
        user_last_name = user_arg.last_name
    
    register_response = client.post("/register", data = {"f_name": user_name,
                                     "l_name":user_last_name,
                                     "email": user_email,
                                     "password1": user_password,
                                     "password2": user_password}, follow_redirects=True)
    assert register_response.status_code == 200
    assert register_response.request.path == '/' 

    # Return last (this) User entry
    example_users = list_users()
    return example_users[len(example_users)-1]

def post_example_recipe(client,author=None,recipe=None):
    if not client:
        raise TypeError("Expected Client!")
    # Example Author Details
    if (author and not isinstance(author, User)) or not author:
        author = post_example_user(client)

    # Example Recipe Details
    recipe_title       = "Hamburger Example"
    recipe_description = "This would be a tasty hamburger if it was real!"
    recipe_portions    = 10
    recipe_ingredients = ["Meat","Bun"]
    recipe_amounts     = [4,2]
    recipe_units       = ["Patty","Whole"]
    recipe_steps       = ["",""]

    if recipe and isinstance(recipe, Recipe):
        recipe_title       = recipe.recipe_title
        recipe_description = recipe.description
        recipe_portions    = recipe.portions
        recipe_ingredients = recipe.ingredients
        recipe_amounts     = []
        recipe_units       = []
        recipe_steps       = recipe.steps
        if recipe.ingredients:
            for ingredient in recipe_ingredients:
                if isinstance(ingredient,Ingredient):
                    recipe_amounts.extend(ingredient.amount)
                    recipe_units.extend(ingredient.unit)
    
    with client.session_transaction() as session:
        session["id"] = author.id
    register_response = client.post( "/create", data = {
                                        "title": recipe_title,
                                        "description":recipe_description,
                                        "portions": recipe_portions,
                                        "ingredients[]": recipe_ingredients,
                                        "amount[]": recipe_amounts,
                                        "unit[]": recipe_units,
                                        "step[]": recipe_steps
                                    },follow_redirects=True)

    assert register_response.status_code == 200
    assert register_response.request.path == '/'

    # Log out from current user
    response = client.post("/logout")

    # Return last (this) Recipe entry
    example_recipes = list_recipes()
    return example_recipes[len(example_recipes)-1]

def post_example_comment(client,author=None,recipe=None,comment=None):
    if not client:
        raise TypeError("Expected Client!")
    # Example Author Details
    if (author and not isinstance(author, User)) or not author:
        author = post_example_user(client)
    
    if (recipe and not isinstance(recipe,Recipe)) or not recipe:
        recipe = post_example_recipe(client,author)

    comment_content = "This is a great recipe!"
    comment_recipe_id = recipe.id
    if comment and isinstance(comment,Comment):
        comment_content = comment.content
        comment_recipe_id = comment.id

    with client.session_transaction() as session:
        session["id"] = author.id

    post_comment = client.post("/comment", data = {"recipe_id"  : comment_recipe_id,
                                                    "comment"    : comment_content}, follow_redirects=True)
    assert post_comment.status_code == 200
    assert post_comment.request.path == '/'   

    # Log out from current user
    response = client.post("/logout")

    with client.session_transaction() as session:
        assert session.get("id") == None

    # Return last (this) Recipe entry
    example_comment = list_comments()
    return example_comment[len(example_comment)-1]

def modify_tags(client,recipe,tags:dict=None):
    if not client:
        raise TypeError("Expected Client!")
    if not recipe or not isinstance(recipe,Recipe):
        recipe = post_example_recipe(client)

    # EXAMPLE TAGS 
    example_tags = {"Time":"15 minutes","Complexity":"Easy","Spice":"1"}

    # IF TAGS PROVIDED: OVERRIDE EXAMPLE TAGS
    if tags:
        example_tags = {}
        for tag_category, tag_unit in tags.items():
            example_tags.update({tag_category:tag_unit})

    # MODIFY RECIPE
    modification = client.post("/modify",data={"recipe_id":recipe.id,"tag[]":example_tags})
    return recipe

def list_users():
    try:
        return db.session.execute(select(User)).scalars().all()
    except: raise

def list_recipes():
    try:
        return db.session.execute(select(Recipe)).scalars().all()
    except: raise

def list_comments():
    try:
        return db.session.execute(select(Comment)).scalars().all()
    except: raise

def search(client,pattern="",filter_class: list = ["Recipe"],filter_tags: dict=None):
    data = {"pattern":pattern,"types":filter_class}
    if filter_tags:
        for cat,unit in filter_tags.items():
            data.update({cat:unit})

    response = client.post("/search", data = data,follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/search' 
    return response.data

# def depth_first_building_recursion(b :list):
#     if not b:
#         return
#     for a in b:
#         c = b-a
#         yield depth_first_building_recursion(c)

def test_general_search(client):
    #print(response.get_data(as_text=True))
    # Create database entries
    example_user = post_example_user(client)
    example_recipe = post_example_recipe(client,example_user)
    example_comment = post_example_comment(client,example_user,example_recipe)
    example_recipe = modify_tags(client,example_recipe)

    # Check search route
    response = client.get("/search",follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/search' 

    #USER BYTES
    example_user_name          = bytes(example_user.name, "utf-8")
    example_user_last_name     = example_user_name
    if example_user.last_name and example_user.last_name != "":
        example_user_last_name     = bytes(example_user.last_name, "utf-8")

    #RECIPE BYTES
    example_recipe_title       = bytes(example_recipe.recipe_title, "utf-8")
    example_recipe_description = bytes(example_recipe.description, "utf-8")

    #COMMENT BYES
    example_comment_content    = bytes(example_comment.content, "utf-8")

    #FAULT BYTES
    user_not_found             = bytes("No User Found.","utf-8")
    recipe_not_found           = bytes("No Recipe Found.","utf-8")
    result_not_found           = bytes("recipe_card","utf-8")
    
    search_pattern = [{"User":example_user.name},
                      {"Recipe":example_recipe.description},
                      {"Comment":example_comment.content}]
        
    # FOR EVERY TYPE IN SEARCH TYPES, CONDUCT A SEARCH
    for types in SEARCH_TYPES:
        # ENSURE THAT THE TYPE IS A DATABASE MODEL.
        try:
            type_class = get_model_from_string(types)
        except:
            continue

        for search_dicts in search_pattern:
            # SEARCH WITH ALL PROVIDED TYPES IN SEARCH_TYPES FOR PATTERN PROVIDED IN SEARCH_PATTERN
            for search_class,pattern in search_dicts.items():
                search_result = search(client,pattern,[types])

                # IF THE CLASS MODEL OF THE PATTERN IS THE SAME AS THE ONE BEING SEARCHED FOR, A MATCH SHOULD
                # BE FOUND. ELSE IT SHOULD NOT BE FOUND.
                if get_model_from_string(search_class) == type_class:
                    assert bytes(search_dicts.get(search_class),"utf-8") in search_result
                else:
                    assert bytes(search_dicts.get(search_class),"utf-8") not in search_result

    #RECIPE SEARCH (w filters)
    tags = {}
    for tag_category, tag_units in get_tag_filters().items():
        #Should essentially be replacing the current tag category with the current tag unit.
        tags.update({tag_category:tag_units})
        example_recipe = modify_tags(client,example_recipe,tags)

        for tag_cat, tag_unit in get_tag_filters().items():
            filter_search = search(client,example_recipe.description,["Recipe"],tags)
            recipe_tag = db.session.execute(select(RecipeTag,RecipeTag.recipe_id==example_recipe.id)).scalars().all()
            for r_tag in recipe_tag:
                tag = db.session.execute(select(Tag,Tag.id==r_tag.tag_id)).first()
                if tag:        
                    if tag_cat == tag.category and tag_unit == tag.unit:
                        assert example_recipe_description in filter_search
                    else:
                        assert result_not_found in filter_search

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

    assert b"Search for..." in response.data

    assert b"value=\"Share Recipe\"" in response.data
    assert b"value=\"Review Recipe\"" in response.data
    assert b"value=\"Comment Recipe\"" in response.data


def test_visit_add_recipe(client):
    # not logged in yet
    result = client.get("/create")

    # we expect redirect to /login and redirect status aka 302
    assert result.status_code == 302

    # check redirect location and response
    result = client.get("/create", follow_redirects=True)
    assert result.status_code == 200
    assert result.request.path == '/login'


    # log in to the site and check if we arrive
    with client.session_transaction() as session:
        session['id'] = 1
    
    result = client.get("/create", follow_redirects=True)
    assert result.status_code == 200
    assert result.request.path == '/create'

    email = "Gunnar@student.ju.se"
    password = "123"
    register_response = client.post("/register", data = {"f_name": "gunnar",
                                     "l_name":"",
                                     "email": email,
                                     "password1": password,
                                     "password2": password}, follow_redirects=True)
    
    assert register_response.status_code == 200
    assert register_response.request.path == '/' 

    result = client.post("/create", data = {'title' : "meatballs",
                                            'description' : "good",
                                            'portions' : 2,
                                            'ingredients[]' : ["meat","balls"],
                                            'amount[]' : [2,3],
                                            'unit[]' : ["st","st"],
                                            'step[]' : ["step1","step2"]},
                                              follow_redirects=True)
    assert result.status_code == 200
    assert result.request.path == '/'


def test_create_tags(client):
    Create_Tags()

    tags = Tag.query.all()
    assert len(tags) > 0

def test_tag_recipie(client):
    Create_Tags()

    test_recipe = Recipe(recipe_title = 'A random recipe',
                        description = 'This recipe is something random',
                        portions = 5,
                        user_id = 1)
    
    db.session.add(test_recipe)
    db.session.commit()
    
    tag_add(test_recipe.id, 1)
    tag_add(2, 1)

    tag_correct = RecipeTag.query.filter_by(recipe_id=1, tag_id=1).first()
    tag_no_recipe_id = RecipeTag.query.filter_by(recipe_id=2, tag_id=1).first()

    assert tag_correct.tag.category == 'Time'
    assert tag_correct.tag.unit == '15 minutes'
    assert tag_no_recipe_id is None

def test_password_reset(client):
    create_user = User(name = "a",
                       last_name = "a",
                       email = "a@a.a",
                       password = "a")
    client.post("/register", data = {"f_name": create_user.name,
                                     "l_name": create_user.last_name,
                                     "email": create_user.email,
                                     "password1": create_user.password,
                                     "password2": create_user.password}, follow_redirects=True)
    client.post("/logout")
    with client:
        client.post("/pw-reset", data = {"email": create_user.email,
                                    "name": create_user.name,
                                    "password1": "new",
                                    "password2": "new"}, follow_redirects = True)
        assert session['first_name'].lower() == create_user.name.lower()

def test_comment_edit_delete(client):
    with client.session_transaction() as session:
        session['id'] = 1
    
    test_user = User(name = 'Adam',
                    last_name = 'Karlsson',
                    email = 'cba@123.com',
                    password = 'Ad123',
                    profile_image = 'defualt.svg'
                    )
    
    db.session.add(test_user)
    db.session.commit()
    
    test_recipe = Recipe(recipe_title = 'This recipe is a test',
                        portions = 5,
                        user_id = 1)
    
    db.session.add(test_recipe)
    db.session.commit

    test_comment = Comment(recipe_id = test_recipe.id,
                           user_id = test_user.id,
                           content = 'Hello, Hello!')
    
    db.session.add(test_comment)
    db.session.commit

    comment_response_edit = client.post("/edit-comment", data = {  "comment_id": "1" ,
                                                                   "content": "Hello" }, follow_redirects=True)
    
    assert comment_response_edit.status_code == 200
    assert comment_response_edit.request.path == '/user/recipes'

    with client:
        comment = db.session.get(Comment, 1)
        assert comment.content == "Hello"

    comment_response_delete = client.post("/delete-comment", data = {  "comment_id": "1" }, follow_redirects=True)
    
    assert comment_response_delete.status_code == 200
    assert comment_response_delete.request.path == '/user/recipes'

    with client:
        comment = db.session.get(Comment, 1)
        assert comment is None

def test_review_edit_delete(client):
    with client.session_transaction() as session:
        session['id'] = 1
    
    test_user = User(name = 'Adam',
                    last_name = 'Karlsson',
                    email = 'Hello@123.com',
                    password = 'Ad123',
                    profile_image = 'defualt.svg'
                    )
    
    db.session.add(test_user)
    db.session.commit()
    
    test_recipe = Recipe(recipe_title = 'This recipe is a test',
                        portions = 5,
                        user_id = 1)
    
    db.session.add(test_recipe)
    db.session.commit

    test_review = Review(recipe_id = test_recipe.id,
                           user_id = test_user.id,
                           rating = 5)
    
    db.session.add(test_review)
    db.session.commit

    review_response_edit = client.post("/edit-review", data = {  "review_id": "1" ,
                                                                   "review": "0" }, follow_redirects=True)
    
    assert review_response_edit.status_code == 200
    assert review_response_edit.request.path == '/user/recipes'

    with client:
        review = db.session.get(Review, 1)
        assert review.rating == 0

    review_response_delete = client.post("/delete-review", data = {  "review_id": "1" }, follow_redirects=True)
    
    assert review_response_delete.status_code == 200
    assert review_response_delete.request.path == '/user/recipes'

    with client:
        review = db.session.get(Review, 1)
        assert review is None

def test_review_page_loads(client):
    response = client.get("/review", follow_redirects=True)
    assert response.status_code == 200

def test_review_edit_page_loads(client):
    response = client.get("/edit-review", follow_redirects=True)
    assert response.status_code == 200
    
    db.session.add(Review(recipe_id = 1))
    db.session.commit()
    response = client.get("/edit-review?review_id=1", follow_redirects=True)
    assert response.status_code == 200

def test_comment_page_loads(client):
    response_no_id = client.get("/comment", follow_redirects=True)
    assert response_no_id.status_code == 200


def test_comment_edit_page_get(client):
    response = client.get("/edit-comment", follow_redirects=True)
    assert response.status_code == 200

    db.session.add(Comment(recipe_id = 1))
    db.session.commit()
    response = client.get("/edit-comment?comment_id=1", follow_redirects=True)
    assert response.status_code == 200

def test_review_comment_connection(client):
    with client.session_transaction() as session:
        session['id'] = 1
    
    #Makes a test user
    test_user = User(name = 'Karl',
                    last_name = 'Adamsson',
                    email = 'Karl@123.com',
                    password = 'Kd123',
                    profile_image = 'defualt.svg'
                    )
    
    db.session.add(test_user)
    db.session.commit()
    
    #Makes a test recipe
    test_recipe = Recipe(recipe_title = 'A good recipe',
                        portions = 2,
                        user_id = 1)
    
    db.session.add(test_recipe)
    db.session.commit

    #Add comment to recipe
    comment_response_1 = client.post("/comment", data = {  "recipe_id": "1",
                                                "comment": "Nice recipe!"}, follow_redirects=True)
    
    assert comment_response_1.status_code == 200
    assert comment_response_1.request.path == '/'

    #Add review to recipe
    review_response = client.post("/review", data = {  "recipe_id": "1",
                                                "review": "5"}, follow_redirects=True)
    
    assert review_response.status_code == 200
    assert review_response.request.path == '/'

    #Test if the comment and recipe is connected if the comment was made first
    with client:
        review = db.session.query(Review).filter_by(user_id=test_user.id).first()
        comment = db.session.query(Comment).filter_by(id=1).first()

        assert comment.user_review_id == review.id

    #Add a comment after review
    comment_response_2 = client.post("/comment", data = {  "recipe_id": "1",
                                                "comment": "More people should try this!"}, follow_redirects=True)
    
    assert comment_response_2.status_code == 200
    assert comment_response_2.request.path == '/'

    #Test if the comment and recipe is connected if the review was made first
    with client:
        review = db.session.query(Review).filter_by(user_id=test_user.id).first()
        comment = db.session.query(Comment).filter_by(id=2).first()

        assert comment.user_review_id == review.id
        assert len(review.user_comments) == 2
        
        
def test_recipe_with_empty_name(client):
    create_user(client)
    
    result = client.post("/create", data = {'title' : "",
                                            'description' : "good",
                                            'portions' : 2,
                                            'ingredients[]' : ["meat","balls"],
                                            'amount[]' : [2,3],
                                            'unit[]' : ["st","st"],
                                            'step[]' : ["step1","step2"]},
                                              follow_redirects=True)
    # if we succed we go to the hompage
    # but we should fail and go back to create
    assert result.status_code == 200
    assert result.request.path == '/create'    


def test_adding_tags(client):
    create_user(client)
    Create_Tags()

    result = client.post("/create", data = {'title' : "a good title",
                                            'description' : "good",
                                            'portions' : 2,
                                            'ingredients[]' : ["meat","balls"],
                                            'amount[]' : [2,3],
                                            'unit[]' : ["st","st"],
                                            'step[]' : ["step1","step2"],
                                            'tag[]' : ["Time: 15 minutes", "Complexity: GR"]},
                                              follow_redirects=True)
    
    with client:
        recipe = Recipe.query.first()
        tags = [recipe_tag.tag.unit for recipe_tag in recipe.tags]
        assert len(tags) == 2
        assert "15 minutes" in tags
        assert "GR" in tags
    
    assert result.status_code == 200
    assert result.request.path == '/' 

def test_faulty_tags(client):
    create_user(client)
    Create_Tags()

    result = client.post("/create", data = {'title' : "a good title",
                                            'description' : "good",
                                            'portions' : 2,
                                            'ingredients[]' : ["meat","balls"],
                                            'amount[]' : [2,3],
                                            'unit[]' : ["st","st"],
                                            'step[]' : ["step1","step2"],
                                            'tag[]' : ["Time: 15 min", "Complexity: GR hard"]},
                                              follow_redirects=True)
    
    with client:
        recipe = Recipe.query.first()
        tags = [recipe_tag.tag.unit for recipe_tag in recipe.tags]
        assert len(tags) == 0
    
    assert result.status_code == 200
    assert result.request.path == '/' 

def test_deleting_recipe(client):
    create_user(client)
    result = client.post("/create", data = {'title' : "a good title",
                                            'description' : "good",
                                            'portions' : 2,
                                            'ingredients[]' : ["meat","balls"],
                                            'amount[]' : [2,3],
                                            'unit[]' : ["st","st"],
                                            'step[]' : ["step1","step2"],
                                            'tag[]' : ["Time: 15 min", "Complexity: GR hard"]},
                                              follow_redirects=True)
    assert result.status_code == 200
    assert result.request.path == '/' 

    # delete
    with client:
        recipe = Recipe.query.filter_by(id=1).first()
        assert recipe.recipe_title == "a good title"
    result = client.post("/delete", data = {'recipe_id' : 1}, follow_redirects = True)
    assert result.status_code == 200
    assert result.request.path == '/'
    with client:
        recipe = Recipe.query.filter_by(id=1).first()
        assert recipe == None

    # delete non existing recipe
    result = client.post("/delete", data = {'recipe_id' : 1}, follow_redirects = True)
    assert result.status_code == 200
    assert result.request.path == '/'


def test_get_modify_page(client):
    create_user(client)

    # request on non existing recipe
    result = client.get("/modify", data={'recipe_id' : 1}, follow_redirects=True)
    assert result.status_code == 200
    assert result.request.path == '/'

    recipe = {  'title' : "Test title",
                'description' : "A description",
                'portions' : 2,
                'ingredients[]' : ["meat","balls"],
                'amount[]' : [2,3],
                'unit[]' : ["st","st"],
                'step[]' : ["step1","step2"],
                'tag[]' : ["Time: 15", "Complexity: GR"],
                'private' : "no"}
    re_result = client.post("/create", data=recipe, follow_redirects=True)
    assert re_result.status_code == 200
    assert result.request.path == '/'

    # Get real recipe
    result = client.get("/modify?recipe_id=1", follow_redirects=True)
    assert result.status_code == 200
    assert result.request.path == '/modify'



def test_modify_recipe(client):
    Original_title = "Test title"
    recipe = {  'title' : Original_title,
                'description' : "A description",
                'portions' : 2,
                'ingredients[]' : ["meat","balls"],
                'amount[]' : [2,3],
                'unit[]' : ["st","st"],
                'step[]' : ["step1","step2"],
                'tag[]' : ["Time: 15", "Complexity: GR"],
                'private' : "no"}
    create_modify_base(client, recipe)

    # check so the base recipe was added
    with client:
        check_recipe = Recipe.query.filter_by(id=1).first()
        assert check_recipe.recipe_title == recipe['title']

    # Change nothing (add id to post)
    recipe['recipe_id'] = 1
    result = client.post("/modify", data = recipe, follow_redirects=True)
    assert result.status_code == 200
    assert result.request.path == '/'

    # Remove title
    recipe["title"] = ""
    result = client.post("/modify", data = recipe, follow_redirects=True)

    # Should be the same as the old one
    with client:
        check_recipe = Recipe.query.filter_by(id=1).first()
        assert check_recipe.recipe_title == Original_title
    assert result.status_code == 200
    assert result.request.path == '/'

def test_view_user(client):
    test_user = create_user(client)
    user = User.query.filter_by(name ='Björk').first()
    result = client.get("/viewuser",query_string={"user_id":user.id})
    assert result.status_code == 200
    assert result.request.full_path == f'/viewuser?user_id=1'
    result = client.get("/viewuser",query_string={"user_id":3},follow_redirects=True)
    assert result.request.path == '/'
    result = client.post("/viewuser",follow_redirects=True)
    assert result.request.path == '/'

def create_modify_base(used_client, recipe):
    Create_Tags()
    create_user(used_client)
    result = used_client.post("/create", data = recipe,
                                              follow_redirects=True)
    assert result.status_code == 200
    assert result.request.path == '/'


def create_user(used_client):
    with used_client.session_transaction() as session:
        session['id'] = 1
    test_user = User(name = 'Björk',
                    last_name = 'Lukasson',
                    email = 'cba@321.com',
                    password = 'Bj123',
                    profile_image = 'defualt.svg'
                    )

    db.session.add(test_user)
    db.session.commit()

