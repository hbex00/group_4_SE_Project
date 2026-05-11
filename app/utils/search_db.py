from flask import Flask, session
from sqlalchemy import select, String, Text, or_
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.inspection import inspect
from app.services.models import Tag
from database.db import db

def text_search_table(pattern,orm_class,class_tags: dict=None):
    #Handle incoming arguments
    if not pattern:
        pattern = ""
    if not orm_class:
        raise ValueError("Empty class")
    if not isinstance(orm_class, DeclarativeMeta):
        raise TypeError("orm_class must be a SQLAlchemy model")

    #Construct a pattern string format to look for
    if pattern == "":
        search_pattern = f"%"
    else:
        search_pattern = f"%{pattern}%"  

    #Return all tables from a specific class with text content
    table_text_columns = []
    for column in orm_class.__table__.columns:
        if isinstance(column.type, (String,Text)):
            table_text_columns.append(column)
    if not table_text_columns:
        return []

    #text columns that match the search pattern
    column_match_conditions = [column.ilike(search_pattern) for column in table_text_columns]
    #Query where any such match is returned.
    matching_table_query = select(orm_class).where(or_(*column_match_conditions))

    verified_tags = False
    if class_tags:
        orm_class_tag: DeclarativeMeta = None
        mapper = inspect(orm_class)

        # Go through the relationships of the Orm Model until the target matches tags
        for relation in mapper.relationships:
            target = relation.entity.class_
            if hasattr(target,"tag_id"):
                orm_class_tag = target
                break

        # Target was acquired. Performing the search with tags.
        if orm_class_tag:
            verified_tags = True

            #If orm_class_tag is None:
            #raise ValueError("No tags found for " + str(orm_class))
            #Are you sure that you are looking for an object with tags in its relationship..?

    #Only perform the following if we know that the Model has relations to Tags.
    if verified_tags:
        
        # The following is essentially a function/query to explore in-depth and return foreign keys in an SQL Orm class
        # This is specifically needed due to intermediate model classes like RecipeTags (Tags -> RecipeTags -> Recipe)
        parent_foreign_key = next(column
                                  for column in orm_class_tag.__table__.columns
                                    if column.foreign_keys and any(
                                        fk.column.table == orm_class.__table__
                                        for fk in column.foreign_keys))
        
        # Form the query to join its respective tags class (i.e. RecipeTag)
        matching_table_query = (matching_table_query
                                .join(orm_class_tag, parent_foreign_key==orm_class.id)
                                .join(Tag,Tag.id == orm_class_tag.tag_id))
        
        # For each tag provided in class_tags we update the table query to only return results with matching tag categories and units.
        for tag_category,tag_units in class_tags.items():
            matching_table_query = matching_table_query.where(Tag.category == tag_category,Tag.unit.in_(tag_units))


    # The Query will return the matching sets and base it on their class id. Only distinct results are returned.
    matching_table_query = matching_table_query.group_by(orm_class.id).distinct()

    # Try executing the Query and proceed to return the results
    try:
        return db.session.execute(matching_table_query).scalars().all()
    except: raise RuntimeError("Could not execute Query.")