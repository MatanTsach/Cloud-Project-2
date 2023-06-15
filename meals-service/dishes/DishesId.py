# Implements /dishes/{ID} endpoint
from flask_restful import Resource
from flask import jsonify
import json
import MealModules

class DishesId(Resource):
    
    def __init__(self, db):
        self.db = db
        self.dishes = db['dishes']

    def get(self, id):
        dish = self.dishes.find_one({'ID': id}, {"_id": 0})
        if dish is None:
            return -5, 404
        
        return jsonify(json.loads(json.dumps(dish, default=str)))

    def delete(self, id):
        dish = self.dishes.find_one({'ID': id}, {"_id": 0})

        if dish is None:
            return -5, 404
        
        self.dishes.delete_one({'ID': id})
        MealModules.update_meals(self.db['meals'], dish)
        
        return id
