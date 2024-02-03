from services.discovery_service import DiscoveryService
from repositories.restaurants import RestaurantRepository
from fastapi import FastAPI, Depends
from mangum import Mangum

app = FastAPI()


def get_discovery_service():
    return DiscoveryService(RestaurantRepository())


def create_payload(popular, new, nearby):
    sections = []

    if popular:
        sections.append({"title": "Popular Restaurants", "restaurants": popular})
    if new:
        sections.append({"title": "New Restaurants", "restaurants": new})
    if nearby:
        sections.append({"title": "Nearby Restaurants", "restaurants": nearby})

    return {"sections": sections}


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
