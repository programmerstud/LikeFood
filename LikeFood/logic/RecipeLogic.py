from logic import db
from logic.models import Recipe, User
from sqlalchemy import desc, func
from flask_sqlalchemy import BaseQuery
from sqlalchemy.sql import text, case

class RecipeLogic:
    def __init__(self):
        self.entityClass = Recipe

    def add_recipe(self, title, category_id, file_path, recipe_text, author_id):
        new_recipe = Recipe(title=title, category_id=category_id, image=file_path, recipe_text=recipe_text, author_id=author_id)
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe

    def get_recipes(self):
        return Recipe.query

    def get_recipe_likes(self, id):
        return db.session.query(User).join(User.user_like_recipe).filter(Recipe.id==id).count()


    def get_recipes_with_likes(self):
        return db.session.query(Recipe).join(User.user_like_recipe).filter(Recipe.id==id).count()


    def get_recipe_like_by_user(self, user: User, id):
        return db.session.query(User).join(User.user_like_recipe).filter(Recipe.id==id, User.id==user.id).all()

    def put_like(self, user: User, recipe:Recipe):
        user.user_like_recipe.append(recipe)
        db.session.add(user)
        db.session.commit()

    def delete_like(self, user: User, recipe:Recipe):
        user.user_like_recipe.remove(recipe)
        db.session.add(user)
        db.session.commit()

    def get_author_recipes(self, author_id):
        return Recipe.query.filter_by(author_id=author_id).all()

    def find_recipe_by_id(self, id):
        return Recipe.query.filter_by(id=id).first()

    def delete_recipe(self, id):
        db.session.delete(self.find_recipe_by_id(id))
        db.session.commit()

    def filter_by_recipe_name(self, recipes : BaseQuery, name):
        return recipes.filter(Recipe.title.like('%' + name + '%'))

    def filter_by_author(self, recipes : BaseQuery, author : User):
        return recipes.filter(Recipe.author_id == author.id)

    def filter_by_author_id(self, recipes : BaseQuery, author_id):
        return recipes.filter(Recipe.author_id == author_id)

    def filter_by_categories(self, recipes : BaseQuery, categories):
        return recipes.filter(Recipe.category_id.in_(categories))

    def filter_order_by(self, recipes : BaseQuery, order):
        if (order == 'new'):
            return recipes.order_by(desc(Recipe.id))
        else:
            likes = {}
            for recipe in recipes:
                likes[recipe.id] = self.get_recipe_likes(recipe.id)

            sort_order = case(likes, value=Recipe.id)
            q = recipes.order_by(sort_order.desc()).all()

            return recipes.order_by(sort_order.desc())