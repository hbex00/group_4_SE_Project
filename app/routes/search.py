from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from app.utils.search_db import text_search_table
from app.services.models import User,Recipe,Tag
from collections import defaultdict
from database.db import db
from sqlalchemy import select

search_bp = Blueprint("searchpage", __name__)

#Page Constants
PAGE = 'searchpage.html'
PATH = '/search'
FLASHES = True
FILTERS = None
SEARCH_TYPES = Recipe.__name__, User.__name__

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
    global FILTERS
    if FILTERS is None:
        FILTERS = build_tag_filters()
    return FILTERS

@search_bp.route('/search',methods = ['POST','GET'])
def searchpage():
    if request.method == "POST":
        try:
            pattern = getArgument(arguments=request.form.to_dict(), value="pattern")
            has_filter_user   = hasArgument(arg=request.form.to_dict(), val="")
            has_filter_recipe = hasArgument(arg=request.form.to_dict(), val="filter_recipe")
            has_any_filter    = has_filter_user | has_filter_recipe

            '''information_provided = request.form.listvalues()
            print(str(information_provided))
            information_provided = request.form.to_dict()
            print(str(information_provided))
            information_provided = request.form.getlist("types")
            print(str(information_provided))'''

            results = {}
            for search_class in request.form.getlist("types"):
                class_tags = {}
                for tag_data in request.form.lists():
                    tag_category, tag_unit = tag_data
                    if "." in tag_category:
                        tag_category = (tag_category.split("."))[0]
                        class_tags.update({tag_category:tag_unit})

                if class_tags:
                    class_search_results = {search_class:text_search_table(pattern,get_model_from_string(search_class),class_tags)}
                
                else:
                    class_search_results = {search_class:text_search_table(pattern,get_model_from_string(search_class))}
                
                results.update({search_class:class_search_results})
            print(str(results))
                
            '''if pattern:
                result_users = list()
                result_recipes = list()



                if has_filter_user:
                    result_users.extend(text_search_table(pattern,User,user_tags))
                    has_filter = False

                if has_filter_recipe | (not has_any_filter):
                    result_recipes.extend(text_search_table(pattern,Recipe,recipe_tags))
                    has_filter = True
                
                return render_template(PAGE,
                                    search_recipes=(not has_any_filter)|has_filter_recipe,
                                    search_users=has_filter_user,
                                    result_users=result_users,
                                    result_recipes=result_recipes)
            else:'''
            return render_template(PAGE,
                                search_recipes=(not has_any_filter)|has_filter_recipe,
                                search_users=has_filter_user)
            
        except Exception as error: return error
        except AttributeError as error: return error
        except TypeError as error: return error
    else:
        return render_template(PAGE,filters=get_tag_filters(),search_types=SEARCH_TYPES)
    
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

def get_model_from_string(string):
    if not string:
        raise ValueError("Missing string input!")
    
    if not isinstance(string, str):
        raise TypeError(f"Expected str! Got: " + str(type(string)))
    
    try: 
        for mapper in Recipe.registry.mappers:
            model_class = mapper.class_
            if model_class.__name__ == string:
                return model_class
            
    except Exception as error:
        print(error)

    raise ValueError("No class matches found!")