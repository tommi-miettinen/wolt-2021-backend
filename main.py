from services.discovery_service import DiscoveryService
from repositories.restaurants import RestaurantRepository
from fastapi import FastAPI, Depends


app = FastAPI()


def get_discovery_service():
    return DiscoveryService(RestaurantRepository())


def create_payload(popular, new, nearby):
    return {
        "sections": [
            {"title": "Popular Restaurants", "restaurants": popular},
            {"title": "New Restaurants", "restaurants": new},
            {"title": "Nearby Restaurants", "restaurants": nearby},
        ]
    }


@app.get("/discovery")
def get_discovery(
    lat: float,
    lng: float,
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    popular = discovery_service.get_most_popular_restaurants((lat, lng))
    new = discovery_service.get_newest_restaurants((lat, lng))
    nearby = discovery_service.get_nearby_restaurants((lat, lng))

    payload = create_payload(popular=popular, new=new, nearby=nearby)

    return payload
