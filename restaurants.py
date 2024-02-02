import json
from models.restaurant import Restaurant

with open("restaurants.json", "r") as file:
    data = json.load(file)
    json_restaurants = data["restaurants"]

restaurants = [Restaurant.from_dict(item) for item in json_restaurants]
