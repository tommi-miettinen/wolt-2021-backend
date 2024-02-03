import os
import sys

current_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
os.chdir(root_dir)
sys.path.append(root_dir)


from services.discovery_service import DiscoveryService
from datetime import datetime
from dateutil.relativedelta import relativedelta
from main import create_payload
from models.restaurant import Restaurant
from geopy.distance import geodesic

current_date = datetime.now()

older_than_4_months_date = (
    current_date - relativedelta(months=4) + relativedelta(days=1)
).strftime("%Y-%m-%d")


user_location = (0, 0)
destination_point = geodesic(meters=1501).destination((0, 0), 90)
lat, lng = destination_point.latitude, destination_point.longitude
location_that_is_1500meters_away_from_00 = (lat, lng)


mock_data = [
    {
        "blurhash": "",
        "name": "Restaurant 1",
        "location": user_location,
        "online": True,
        "popularity": 1,
        "launch_date": current_date.strftime("%Y-%m-%d"),
    },
    {
        "blurhash": "",
        "name": "Restaurant 2",
        "location": user_location,
        "online": True,
        "popularity": 3,
        "launch_date": current_date.strftime("%Y-%m-%d"),
    },
    {
        "blurhash": "",
        "launch_date": current_date.strftime("%Y-%m-%d"),
        "location": location_that_is_1500meters_away_from_00,
        "name": "Restaurant that is 1501 meters away",
        "online": True,
        "popularity": 2,
    },
    {
        "blurhash": "",
        "name": "Restaurant 2",
        "location": user_location,
        "online": True,
        "popularity": 3,
        "launch_date": older_than_4_months_date,
    },
]


class MockRepository:
    def __init__(self, data):
        self.data = data

    def get_restaurants(self):
        return [Restaurant(**x) for x in self.data]


def test_popular_restaurants_are_sorted_by_highest_popularity():
    discovery_service = DiscoveryService(MockRepository(mock_data))
    restaurants = discovery_service.get_most_popular_restaurants((user_location))
    assert restaurants[0].popularity >= restaurants[1].popularity


def test_newest_restaurants_are_sorted_by_launch_date():
    discovery_service = DiscoveryService(MockRepository(mock_data))
    restaurants = discovery_service.get_newest_restaurants((user_location))
    assert restaurants[0].launch_date >= restaurants[1].launch_date


def test_newest_restaurants_doesnt_include_restaurants_older_than_4_months():
    discovery_service = DiscoveryService(MockRepository(mock_data))
    restaurants = discovery_service.get_newest_restaurants((user_location))
    assert all(
        restaurant.launch_date >= older_than_4_months_date for restaurant in restaurants
    )


def test_create_payload_should_not_return_empty_sections():
    result = create_payload(popular=[], new=mock_data, nearby=mock_data)
    assert any(
        section["title"] != "Popular Restaurants" for section in result["sections"]
    )

    assert len(result["sections"]) == 2


def test_doesnt_return_restaurants_that_are_more_than_1500meters_from_the_user():
    discovery_service = DiscoveryService(MockRepository(mock_data))
    restaurants = discovery_service.get_nearby_restaurants(user_location)
    assert all(restaurant.location == [0, 0] for restaurant in restaurants)
