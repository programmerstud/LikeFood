from logic import db
from logic.models import Category

class CategoryLogic:
    def __init__(self):
        self.entityClass = Category

    def find_by_id(self, id):
        return Category.query.filter_by(id=id).first()


    def get_categories(self):
        return db.session.query(Category).all()