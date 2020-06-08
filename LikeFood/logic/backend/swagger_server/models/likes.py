# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from logic.backend.swagger_server.models.base_model_ import Model
from logic.backend.swagger_server.models.like import Like  # noqa: F401,E501
from logic.backend.swagger_server import util


class Likes(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self):  # noqa: E501
        """Likes - a model defined in Swagger

        """
        self.swagger_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'Likes':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Likes of this Likes.  # noqa: E501
        :rtype: Likes
        """
        return util.deserialize_model(dikt, cls)
