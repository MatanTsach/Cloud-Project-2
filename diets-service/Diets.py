# Implements /diets endpoint
from flask_restful import Resource, reqparse
from flask import request
import requests


class Diets(Resource):

    def __init__(self, dishes_collection):
        self.dishes_collection = dishes_collection

    def get(self):
        return self.dishes_collection.dishes