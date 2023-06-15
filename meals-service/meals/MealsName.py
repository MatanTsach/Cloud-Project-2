# Implements /meals/{NAME} endpoint
from flask_restful import Resource
from flask import jsonify
import json

class MealsName(Resource):
    def __init__(self, db):
        self.db = db
        self.meals = self.db['meals']

    def get(self, name):
        meal = self.meals.find_one({'name': name}, {'_id': 0})
        if meal is None:
            return -5, 404
        
        return jsonify(json.loads(json.dumps(meal, default=str)))
    
    def delete(self, name):
        meal = self.meals.find_one({'name': name})
        if meal is None:
            return -5, 404
        
        meal_id = meal['ID']
        self.meals.delete_one({'ID': meal_id})
        return meal_id
