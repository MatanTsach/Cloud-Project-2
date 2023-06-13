# Implements /meals/{ID} endpoint
from flask_restful import Resource
from flask_restful import reqparse
from flask import request

class MealsId(Resource):

    def __init__(self, db):
        self.db = db
    
    def get(self, id):
        meal = self.meals_collection.get_meal(id)

        if meal is None:
            return -5, 404
        
        return meal
    
    def delete(self, id):
        deleted_id = self.meals_collection.delete_meal(id)

        if deleted_id == -1:
            return -5, 404
        
        return deleted_id
    
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
        
        
        return id, 200
    
    def update_meal_data(self, meal_data: dict, dishes_data: dict) -> None:
        dish_ids = [meal_data[key] for key in meal_data.keys() if key in self.courses] # to make sure i only take the dish ids
        self._reset_nutrients(meal_data)
        for dish_id in dish_ids:
            for nutrient in self.nutrients:
                meal_data[nutrient] = meal_data.get(nutrient, 0) + dishes_data[dish_id][nutrient]

    def reset_meal(self, meal: dict) -> None:
        for nutrient in self.nutrients:
            meal[nutrient] = None


        
