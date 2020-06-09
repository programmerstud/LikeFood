import json
import os
from logic import db, ma
from logic.models import CategorySchema
from logic.backend.CategoryLogic import CategoryLogic

def get_all_categories():
    categories = CategoryLogic.get_categories()
    categories_schema = CategorySchema(many=True)
    return categories_schema.dump(categories).data

def get_category(id):
    category = CategoryLogic.find_by_id(id)
    if category is not None:
        categories_schema = CategorySchema()
        return categories_schema.dump(category).data
    else:
        return None
