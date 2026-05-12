from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from app.utils.search_db import text_search_table
from app.services.models import User,Recipe,Tag,Comment
from collections import defaultdict
from database.db import db
from sqlalchemy import select

search_bp = Blueprint("searchpage", __name__)

#Page Constants
PAGE = 'searchpage.html'
PATH = '/search'
FLASHES = True
FILTERS = None
SEARCH_TYPES = Recipe.__name__, User.__name__, Comment.__name__

# loads existing tags
def build_tag_filters():
    filters = defaultdict(list)
    tags = db.session.execute(select(Tag.category, Tag.unit).distinct()).all()

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
            results = {}

            for search_class in request.form.getlist("types"):
                
                # Try identify the model class of the provided string.
                try:
                    search_class = get_model_from_string(search_class)
                except RuntimeError as error:
                    print("Error :" + str(error))
                    continue
                except TypeError as error:
                    print("Error :" + str(error))
                    continue
                except ValueError as error:
                    print("Error :" + str(error))
                    continue

                # Identify tags from the request form and assign them as tags of a certain category.
                class_tags = {}
                for tag_data in request.form.lists():
                    tag_category, tag_unit = tag_data
                    if "." in tag_category:
                        tag_category = (tag_category.split("."))[0]
                        if class_tags.get(tag_category):
                            class_tags.get(tag_category).extend(tag_unit)
                        else:
                            class_tags.update({tag_category:tag_unit})

                # Try to fetch search results from search function in search_db.py
                try:
                    if class_tags:
                        class_search_results = text_search_table(pattern,search_class,class_tags)
                    else:
                        class_search_results = text_search_table(pattern,search_class)
                except RuntimeError as error:
                    print("Error :" + str(error))
                except TypeError as error:
                    print("Error :" + str(error))
                except ValueError as error:
                    print("Error :" + str(error))

                # If no exception was encountered, add the results of the class and go to the next search_class iteration.
                else:
                    results.update({search_class.__name__:class_search_results})
                
            return render_template(PAGE,filters=get_tag_filters(),search_types=SEARCH_TYPES,search_result=results)
            
        except TypeError as error:
            print("Error: " + str(error))
            return render_template(PAGE,filters=get_tag_filters(),search_types=SEARCH_TYPES)
        except AttributeError as error:
            print("Error: " + str(error))
            return render_template(PAGE,filters=get_tag_filters(),search_types=SEARCH_TYPES)
        
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