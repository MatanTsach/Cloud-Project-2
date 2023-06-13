# Implements /dishes endpoint
from flask_restful import Resource, reqparse
from flask import request
import requests


class Dishes(Resource):

    def __init__(self, dishes_collection):
        self.dishes_collection = dishes_collection

    def get(self):
        return self.dishes_collection.dishes

    def post(self):
        parser = reqparse.RequestParser()
        content_type = request.headers.get("Content-Type")
        if not content_type or "application/json" not in content_type:
            return 0, 415

        parser.add_argument("name", type=str, location="json")
        args = parser.parse_args() 
        if not all(args.values()):
            return -1, 422

        dish_name = args['name']
        if self.dishes_collection.dish_exists(dish_name):
            return -2, 422
        
        dish_data = self.fetch_dish_data(dish_name)
        if dish_data == None:
            return -4, 504
        
        if len(dish_data.keys()) == 1:
            return -3, 422
        
        new_id = self.dishes_collection.add_dish(dish_data)
        return new_id, 201
        

    def fetch_dish_data(self, dish_name: str) -> dict:
        dish_data = dict()
        dish_data['name'] = dish_name
        api_url = f'https://api.api-ninjas.com/v1/nutrition?query={dish_name}'

        try:
            response = requests.get(api_url, headers={'X-Api-Key': 'ngqYnQOCZa6qeBJzyctYBA==XE7LlknD2VdlOgfe'})
        except:
            return None
        json_data = response.json()
        
        for dish in json_data:
            dish_data['cal'] = dish_data.get('cal', 0) + dish['calories']
            dish_data['size'] = dish_data.get('size', 0) + dish['serving_size_g']
            dish_data['sodium'] = dish_data.get('sodium', 0) + dish['sodium_mg']
            dish_data['sugar'] = dish_data.get('sugar', 0) + dish['sugar_g']
        return dish_data
    
    def delete(self):
        response_message = "This method is not allowed for the requested URL"
        return response_message, 405
        