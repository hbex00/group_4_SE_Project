from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from app.utils.search_db import search
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
            pattern_filter=dict()
            print(">>>>>>>>>>>>>>Error after this point!<<<<<<<<<<<<<<<<")
            print("arguments > " + str(request.form.to_dict()))
            value = hasArgument(arg=request.form.to_dict(), val="filter_recipe")
            pattern_filter["recipe"] = value
            value = hasArgument(arg=request.form.to_dict(), val="filter_user")
            pattern_filter["user"] = value

            # No pattern was provided. Assuming search for Recipe content
            if not (pattern_filter["user"] and pattern_filter["recipe"]):
                pattern_filter["recipe"] = True

            pattern = getArgument(arguments=request.form.to_dict(), value="pattern")
            results = search(pattern=pattern, filter=pattern_filter)
            result_users = list()
            result_recipes = list()

            if len(results) > 0:
                i = 0
                if pattern_filter["user"]:
                    while len(results) > i and type(results[i]) == User:
                        result_users.append(results[i])
                        i = i+1

                if pattern_filter["recipe"]:
                    while len(results) > i and type(results[i]) == Recipe:
                        result_recipes.append(results[i])
                        i = i+1

            return render_template(page,
                                search_recipes=pattern_filter["recipe"],
                                search_users=pattern_filter["user"],
                                result_users=result_users,
                                result_recipes=result_recipes)
        except TypeError as error: return error
    else:
        return render_template(page)
    
def getArgument(arguments: dict, value: str):
    if hasArgument(arg=arguments,val=value):
        return arguments.get(value)
    return None
    
def hasArgument(arg: dict, val):
    print("Bool status:")
    print(" > " + str(bool(arg)))
    print("   - " + str(arg))
    if bool(arg) == False:
        return False
    print(" => " + str(arg.get(val)))
    if arg.get(val) == None:
        return False
    if type(arg.get(val)) == str and arg.get(val) == "":
        return False
    return True

def trigger(index,argument):
    print("AT: " + str(index) + "> " + str(argument))