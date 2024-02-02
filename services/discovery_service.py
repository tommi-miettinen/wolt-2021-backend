from restaurants import restaurants as data
from geopy.distance import geodesic
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_distance(latlng1: tuple, latlng2: tuple):
    return geodesic(latlng1, latlng2).kilometers


def get_restaurants_filtered_by_distance(latlng: tuple, threshold: float = 1.5):
    return [x for x in data if get_distance(latlng, x["location"]) <= threshold]


def get_most_popular_restaurants(latlng: tuple, take: int = 10):
    restaurants_filtered_by_distance = get_restaurants_filtered_by_distance(latlng)
    restaurants_sorted_by_popularity = sorted(
        restaurants_filtered_by_distance,
        key=lambda x: (x["online"], x["popularity"]),
        reverse=True,
    )
    return restaurants_sorted_by_popularity[:take]


def get_newest_restaurants(latlng: tuple, take: int = 10):
    restaurants_filtered_by_distance = get_restaurants_filtered_by_distance(latlng)
    sorted_by_launch = sorted(
        restaurants_filtered_by_distance,
        key=lambda x: (-x["online"], x["launch_date"]),
        reverse=True,
    )

    current_date = datetime.now()
    no_older_than = current_date - relativedelta(months=4)

    filtered_by_max_launch_date = [
        x
        for x in sorted_by_launch
        if datetime.strptime(x["launch_date"], "%Y-%m-%d") < no_older_than
    ]
    return filtered_by_max_launch_date[:take]


def get_nearby_restaurants(latlng: tuple, take: int = 10):
    restaurants_filtered_by_distance = get_restaurants_filtered_by_distance(latlng)
    sorted_by_distance = sorted(
        restaurants_filtered_by_distance,
        key=lambda x: (-x["online"], get_distance(latlng, x["location"])),
    )
    return sorted_by_distance[:take]
