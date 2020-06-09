import json
import os
from logic.models import Recipe, LikeSchema
from logic.backend.RecipeLogic import RecipeLogic
from logic import db, ma

def get_all_likes():
    likes = RecipeLogic.get_recipes_with_likes()
    likes_schema = LikeSchema(many=True)
    return likes_schema.dump(likes).data

def remove_like(id):
    like = db.query(Recipe.user_like_recipe).filter_by(id=id).first()
    if like is not None:
        db.session.delete(like)
        db.session.commit()
        return True
    else:
        return None

def add_like(like):
    like = RecipeLogic.put_like(like.user_id, like.recipe_id)
    schema = LikeSchema()
    new_like = schema.load(like, session=db.session).data
    data = schema.dump(new_like).data
    return data
