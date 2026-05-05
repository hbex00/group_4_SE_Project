from flask import Flask, session
from database.db import db
from app.services.models import *

def ingredients_add(ingredients, recipe_id):
    try:          
        # Ingredients is a tuple that contains lists with 3 elements (ingredient name, amount, and unit)
        for name, amount, unit in ingredients:
            added_ingredient = ingredient_create(name, amount, unit, recipe_id)
            
            if added_ingredient is not None:
                db.session.add(added_ingredient)

        db.session.commit()
    except:
        return 'there was an error adding a ingredient'
    

def ingredient_create(name, amount, unit, recipe_id):
    try:
        amo = float(amount)
    except:
        return None

    if name.strip() != "" and amo > 0:
        new_ingredient = Ingredient(name = name, 
                                    amount = amo, 
                                    unit = unit, 
                                    recipe_id=recipe_id)
        return new_ingredient
    else:
        return None


def steps_add(steps , recipe_id):
    try:
        # Creates a new step for each step sent from frontend and adds it to the database
        for recipe_step in steps:
            if recipe_step.strip() != "":
                db.session.add(create_step(recipe_step, recipe_id))
        
        db.session.commit()
    except:
        return 'there was an error adding a step'
      
def create_step(recipe_step, recipe_id):
    if recipe_step.strip() != "" and recipe_id > 0:
        new_step = Step(name=recipe_step,
                        recipe_id=recipe_id) 
    else:
        return None
    return new_step

def comment_add(recipe_id, content, user_id):
    try:
        created = comment_create(recipe_id, content, user_id)

        if created is not None:
            recipe_exist = Recipe.query.filter_by(id=recipe_id).first()
            user_exist = User.query.filter_by(id=user_id).first()

            if recipe_exist is not None and user_exist is not None:
                db.session.add(created)
                db.session.commit()

    except:
        return 'there was an error adding a comment'
    

def comment_create(recipe_id, content, user_id):
    if content.strip() != "" and recipe_id > 0 and user_id > 0:
        comment = Comment(recipe_id = recipe_id,
                          content = content,
                          user_id = user_id)
        
        return comment
    else:
        return None
    
def review_add(recipe_id, score, user_id):
    try:
        review = review_create(recipe_id, score, user_id)

        if review is not None:
            recipe_exist = Recipe.query.filter_by(id=recipe_id).first()
            user_exist = User.query.filter_by(id=user_id).first()

            if recipe_exist is not None and user_exist is not None:
                db.session.add(review)

        db.session.commit()
    
    except:
        return 'There was an error adding your review'

def review_create(recipe_id, score, user_id):
    try:
        rating = round(float(score))
    except:
        return None
    
    if rating >= 0 and rating <= 5:
        new_review = Review(recipe_id=recipe_id,
                            rating=rating,
                            user_id=user_id)
        return new_review
    
    elif rating > 5:
        new_review = Review(recipe_id=recipe_id,
                            rating=5,
                            user_id=user_id)
        return new_review
    
    elif rating < 0:
        new_review = Review(recipe_id=recipe_id,
                            rating=0,
                            user_id=user_id)
        return new_review
    else:
        return None

def tag_add(recipe_id, tag_id):
    try:
        recipe_exist = Recipe.query.filter_by(id=recipe_id).first()
        tag_exist = Tag.query.filter_by(id=tag_id).first()

        if recipe_exist is not None and tag_exist is not None:
            rt = recipetag_create(recipe_id, int(tag_id))

            if rt is not None:
                db.session.add(rt)
            
            db.session.commit()
        
    except:
        return 'There was an error adding a tag to your recipe'
    
def recipetag_create(recipe_id, tag_id):
    if recipe_id > 0 and tag_id > 0:
        rt = RecipeTag( recipe_id = recipe_id,
                        tag_id = tag_id)
    
        return rt
    else:
        return None
    
def review_remove(review_id, user_id):
    try:
        review = db.session.get(Review, review_id)
        user = db.session.get(User, user_id)

        if review is not None and user.id == review.user_id:
            db.session.delete(review)
            db.session.commit()
        else:
            return None
    except:
        return None
