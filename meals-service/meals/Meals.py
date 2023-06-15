# Implements /meals endpoint
from flask_restful import Resource
from flask import request, jsonify
import json
import MealModules
import requests

class Meals(Resource):

    def __init__(self, db):
        self.db = db
        self.meals = db['meals']
        
        if self.meals.find_one({'_id': 0}) is None:
            self.meals.insert_one({"_id": 0, 'key': 0})

    def get(self):
        diet_name = request.args.get('diet')

        if diet_name is None:
            results = self.meals.find({"_id": {"$ne": 0}}, {"_id": 0})
        else:
            url = f'http://diets:8000/diets/{diet_name}'
            response = requests.get(url)
            
            if response.status_code == 404:
                return f"Diet {diet_name} not found", 404
            
            response_json = response.json()
            print(response_json)
            results = self.meals.find(
            {
                "_id": {"$ne": 0},
                "cal": {"$lte": response_json['cal']},
                "sodium": {"$lte": response_json['sodium']},
                "sugar": {"$lte": response_json['sugar']}
            },
            {"_id": 0})

        json_objects = [json.loads(json.dumps(result, default=str)) for result in results]

        return jsonify(json_objects)

    def post(self):
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
        
        if self.meals.find_one({'name': request_args['name']}):
            return -2, 422
        
        for key, value in request_args.items():
            if key != 'name' and not self.db['dishes'].find_one({'ID': value}):
                return -6, 422
        
        meal_data = dict(request_args)
        meal_id = self.update_key()
        meal_data['ID'] = meal_id
        MealModules.add_meal_data(meal_data, self.db['dishes'])
        self.meals.insert_one(meal_data)

        return meal_id, 201
    
    def delete(self):
        response_message = "This method is not allowed for the requested URL"
        return response_message, 405
    
    def update_key(self):
        document = {'_id': 0}
        new_id = self.meals.find_one(document)['key'] + 1
        self.meals.update_one(document, {'$set': {'key': new_id}})
        return new_id
        