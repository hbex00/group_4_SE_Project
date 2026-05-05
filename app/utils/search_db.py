from flask import Flask, session
from sqlalchemy import select
from database.db import db
from app.services.models import *

def search(pattern, filter : dict):
    return_list = list()
    if pattern == None:
        print("Pattern is None...")
        return return_list
    
    if bool(filter) == True:
        print(str(pattern)+"...")
        if filter.get('user') and filter.get('user') == True:
            trigger(1)
            for i in range(0,len(select(User))):
                trigger(2,i)
                user: User = db.session.get(User,i)
                fullname :str = (user.name + (user.last_name | "")).lower()
                if pattern.lower() in fullname:
                    trigger(2,fullname)
                    return_list.append(user)

        if filter.get('recipe') and filter.get('recipe') == True:
            trigger(3)
            for i in range(0,len(select(Recipe))):
                trigger(4,i)
                recipe: Recipe = db.session.get(Recipe,i)
                text :str = (recipe.recipe_title).lower() + ((recipe.description).lower() | "") + ((recipe.steps).lower() | "")
                if pattern.lower() in text:
                    trigger(4,text)
                    return_list.append(recipe) 

    print("No return at all?")
    return return_list

def trigger(arg, args):
    if bool(args):
        print("Error encountered at: " + str(arg) + "> " + str(args))
    else:
        print("Error encountered at: " + str(arg))
    
    