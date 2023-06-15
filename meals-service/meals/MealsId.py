# Implements /meals/{ID} endpoint
from flask_restful import Resource
from flask import request, jsonify
import json
import MealModules

class MealsId(Resource):

    def __init__(self, db):
        self.db = db
        self.meals = self.db['meals']
    
    def get(self, id):
        meal = self.meals.find_one({'ID': id}, {"_id": 0})
        if meal is None:
            return -5, 404
        
        return jsonify(json.loads(json.dumps(meal, default=str)))
    
    def delete(self, id):
        deleted_result = self.meals.delete_one({'ID': id})
        if deleted_result.deleted_count == 0:
            return -5, 404
        
        return id
    
    def put(self, id):
        required_args = {
            'name': str,
            'appetizer': int,
            'main': int,
            'dessert': int
        }
        content_type = request.headers.get("Content-Type")
        if not content_type or "application/json" not in content_type:
            return 0, 415
        
        request_args = request.get_json()

        if all(arg in request_args for arg in required_args) and len(request_args) == len(required_args):
            for arg, arg_type in required_args.items():
                if not isinstance(request_args[arg], arg_type):
                    return -1, 422
        else:
            return -1, 422
        
        for key, value in request_args.items():
            if key != 'name' and not self.db['dishes'].find_one({'ID': value}):
                return -6, 422
            
        meal_data = dict(request_args)
        MealModules.add_meal_data(meal_data, self.db['dishes'])
        self.meals.update_one({'ID': id}, {'$set': meal_data})

        return id, 200


        
