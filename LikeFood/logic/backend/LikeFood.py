#!/usr/local/bin/python
# coding: utf-8
from flask_login import login_user, logout_user, current_user
import os
import random
import string
from logic.backend.UserLogic import UserLogic
from logic.backend.RecipeLogic import RecipeLogic
from logic.backend.CategoryLogic import CategoryLogic

class LikeFood:

    def __init__(self):
        self.user_logic = UserLogic()
        self.recipe_logic = RecipeLogic()
        self.category_logic = CategoryLogic()

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg', 'gif'])

    def gen_password(self, length=8, method=["lowercase", "uppercase", "digits", "punctuation"]):
        pwd = []
        for i in range(length):
            choice = random.choice(method)
            if choice == "lowercase":
                pwd.append(random.choice(string.ascii_lowercase))
            if choice == "uppercase":
                pwd.append(random.choice(string.ascii_uppercase))
            if choice == "digits":
                pwd.append(random.choice(string.digits))
            if choice == "punctuation":
                pwd.append(random.choice(string.punctuation))
            if choice == "string":
                pwd.append(random.choice(string.punctuation))
        random.shuffle(pwd)
        return ''.join(pwd)

    def show_top_raiting(self):
        authors = self.user_logic.get_all_authors()
        raiting = {}
        for author in authors:
            count = 0
            recipes = self.recipe_logic.get_author_recipes(author.id)
            for recipe in recipes:
                count += self.recipe_logic.get_recipe_likes(recipe.id)
            raiting[author.login] = count
        list_raiting = list(raiting.items())
        list_raiting.sort(key=lambda i: i[1], reverse=True)
        return list_raiting

    def show_recipes(self, recipes, value):
        names_authors = [recipes.count()]
        likes = [recipes.count()]
        i = 1
        for recipe in recipes:
            user = self.user_logic.find_by_id(recipe.author_id)
            names_authors.insert(i, user.login)
            likes.insert(i, self.recipe_logic.get_recipe_likes(recipe.id))
            i += 1
        if value == 'authors':
            return names_authors
        if value == 'likes':
            return likes

    def check_user(self, login):
        return self.user_logic.find_by_login(login)

    def get_recipe_info(self, recipe_id):
        return self.recipe_logic.find_recipe_by_id(recipe_id)

    def is_user_like_recipe(self, id):
        like = self.recipe_logic.get_recipe_like_by_user(current_user, id)
        if like:
            return True
        else:
            return False

    def add_like_to_recipe(self, recipe_id):
        return self.recipe_logic.put_like(current_user, self.get_recipe_info(recipe_id))

    def delete_like_from_recipe(self, recipe_id):
        return self.recipe_logic.delete_like(current_user, self.get_recipe_info(recipe_id))

    def delete_recipe(self, recipe_id):
        return self.recipe_logic.delete_recipe(recipe_id)

    def login(self, login):
        login_user(self.user_logic.find_by_login(login))

    def register(self, login, password, role):
        return self.user_logic.add_user(login, password, role)

    def get_filtered_recipes(self, name, author_name, my_id, categories, order):
        recipes = self.recipe_logic.get_recipes()
        if name:
            recipes = self.recipe_logic.filter_by_recipe_name(recipes, name)
        if author_name:
            if (self.user_logic.find_by_login(author_name)):
                recipes = self.recipe_logic.filter_by_author(recipes, self.user_logic.find_by_login(author_name))
        if (my_id == 'True'):
            recipes = self.recipe_logic.filter_by_author_id(recipes, current_user.id)
        if categories:
            recipes = self.recipe_logic.filter_by_categories(recipes, categories)
        return self.recipe_logic.filter_order_by(recipes, order)

    def create_recipe(self, title, category_id, image, recipe_text):
        author_id = current_user.id
        PATH = os.getcwd() + "\\logic\\static\\images\\" + title
        os.mkdir(PATH)
        image.save(os.path.join(PATH + "\\" + image.filename))
        file_path = "static/images/" + title + "/" + image.filename
        return self.recipe_logic.add_recipe(title, category_id, file_path, recipe_text, author_id)

    def show_categories(self):
        return self.category_logic.get_categories()

    def change_password(self, login, new_password):

        self.user_logic.change_password(self.user_logic.find_by_login(current_user.login), new_password)

    def current_user_role(self):
        return current_user.role

    def current_user_id(self):
        return current_user.id

    def current_user_is_authenticated(self):
        return current_user.is_authenticated

    def get_author_login(self, author_id):
        return self.user_logic.find_by_id(author_id).login

    def get_category_name(self, category_id):
        return self.category_logic.find_by_id(category_id).title

    def logout(self):
        logout_user()

likeFood = LikeFood()