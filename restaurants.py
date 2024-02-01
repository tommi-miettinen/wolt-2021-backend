import json

with open('restaurants.json', 'r') as file:
    data = json.load(file)
    restaurants = data['restaurants']