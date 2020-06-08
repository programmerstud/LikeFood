# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from logic.backend.swagger_server.models.base_model_ import Model
from logic.backend.swagger_server import util


class Like(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, recipe_id: int=None, user_id: int=None):  # noqa: E501
        """Like - a model defined in Swagger

        :param id: The id of this Like.  # noqa: E501
        :type id: int
        :param recipe_id: The recipe_id of this Like.  # noqa: E501
        :type recipe_id: int
        :param user_id: The user_id of this Like.  # noqa: E501
        :type user_id: int
        """
        self.swagger_types = {
            'id': int,
            'recipe_id': int,
            'user_id': int
        }

        self.attribute_map = {
            'id': 'id',
            'recipe_id': 'recipe_id',
            'user_id': 'user_id'
        }
        self._id = id
        self._recipe_id = recipe_id
        self._user_id = user_id

    @classmethod
    def from_dict(cls, dikt) -> 'Like':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Like of this Like.  # noqa: E501
        :rtype: Like
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Like.


        :return: The id of this Like.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Like.


        :param id: The id of this Like.
        :type id: int
        """

        self._id = id

    @property
    def recipe_id(self) -> int:
        """Gets the recipe_id of this Like.


        :return: The recipe_id of this Like.
        :rtype: int
        """
        return self._recipe_id

    @recipe_id.setter
    def recipe_id(self, recipe_id: int):
        """Sets the recipe_id of this Like.


        :param recipe_id: The recipe_id of this Like.
        :type recipe_id: int
        """
        if recipe_id is None:
            raise ValueError("Invalid value for `recipe_id`, must not be `None`")  # noqa: E501

        self._recipe_id = recipe_id

    @property
    def user_id(self) -> int:
        """Gets the user_id of this Like.


        :return: The user_id of this Like.
        :rtype: int
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: int):
        """Sets the user_id of this Like.


        :param user_id: The user_id of this Like.
        :type user_id: int
        """
        if user_id is None:
            raise ValueError("Invalid value for `user_id`, must not be `None`")  # noqa: E501

        self._user_id = user_id
