import pytest
import services.discovery_service as discovery_service

mock_data = [
    {
        "name": "Restaurant 1",
        "location": (1, 1),
        "popularity": 5,
        "launch_date": "2022-01-01",
    },
    {
        "name": "Restaurant 2",
        "location": (1, 1),
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