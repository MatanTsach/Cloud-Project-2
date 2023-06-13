# Implements /dishes/{ID} endpoint
from flask_restful import Resource
import json

class DishesId(Resource):
    
    def __init__(self, db):
        self.db = db
        self.dishes = db['dishes']

    def get(self, id):
        dish = self.dishes.find({'ID': id})
        if dish is None:
            return -5, 404
        return dish

    def delete(self, id):
        deleted_result = self.dishes.delete_many({'ID': id})
        if deleted_result.deleted_count == 0:
            return -5, 404
        return id
