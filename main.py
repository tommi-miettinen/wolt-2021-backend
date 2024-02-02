from services.discovery_service import DiscoveryService
from fastapi import FastAPI
from restaurants import restaurants as data

app = FastAPI()


discovery_service = DiscoveryService(data)


def create_payload(popular, new, nearby):
    return {
        "sections": [
            {"title": "Popular Restaurants", "restaurants": popular},
            {"title": "New Restaurants", "restaurants": new},
            {"title": "Nearby Restaurants", "restaurants": nearby},
        ]
    }


@app.get("/restaurants/discovery")
def get_discovery(lat: float, lng: float):
    popular = discovery_service.get_most_popular_restaurants((lat, lng))
    new = discovery_service.get_newest_restaurants((lat, lng))
    nearby = discovery_service.get_nearby_restaurants((lat, lng))

    payload = create_payload(popular=popular, new=new, nearby=nearby)

    return payload
