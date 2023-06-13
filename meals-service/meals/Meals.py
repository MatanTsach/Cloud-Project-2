# Implements /meals endpoint
from flask_restful import Resource, reqparse
from flask import request


class Meals(Resource):

    def __init__(self, meals_collection, dishes_collection):
        self.meals_collection = meals_collection
        self.dishes_collection = dishes_collection

    def get(self):
        return self.meals_collection.meals

    def post(self):
        parser = reqparse.RequestParser()
        content_type = request.headers.get("Content-Type")
        if not content_type or "application/json" not in content_type:
            return 0, 415
        
        parser.add_argument("name", type=str, location="json")
        parser.add_argument("appetizer", type=int, location="json")
        parser.add_argument("main", type=int, location="json")
        parser.add_argument("dessert", type=int, location="json")
        args = parser.parse_args()

        if not all(args.values()):
            return -1, 422
        
        if self.meals_collection.meal_exists(args['name']):
            return -2, 422
        
        dishes_data = self.dishes_collection.dishes
        for key, value in args.items():
            if key != 'name' and value not in dishes_data.keys():
                    return -6, 422
        
        meal_data = dict(args)
        meal_id = self.meals_collection.add_meal(meal_data, dishes_data)
        return meal_id, 201
    
    def delete(self):
        response_message = "This method is not allowed for the requested URL"
        return response_message, 405
        