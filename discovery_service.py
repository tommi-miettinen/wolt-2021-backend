from restaurants import restaurants as data
from geopy.distance import geodesic

def get_most_popular_restaurants(latlng: tuple, take: int):
    filtered_sorted_data = sorted(
        [restaurant for restaurant in data if geodesic((restaurant["location"][0], restaurant["location"][1]), latlng).kilometers <= 1.5],
        key=lambda x: x['popularity'], reverse=True
    )
    return filtered_sorted_data[:take]

def get_newest_restaurants(latlng: tuple, take: int):
    filtered_sorted_data = sorted(
        [restaurant for restaurant in data if geodesic((restaurant["location"][0], restaurant["location"][1]), latlng).kilometers <= 1.5],
        key=lambda x: x['launch_date'], reverse=True
    )
    return filtered_sorted_data[:take]


def get_nearby_restaurants(latlng:tuple,take:int):
    filtered_sorted_data = sorted(
        [restaurant for restaurant in data if geodesic((restaurant["location"][0], restaurant["location"][1]), latlng).kilometers <= 1.5],
        key=lambda x: geodesic((x["location"][0], x["location"][1]), latlng).kilometers
    )
    return filtered_sorted_data[:take]