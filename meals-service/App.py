from flask import Flask
from flask_restful import Api
from dishes.Dishes import Dishes
from dishes.DishesCollection import DishesCollection
from dishes.DishId import DishId
from dishes.DishName import DishName
from meals.Meals import Meals
from meals.MealsCollection import MealsCollection
from meals.MealsId import MealsId
from meals.MealsName import MealsName
import os

app = Flask(__name__)
api = Api(app)

meals_collection = MealsCollection()
dishes_collection = DishesCollection(meals_collection)
api.add_resource(Dishes, '/dishes', resource_class_kwargs={'dishes_collection': dishes_collection})
api.add_resource(DishId, '/dishes/<int:id>', resource_class_kwargs={'dishes_collection': dishes_collection})
api.add_resource(DishName, '/dishes/<string:name>', resource_class_kwargs={'dishes_collection': dishes_collection})
api.add_resource(Meals, '/meals', resource_class_kwargs={'meals_collection': meals_collection, 'dishes_collection': dishes_collection})
api.add_resource(MealsId, '/meals/<int:id>', resource_class_kwargs={'meals_collection': meals_collection, 'dishes_collection': dishes_collection})
api.add_resource(MealsName, '/meals/<string:name>', resource_class_kwargs={'meals_collection': meals_collection})

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 6000))
    host = str(os.environ.get("FLASK_RUN_HOST", '0.0.0.0'))
    app.run(host=host, port=port)
