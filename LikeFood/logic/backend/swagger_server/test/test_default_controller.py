# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from logic.backend.swagger_server.models.categories import Categories  # noqa: E501
from logic.backend.swagger_server.models.category import Category  # noqa: E501
from logic.backend.swagger_server.models.like import Like  # noqa: E501
from logic.backend.swagger_server.models.likes import Likes  # noqa: E501
from logic.backend.swagger_server.models.recipe import Recipe  # noqa: E501
from logic.backend.swagger_server.models.recipes import Recipes  # noqa: E501
from logic.backend.swagger_server.models.user import User  # noqa: E501
from logic.backend.swagger_server.models.users import Users  # noqa: E501
from logic.backend.swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_change_pass(self):
        """Test case for change_pass

        Сменить пароль
        """
        body = User()
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/change_password'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_recipe(self):
        """Test case for create_recipe

        Создать рецепт
        """
        body = Recipe()
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/recipe',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_user(self):
        """Test case for create_user

        Создать нового пользователя в системе
        """
        body = User()
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/register',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_like(self):
        """Test case for delete_like

        Удалить оценку с рецепта
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/like/{user_id}/{recipe_id}'.format(user_id=56, recipe_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_recipe(self):
        """Test case for delete_recipe

        Удалить рецепт
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/recipe/{id}'.format(id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_categories(self):
        """Test case for get_all_categories

        Получить все категории
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/category',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_likes(self):
        """Test case for get_all_likes

        Получить все оценки
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/likes',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_recipes(self):
        """Test case for get_all_recipes

        Получить все рецепты
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/recipes',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_category_by_id(self):
        """Test case for get_category_by_id

        Возвращает категорию по id
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/category/{id}'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_like_by_recipe_id(self):
        """Test case for get_like_by_recipe_id

        Возвращает все оценки на рецепте по его id
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/like/{recipe_id}'.format(recipe_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_like_by_user_id(self):
        """Test case for get_like_by_user_id

        Возвращает все оценки пользователя по его id
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/like/{user_id}'.format(user_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_recipe_by_category_id(self):
        """Test case for get_recipe_by_category_id

        Фильтрация по категории
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/recipe/{category_id}'.format(category_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_recipe_by_recipe_id(self):
        """Test case for get_recipe_by_recipe_id

        Возвращает рецепт по id
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/recipe/{id}'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_recipe_by_title(self):
        """Test case for get_recipe_by_title

        Фильтрация по названию
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/recipe/{title}'.format(title='title_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_recipe_by_user_id(self):
        """Test case for get_recipe_by_user_id

        Возвращает все рецепты, созданные пользователем
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/recipe/{author_id}'.format(author_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user_byid(self):
        """Test case for get_user_byid

        Возвращает пользователя по id
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/user/{id}'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_like(self):
        """Test case for put_like

        Оценить рецепт
        """
        body = Like()
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/like',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_top_authors(self):
        """Test case for top_authors

        Вернуть список авторов
        """
        response = self.client.open(
            '/MarinaVereshhagina/LikeFood/1.0.0/top-authors',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
