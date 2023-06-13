# Implements /meals/{ID} endpoint
from flask_restful import Resource
from flask_restful import reqparse
from flask import request

class MealsId(Resource):

    def __init__(self, meals_collection, dishes_collection):
        self.meals_collection = meals_collection
        self.dishes_collection = dishes_collection
    
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
        parser = reqparse.RequestParser()

        if "application/json" not in request.headers.get("Content-Type"):
            return 0, 415

        parser.add_argument("name", type=str, location="json")
        parser.add_argument("appetizer", type=int, location="json")
        parser.add_argument("main", type=int, location="json")
        parser.add_argument("dessert", type=int, location="json")

        args = parser.parse_args()
        if not all(args.values()):
            return -1, 422
        
        dishes_data = self.dishes_collection.dishes
        for key, value in args.items():
            if key != 'name' and value not in dishes_data.keys():
                    return -6, 422   
        # Assuming the id of the meal already exists, according to the lecture.
        self.meals_collection.update_meal(id, dict(args),dishes_data)
        return id, 200


        
