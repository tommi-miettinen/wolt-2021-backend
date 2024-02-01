import services.discovery_service as discovery_service
from fastapi import FastAPI

app = FastAPI()

@app.get("/restaurants/discovery")
def get_discovery(lat: float, lng: float):
    popular = discovery_service.get_most_popular_restaurants((lat, lng))
    new = discovery_service.get_newest_restaurants((lat, lng))
    nearby = discovery_service.get_nearby_restaurants((lat, lng))
    
    sections = []
    
    if popular:
        sections.append({"title": "Popular Restaurants","restaurants": popular})
    if new:
        sections.append({"title": "New Restaurants","restaurants": new})
    if nearby:
        sections.append({"title": "Nearby Restaurants","restaurants": nearby})
    
    return {"sections": sections}