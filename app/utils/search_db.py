from flask import Flask, session
from sqlalchemy import select, String, Text, or_
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.inspection import inspect
from app.services.models import Tag
from database.db import db

def text_search_table(pattern,orm_class,class_tags: dict=None):
    if not pattern:
        pattern = ""
     
    if not orm_class:
        raise ValueError("Empty class")
    
    if not isinstance(orm_class, DeclarativeMeta):
        raise TypeError("orm_class must be a SQLAlchemy model")

    if pattern == "":
        search_pattern = f"%"
    else:
        search_pattern = f"%{pattern}%"  

    table_text_columns = []
    for column in orm_class.__table__.columns:
        if isinstance(column.type, (String,Text)):
            table_text_columns.append(column)
    if not table_text_columns:
        return []

    column_match_conditions = [column.ilike(search_pattern) for column in table_text_columns]
    matching_table_query = select(orm_class).where(or_(*column_match_conditions))

    if class_tags:
        orm_class_tag: DeclarativeMeta = None
        mapper = inspect(orm_class)

        for relation in mapper.relationships:
            target = relation.entity.class_
            if hasattr(target,"tag_id"):
                orm_class_tag = target
                break

        if orm_class_tag is None:
            verified_tags = False
            #raise ValueError("No tags found for " + str(orm_class))
            #Are you sure that you are looking for an object with tags in its relationship..?
        else:
            verified_tags = True

    if verified_tags:
        
        # The following is essentially a function/query to explore in-depth and return foreign keys in an SQL Orm class
        parent_foreign_key = next(column
                                  for column in orm_class_tag.__table__.columns
                                    if column.foreign_keys and any(
                                        fk.column.table == orm_class.__table__
                                        for fk in column.foreign_keys))
        
        # Form the query to include its respective tags (i.e. RecipeTag)
        matching_table_query = (matching_table_query
                                .join(orm_class_tag, parent_foreign_key==orm_class.id)
                                .join(Tag,Tag.id == orm_class_tag.tag_id))
        
        # For each tag provided in class_tags we update the table query to only return results with matching tag categories and units.
        for tag_category,tag_units in class_tags.items():
            matching_table_query = matching_table_query.where(Tag.category == tag_category,Tag.unit.in_(tag_units))

        # The Query will return the matching sets and base it on their class id. Only distinct results are returned.
        matching_table_query = matching_table_query.group_by(orm_class.id).distinct()

    try:
        return db.session.execute(matching_table_query).scalars().all()
    except: raise