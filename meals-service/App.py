import os
from flask import Flask
from flask_restful import Api
from dishes.DishesId import DishesId
from dishes.DishesName import DishesName
from dishes.Dishes import Dishes
from meals.Meals import Meals
from meals.MealsId import MealsId
from meals.MealsName import MealsName
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
client = MongoClient('mongodb://mongo:27017')
db = client['Project2']

api.add_resource(Dishes, '/dishes', resource_class_kwargs={'db': db})
api.add_resource(DishesId, '/dishes/<int:id>', resource_class_kwargs={'db': db})
api.add_resource(DishesName, '/dishes/<string:name>', resource_class_kwargs={'db': db})
api.add_resource(Meals, '/meals', resource_class_kwargs={'db': db})
api.add_resource(MealsId, '/meals/<int:id>', resource_class_kwargs={'db': db})
api.add_resource(MealsName, '/meals/<string:name>', resource_class_kwargs={'db': db})

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 6000))
    host = str(os.environ.get("FLASK_RUN_HOST", '0.0.0.0'))
    app.run(host=host, port=port)
