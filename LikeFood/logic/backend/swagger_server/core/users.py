import json
import os
from logic.backend.models import User, UserSchema
from logic.backend.UserLogic import UserLogic
from logic import db, ma

def get_all_users():
    users = UserLogic.get_all_authors()    
    users_schema = UserSchema(many=True)
    return users_schema.dump(users).data

def add_user(user):
    UserLogic.add_user(user.login, user.password, user.role)
    schema = UserSchema()
    new_user = schema.load(user, session=db.session).data
    data = schema.dump(new_user).data
    return data


def get_user(id):
    user = UserLogic.find_by_id(id)
    if user is not None:
        users_schema = UserSchema()
        return users_schema.dump(user).data
    else:
        return None

def update_user(id, user): 
    update_user = (User.query.filter(User.id == user.id).one_or_none() )

    if update_user is not None:
        schema = UserSchema()
        update = schema.load(user, session=db.session).data
        update.id = update_user.id
        db.session.merge(update)
        db.session.commit()
        data = schema.dump(update_user).data
        return data
    else:
        return None
