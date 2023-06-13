class DietsByName(Resource):

    def __init__(self, client):
        self.diets_collection = db['diets']

    def get(self, name):
        diet = diets_collection.find_one({'name': name})
        if diet:
            return diet
        return {"message": "Diet not found"}, 404