import json
from models.restaurant import Restaurant


class RestaurantRepository:
    def __init__(self, filepath="restaurants.json"):
        self.restaurants = self.load_restaurants(filepath)

    def load_restaurants(self, filepath) -> list[Restaurant]:
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
                json_restaurants = data["restaurants"]
                return [Restaurant(**x) for x in json_restaurants]

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading restaurant data: {e}")
            return []

    def get_restaurants(self):
        return self.restaurants
