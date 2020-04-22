from logic import db
from logic.models import User

class UserLogic:
    def __init__(self):
        self.entityClass = User

    def add_user(self, login, password, role):
        user = User(login=login, password=password,role=role)
        db.session.add(user)
        db.session.commit()
        return user

    def find_by_id(self, id):
        return User.query.filter_by(id=id).first()

    def get_all_authors(self):
        return User.query.filter_by(role='Author').all()

    def find_by_login(self, login):
        return User.query.filter_by(login=login).first()

    def check_password(self, user: User, password):
        return user.password == password

    def change_password(self, user: User, new_password):
        user.password = new_password
        db.session.add(self)
        db.session.commit()
        return user