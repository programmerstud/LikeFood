import connexion
import six

from logic.backend.swagger_server.models.categories import Categories  # noqa: E501
from logic.backend.swagger_server.models.category import Category  # noqa: E501
from logic.backend.swagger_server.models.like import Like  # noqa: E501
from logic.backend.swagger_server.models.likes import Likes  # noqa: E501
from logic.backend.swagger_server.models.recipe import Recipe  # noqa: E501
from logic.backend.swagger_server.models.recipes import Recipes  # noqa: E501
from logic.backend.swagger_server.models.user import User  # noqa: E501
from logic.backend.swagger_server.models.users import Users  # noqa: E501
from logic.backend.swagger_server import util

from logic.backend.swagger_server.core import categories
from logic.backend.swagger_server.core import recipes
from logic.backend.swagger_server.core import likes
from logic.backend.swagger_server.core import users


def change_pass(id_, body):  # noqa: E501
    """Сменить пароль

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: id of the user that needs an update
    :type id: str

    :rtype: None
    """

    response = {"error": "Пользователь не был найден!"}, 404
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
        try:
            user = users.update_user(id_, body)
            response = user, 200
        except KeyError:
            response = {"error": "Пользователь не был найден!"}, 404
    return response


def create_recipe(body):  # noqa: E501
    """Создать рецепт

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Recipe
    """
    try:
        if connexion.request.is_json:
            body = Recipe.from_dict(connexion.request.get_json())  # noqa: E501
            recipes.add_recipe(body)
            response = body, 200
        else:
            response = {}, 404
    except KeyError:
        response = {"error": "Рецепт не был найден!"}, 404

    return response


def create_user(body):  # noqa: E501
    """Создать нового пользователя в системе

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
        """
    try:
        if connexion.request.is_json:
            body = User.from_dict(connexion.request.get_json())  # noqa: E501
            users.add_user(body)
            response = body, 200
        else:
            response = {}, 404
    except KeyError:
        response = {"error": " "}, 404
    return response


def delete_like(user_id, recipe_id):  # noqa: E501
    """Удалить оценку с рецепта

     # noqa: E501

    :param user_id: id пользователя
    :type user_id: int
    :param recipe_id: id рецепта
    :type recipe_id: int

    :rtype: None
    """
    try:
        pets = likes.remove_like()
        response = {"message": "удаление было произведено успешно"}, 200
    except KeyError:
        response = {"error": "такого рецепта нет!"}, 404
    return response


def delete_recipe(id_):  # noqa: E501
    """Удалить рецепт

     # noqa: E501

    :param id: id рецепта
    :type id: int

    :rtype: None
    """
    try:
        recipes.remove_recipe(str(id_))
        response = {"message": "удаление было произведено успешно"}, 200
    except KeyError:
        response = {"error": "такого рецепта нет!"}, 404
    return response


def get_all_categories():  # noqa: E501
    """Получить все категории

     # noqa: E501


    :rtype: Categories
    """
    categories_in_app = categories.get_all_categories()
    return categories_in_app, 200


def get_all_likes():  # noqa: E501
    """Получить все оценки

     # noqa: E501


    :rtype: List[Likes]
    """
    likes_in_app = likes.get_all_likes()
    return likes_in_app, 200


def get_all_recipes():  # noqa: E501
    """Получить все рецепты

     # noqa: E501


    :rtype: Recipes
    """
    recipes_all = recipes.get_all_recipes()
    return recipes_all, 200


def get_category_by_id(id_):  # noqa: E501
    """Возвращает категорию по id

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Category
    """
    try:
        response = categories.get_category(id_)
    except KeyError:
        response = {"error": "не было ничего найдено!"}, 404
    return response


def get_like_by_recipe_id(recipe_id):  # noqa: E501
    """Возвращает все оценки на рецепте по его id

     # noqa: E501

    :param recipe_id: 
    :type recipe_id: int

    :rtype: Likes
    """
    all_likes = likes.get_all_likes()
    likes_in_app=[]
    for like in all_likes:
        if (recipe_id == like["recipe_id"]):
            likes_in_app.append(like)

    if (likes_in_app != []):
        return likes_in_app, 200
    else:
        return {"error": "не было ничего найдено!"}, 404


def get_like_by_user_id(user_id):  # noqa: E501
    """Возвращает все оценки пользователя по его id

     # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: Likes
    """
    all_likes = likes.get_all_likes()
    likes_in_app=[]
    for like in all_likes:
        if (user_id == like["user_id"]):
            likes_in_app.append(like)

    if (likes_in_app != []):
        return likes_in_app, 200
    else:
        return {"error": "не было ничего найдено!"}, 404


def get_recipe_by_category_id(category_id):  # noqa: E501
    """Фильтрация по категории

     # noqa: E501

    :param category_id: 
    :type category_id: int

    :rtype: Recipes
    """
    if (recipes.get_recipes_by_category(category_id) is not None):
        return users.get_user(category_id), 200
    else:
        return {"error": "не было ничего найдено!"}, 404


def get_recipe_by_recipe_id(id):  # noqa: E501
    """Возвращает рецепт по id

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Recipe
    """    
    if (recipes.get_recipe(id) is not None):
        return users.get_user(id), 200
    else:
        return {"error": "не было ничего найдено!"}, 404



def get_recipe_by_title(title):  # noqa: E501
    """Фильтрация по названию

     # noqa: E501

    :param title: 
    :type title: str

    :rtype: Recipes
    """
    if (recipes.get_recipes_by_title(title) is not None):
        return users.get_user(title), 200
    else:
        return {"error": "не было ничего найдено!"}, 404



def get_recipe_by_user_id(author_id):  # noqa: E501
    """Возвращает все рецепты, созданные пользователем

     # noqa: E501

    :param author_id: 
    :type author_id: int

    :rtype: List[Recipes]
    """
    if (recipes.get_recipes_by_user_id(author_id) is not None):
        return users.get_user(author_id), 200
    else:
        return {"error": "не было ничего найдено!"}, 404


def get_user_byid(id_):  # noqa: E501
    """Возвращает пользователя по id

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: User
    """
    if (users.get_user(id_) is not None):
        return users.get_user(id_), 200
    else:
        return {"error": "не было ничего найдено!"}, 404


def put_like(body):  # noqa: E501
    """Оценить рецепт

     # noqa: E501

    :param body: Пользователь оценил рецепт
    :type body: dict | bytes

    :rtype: Like
    """
    try:
        if connexion.request.is_json:
            body = Like.from_dict(connexion.request.get_json())  # noqa: E501
            likes.add_like(body)
            response = body, 200
        else:
            response = {"error": " "}, 404
    except KeyError:
        response = {"error": " "}, 404
    return response


def top_authors():  # noqa: E501
    """Вернуть список авторов

     # noqa: E501


    :rtype: Users
    """
    try:
        return users.all_users(), 200
    except KeyError:
        return {"error" : "не было ничего найдено!"}, 404
