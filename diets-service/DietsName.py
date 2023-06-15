from flask_restful import Resource
from flask import jsonify
import json

class DietsName(Resource):

    def __init__(self, db):
        self.diets = db['diets']

    def get(self, name):
        diet = self.diets.find_one({'name': name}, {'_id': 0})
        if diet is None:
            return -5, 404
        
        return jsonify(json.loads(json.dumps(diet, default=str)))