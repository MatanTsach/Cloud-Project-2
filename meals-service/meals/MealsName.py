# Implements /meals/{NAME} endpoint
from flask_restful import Resource


class MealsName(Resource):
    def __init__(self, db):
        self.db = db

    def get(self, name):
        pass
        """
        meal_id = self.meals_collection.get_meal_id(name)
        meal = self.meals_collection.get_meal(meal_id)
        if meal is None:
            return -5, 404
        return meal

    def delete(self, name):
        meal_id = self.meals_collection.get_meal_id(name)
        deleted_id = self.meals_collection.delete_meal(meal_id)
        if deleted_id == -1:
            return -5, 404
        return deleted_id
        """
