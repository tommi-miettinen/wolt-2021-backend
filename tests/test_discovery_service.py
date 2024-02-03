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


older_than_4_months_date = (
    datetime.now() - relativedelta(months=4) + relativedelta(days=1)
).strftime("%Y-%m-%d")


mock_data = [
    {
        "blurhash": "",
        "name": "Restaurant 1",
        "location": (1, 1),
        "popularity": 5,
        "online": True,
        "launch_date": "2022-01-01",
    },
    {
        "blurhash": "",
        "name": "Restaurant 2",
        "location": (1, 1),
        "online": True,
        "popularity": 10,
        "launch_date": "2022-02-01",
    },
    {
        "blurhash": "",
        "launch_date": older_than_4_months_date,
        "location": [1, 1],
        "name": "Old Restaurant",
        "online": True,
        "popularity": 0.3919633748546864,
    },
]


class MockRepository:
    def get_restaurants(self):
        return [Restaurant(**x) for x in mock_data]


discovery_service = DiscoveryService(MockRepository())


def test_get_most_popular_restaurants():
    restaurants = discovery_service.get_most_popular_restaurants((1, 1))
    assert len(restaurants) == 3


def test_get_newest_restaurants():
    restaurants = discovery_service.get_newest_restaurants((1, 1))
    assert len(restaurants) == 2


def test_popular_restaurants_are_sorted_by_highest_popularity():
    restaurants = discovery_service.get_most_popular_restaurants((1, 1))
    assert restaurants[0].popularity >= restaurants[1].popularity


def test_newest_restaurants_are_sorted_by_launch_date():
    restaurants = discovery_service.get_newest_restaurants((1, 1))
    assert restaurants[0].launch_date >= restaurants[1].launch_date


def test_create_payload_should_not_return_empty_sections():
    result = create_payload(popular=[], new=mock_data, nearby=mock_data)
    assert {"title": "Popular Restaurants"} not in result["sections"]


def test_newest_restaurant_doesnt_return_older_than_4_months():
    restaurants = discovery_service.get_newest_restaurants((1, 1))
    older_than_4_months_date = (datetime.now() - relativedelta(months=4)).date()

    for restaurant in restaurants:
        restaurant_launch_date = datetime.strptime(
            restaurant.launch_date, "%Y-%m-%d"
        ).date()
        assert restaurant_launch_date >= older_than_4_months_date