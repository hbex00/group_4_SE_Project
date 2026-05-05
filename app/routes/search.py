from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from app.utils.search_db import text_search_table, exact_text_search_table
from app.services.models import User,Recipe

search_bp = Blueprint("searchpage", __name__)

#Page variables
page = 'searchpage.html'
path = '/search'
flashes = True

@search_bp.route('/search',methods = ['POST','GET'])
def searchpage():
    if request.method == "POST":
        try:
            pattern = getArgument(arguments=request.form.to_dict(), value="pattern")
            result_users = list()
            result_recipes = list()

            has_filter_user   = hasArgument(arg=request.form.to_dict(), val="filter_user")
            has_filter_recipe = hasArgument(arg=request.form.to_dict(), val="filter_recipe")
            has_any_filter    = has_filter_user | has_filter_recipe

            if has_filter_user:
                result_users.extend(exact_text_search_table(pattern,User))
                has_filter = False

            if has_filter_recipe | (not has_any_filter):
                result_recipes.extend(text_search_table(pattern,Recipe))
                has_filter = True
            
            return render_template(page,
                                search_recipes=(not has_any_filter)|has_filter_recipe,
                                search_users=has_filter_user,
                                result_users=result_users,
                                result_recipes=result_recipes)
        except Exception as error: return error
    else:
        return render_template(page)
    
def getArgument(arguments: dict, value: str):
    if hasArgument(arg=arguments,val=value):
        return arguments.get(value)
    return None
    
def hasArgument(arg: dict, val):
    if bool(arg) == False:
        return False
    if arg.get(val) == None:
        return False
    if type(arg.get(val)) == str and arg.get(val) == "":
        return False
    return True