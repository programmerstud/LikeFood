from flask_login import UserMixin

from logic import db, manager, ma


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

user_schema = UserSchema(many = True)