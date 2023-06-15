import os
from flask import Flask
from flask_restful import Api
from Diets import Diets
from DietsName import DietsName
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
client = MongoClient('mongodb://mongo:27017')
db = client['Project2']

api.add_resource(Diets, '/diets', resource_class_kwargs={'db': db})
api.add_resource(DietsName, '/diets/<string:name>', resource_class_kwargs={'db': db})

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 6000))
    host = str(os.environ.get("FLASK_RUN_HOST", '0.0.0.0'))
    app.run(host=host, port=port)
