import services.discovery_service as discovery_service

from fastapi import FastAPI

app = FastAPI()


@app.get("/restaurants/discovery")
def get_discovery(lat: float, lng: float):
    return {
        "sections": [
            {
                "title":"Popular Restaurants",
                "restaurants": discovery_service.get_most_popular_restaurants((lat, lng)),
            },
            {
                "title": "New Restaurants",
                "restaurants":discovery_service.get_newest_restaurants((lat, lng))
            },
            {
                "title":"Nearby Restaurants",
                "restaurants":discovery_service.get_nearby_restaurants((lat, lng))
            }
        ],
    }