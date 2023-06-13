# Implements /dishes/{name} endpoint
from flask_restful import Resource

class DishesName(Resource):

    def __init__(self, db):
        self.db = db
    
    def get(self, name):
        dish_id = self.dishes_collection.get_dish_id(name)
        dish = self.dishes_collection.get_dish(dish_id)
        if dish is None:
            return -5, 404
        return dish
    
    def delete(self, name):
        dish_id = self.dishes_collection.get_dish_id(name)
        deleted_id = self.dishes_collection.delete_dish(dish_id)
        if deleted_id == -1:
            return -5, 404
        return deleted_id