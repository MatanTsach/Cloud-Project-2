# Implements /dishes/{ID} endpoint
from flask_restful import Resource

class DishId(Resource):
    
    def __init__(self, dishes_collection):
        self.dishes_collection = dishes_collection

    def get(self, id):
        dish = self.dishes_collection.get_dish(id)
        if dish is None:
            return -5, 404
        return dish

    def delete(self, id):
        deleted_id = self.dishes_collection.delete_dish(id)
        if deleted_id == -1:
            return -5, 404
        return deleted_id
