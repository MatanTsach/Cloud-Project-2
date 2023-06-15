# Implements /dishes/{name} endpoint
from flask_restful import Resource
from flask import jsonify
import json
import MealModules

class DishesName(Resource):

    def __init__(self, db):
        self.db = db
        self.dishes = self.db['dishes']
    
    def get(self, name):
        dish = self.dishes.find_one({'name': name}, {'_id': 0})
        if dish is None:
            return -5, 404
        
        return jsonify(json.loads(json.dumps(dish, default=str)))
    
    def delete(self, name):
        dish = self.dishes.find_one({'name': name})
        if dish is None:
            return -5, 404
        
        dish_id = dish['ID']
        self.dishes.delete_one({'ID': dish_id})
        MealModules.update_meals(self.db['meals'], dish)
        return dish_id