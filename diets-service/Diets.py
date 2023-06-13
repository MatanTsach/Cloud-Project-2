from flask import Flask
from flask_restful import Api, Resource, reqparse

class Diets(Resource):
    def __init__(self, db):
        self.diets_collection = db['diets']

    def get(self):
        return diets_collection

    def post(self):
        new_diet = request.get_json()
        if not new_diet.get('name') or not new_diet.get('cal') or not new_diet.get('sodium') or not new_diet.get('sugar'):
            return {"message": "Missing required fields. Please provide 'name', 'cal', 'sodium', and 'sugar'."}, 400

        required_fields = ['name', 'cal', 'sodium', 'sugar']
        if len(new_diet) != len(required_fields):
            return {"message": "Invalid number of fields. Please provide all the required fields."}, 400

        diet_name = args['name']
        existing_diet = diets_collection.find_one({'name': diet_name})
        if existing_diet:
            return {"message": f"Diet with name '{diet_name}' already exists."}, 409

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('cal', type=int, required=True)
        parser.add_argument('sodium', type=int, required=True)
        parser.add_argument('sugar', type=int, required=True)
        args = parser.parse_args()

        errors = []

        if not isinstance(args['name'], str):
            errors.append("'name' should be a string.")

        if not isinstance(args['cal'], int):
            errors.append("'cal' should be an integer.")

        if not isinstance(args['sodium'], int):
            errors.append("'sodium' should be an integer.")

        if not isinstance(args['sugar'], int):
            errors.append("'sugar' should be an integer.")

        if errors:
            return {"message": "Invalid request payload.", "errors": errors}, 400    

        diets_collection.insert_one(new_diet)
        return {"message": "Diet added successfully"}, 201    


