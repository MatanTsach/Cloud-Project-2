# Implements /meals endpoint
from flask_restful import Resource, reqparse
from flask import request
import json

class Meals(Resource):

    def __init__(self, db):
        self.db = db
        self.meals = db['meals']
        
        if self.meals.find_one({'_id': 0}) is None:
            self.meals.insert_one({"_id": 0, 'key': 0})

    def get(self):
        return [json.dumps(document, default=str) for document in self.meals.find()]

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
        document = {'_id': 0}
        new_id = self.meals.find_one(document)['key'] + 1
        meal_data['ID'] = new_id
        self.meals.update_one(document, {'$set': {'key': new_id}})
        self.meals.insert_one(meal_data)
        return new_id, 201
    
    def delete(self):
        response_message = "This method is not allowed for the requested URL"
        return response_message, 405
        