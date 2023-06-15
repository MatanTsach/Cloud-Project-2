from flask import jsonify, request
from flask_restful import Resource
import json
class Diets(Resource):
    def __init__(self, db):
        self.diets = db['diets']

        if self.diets.find_one({'_id': 0}) is None:
            self.diets.insert_one({"_id": 0, 'key': 0})

    def get(self):
        results = self.diets.find({"_id": {"$ne": 0}}, {"_id": 0})
        json_objects = [json.loads(json.dumps(result, default=str)) for result in results]
        return jsonify(json_objects)
    
    def post(self):
        required_args = {
            'name': str,
            'cal': (float, int),
            'sodium': (float, int),
            'sugar': (float, int)
        }

        content_type = request.headers.get("Content-Type")
        if not content_type or "application/json" not in content_type:
            return "POST expects content type to be application/json", 415
        
        request_args = request.get_json()
        if all(arg in request_args for arg in required_args) and len(request_args) == len(required_args):
            for arg, arg_type in required_args.items():
                if not isinstance(request_args[arg], arg_type):
                    return "Incorrect POST format", 422
        else:
            return "Incorrect POST format", 422
        
        diet_data = dict(request_args)
        if self.diets.find_one({'name': request_args['name']}):
            return f"Diet with name {diet_data['name']} already exists", 422

        self.diets.insert_one(diet_data)

        return f"Diet {diet_data['name']} was created successfully", 201


