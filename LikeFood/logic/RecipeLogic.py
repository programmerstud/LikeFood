from logic import db
from logic.models import Recipe, User
from sqlalchemy import desc
from flask_sqlalchemy import BaseQuery

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

    def filter_recipes_author(self, author_login, name, category, sorting):
        return Recipe.query.join(User).filter_by(Recipe.author_id == User.id).filter_by(User.login.like(author_login))

    def filter_recipes_name(self, author_login, name, category, sorting):
        return self.filter_recipes_author(author_login, name, category, sorting).filter_by(Recipe.name == name)

    def filter_recipes_category(self, author_login, name, category, sorting):
        return self.filter_recipes_name(author_login, name, category, sorting).filter_by(Recipe.category_id in [category])

    def filter_recipes_sorting(self, author_login, name, category, sorting):
        if ('sorting' == 'new'):
            return  self.filter_recipes_category(author_login, name, category, sorting).order_by(desc(Recipe.id))
        else:
            return  self.filter_recipes_category(author_login, name, category, sorting).order_by(desc(self.get_recipe_likes(Recipe.id)))

    def filter_my_recipes(self, author_login, name, category, sorting, user: User):
        if ('sorting' == 'new'):
            return  self.filter_recipes_category(author_login, name, category, sorting).filter(Recipe.author_id == user.id).order_by(desc(Recipe.id))
        else:
            return  self.filter_recipes_category(author_login, name, category, sorting).filter(Recipe.author_id == user.id).order_by(desc(self.get_recipe_likes(Recipe.id)))

    def delete_recipe(self, id):
        db.session.delete(self.find_recipe_by_id(id))
        db.session.commit()

    def filter_by_recipe_name(self, recipes : BaseQuery, name):
        return recipes.filter(Recipe.title.like('%' + name + '%'))

    def filter_by_author(self , recipes : BaseQuery, author : User):
        return recipes.filter(Recipe.author_id == author.id)

    def filter_by_author_id(self, recipes : BaseQuery, author_id):
        return recipes.filter(Recipe.author_id == author_id)

    def filter_by_categories(self, recipes : BaseQuery, categories):
        return recipes.filter(Recipe.category_id.in_(categories))

    def filter_order_by(self, recipes : BaseQuery, order):
        if (order == 'like'):
            return None
            '''
            print(User.user_like_recipe.all())
            print('-------------------------------------------')

            db.session.query(User).options(db.joinedload(User.user_like_recipe))

            print(db.session.query(User.id, Recipe.id).join(Recipe).options(db.joinedload(User.user_like_recipe)))
            print(db.session.query(User.id, Recipe.id).join(Recipe).options(db.joinedload(User.user_like_recipe)).all())
            print(db.session.query(User.user_like_recipe).join(Recipe).filter(Recipe.id = user_like_recipe_1.id))
            print(db.session.query(User.user_like_recipe).join(Recipe).filter(
                Recipe.id == User.user_like_recipe.recipe_id))
                recipes.order_by(desc(recipes.join(User.user_like_recipe).filter(Recipe.id == id).count()))'''

        else:
            return recipes.order_by(desc(Recipe.id))
