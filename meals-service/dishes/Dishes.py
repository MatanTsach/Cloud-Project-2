# Implements /dishes endpoint
from flask_restful import Resource, reqparse
from flask import request
from flask import jsonify
import json
import requests


class Dishes(Resource):

    def __init__(self, db):
        self.db = db
        self.dishes = db['dishes']
        
        if self.dishes.find_one({'_id': 0}) is None:
            self.dishes.insert_one({"_id": 0, 'key': 0})

    def get(self):
        results = self.dishes.find({"_id": {"$ne": 0}}, {"_id": 0})
        json_objects = [json.loads(json.dumps(result, default=str)) for result in results]
        return jsonify(json_objects)

    def post(self):
        required_args = {
            'name': str
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

        dish_name = request_args['name']
        if self.dishes.find_one({'name': dish_name}):
            return -2, 422
        
        dish_data = self.fetch_dish_data(dish_name)
        if dish_data == None:
            return -4, 504
        
        if len(dish_data.keys()) == 1:
            return -3, 422
        
        document = {'_id': 0}
        new_id = self.dishes.find_one(document)['key'] + 1
        dish_data['ID'] = new_id
        self.dishes.update_one(document, {'$set': {'key': new_id}})
        self.dishes.insert_one(dish_data)
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