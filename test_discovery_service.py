import pytest
import services.discovery_service as discovery_service
from datetime import datetime
from dateutil.relativedelta import relativedelta
from main import create_payload

mock_data = [
    {
        "name": "Restaurant 1",
        "location": (1, 1),
        "popularity": 5,
        "online": True,
        "launch_date": "2022-01-01",
    },
    {
        "name": "Restaurant 2",
        "location": (1, 1),
        "online": True,
        "popularity": 10,
        "launch_date": "2022-02-01",
    },
]


@pytest.fixture
def mock_data_import(monkeypatch):
    monkeypatch.setattr("services.discovery_service.data", mock_data)


def test_get_most_popular_restaurants(mock_data_import):
    restaurants = discovery_service.get_most_popular_restaurants((1, 1))
    assert len(restaurants) == 2


def test_get_newest_restaurants(mock_data_import):
    restaurants = discovery_service.get_newest_restaurants((1, 1))
    assert len(restaurants) == 2


def test_popular_restaurants_are_sorted_by_highest_popularity(mock_data_import):
    restaurants = discovery_service.get_most_popular_restaurants((1, 1))
    assert restaurants[0]["popularity"] >= restaurants[1]["popularity"]


def test_newest_restaurants_are_sorted_by_launch_date(mock_data_import):
    restaurants = discovery_service.get_newest_restaurants((1, 1))
    assert restaurants[0]["launch_date"] >= restaurants[1]["launch_date"]


def test_create_payload():
    result = create_payload(popular=[], new=mock_data, nearby=mock_data)
    assert {"title": "Popular Restaurants"} not in result["sections"]


@pytest.fixture
def mock_newest_data(monkeypatch):
    older_than_4_months_date = (
        datetime.now() - relativedelta(months=4) + relativedelta(days=1)
    ).strftime("%Y-%m-%d")
    data = [
        {
            "launch_date": older_than_4_months_date,
            "location": [1, 1],
            "name": "Old Restaurant",
            "online": True,
            "popularity": 0.3919633748546864,
        },
    ]
    monkeypatch.setattr("services.discovery_service.data", data)


def test_newest_restaurant_doesnt_return_older_than_4_months(mock_newest_data):
    restaurants = discovery_service.get_newest_restaurants((1, 1))
    assert len(restaurants) == 0
