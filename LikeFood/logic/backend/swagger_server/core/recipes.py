import json
import os
from logic.models import RecipeSchema
from logic.backend.RecipeLogic import RecipeLogic
from logic import db, ma

def get_all_recipes():
    recipes = RecipeLogic.get_recipes()
    recipes_schema = RecipeSchema(many=True)
    return recipes_schema.dump(recipes).data

def remove_recipe(id):
    recipe = RecipeLogic.find_recipe_by_id(id)
    if recipe is not None:
        db.session.delete(recipe)
        db.session.commit()
        return True
    else:
        return None

def add_recipe(recipe):
    RecipeLogic.add_recipe(recipe.title, recipe.category_id, recipe.file_path, recipe.recipe_text, recipe.author_id)
    schema = RecipeSchema()
    new_recipe = schema.load(recipe, session=db.session).data
    data = schema.dump(new_recipe).data
    return data

def get_recipe(id):
    recipe = RecipeLogic.find_recipe_by_id(id)
    if recipe is not None:
        recipes_schema = RecipeSchema()
        return recipes_schema.dump(recipe).data
    else:
        return None
		
def get_recipes_by_user_id(id):
    recipe = RecipeLogic.get_author_recipes(id)
    if recipe is not None:
        recipes_schema = RecipeSchema(many=True)
        return recipes_schema.dump(recipe).data
    else:
        return None

def get_recipes_by_title(name):
    recipe = RecipeLogic.filter_by_recipe_name(name)
    if recipe is not None:
        recipes_schema = RecipeSchema(many=True)
        return recipes_schema.dump(recipe).data
    else:
        return None
		
def get_recipes_by_category(name):
    recipe = RecipeLogic.filter_by_categories(RecipeLogic.get_recipes(), name)
    if recipe is not None:
        recipes_schema = RecipeSchema(many=True)
        return recipes_schema.dump(recipe).data
    else:
        return None