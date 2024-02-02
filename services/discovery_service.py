from geopy.distance import geodesic
from datetime import datetime
from dateutil.relativedelta import relativedelta
from models.restaurant import Restaurant


class DiscoveryService:
    def __init__(self, data: list[Restaurant]):
        self.data = data

    def get_distance(self, latlng1: tuple, latlng2: tuple):
        return geodesic(latlng1, latlng2).kilometers

    def get_restaurants_filtered_by_distance(
        self, latlng: tuple, threshold: float = 1.5
    ):
        return [
            x for x in self.data if self.get_distance(latlng, x.location) <= threshold
        ]

    def get_most_popular_restaurants(self, latlng: tuple, take: int = 10):
        restaurants_filtered_by_distance = self.get_restaurants_filtered_by_distance(
            latlng
        )
        restaurants_sorted_by_popularity = sorted(
            restaurants_filtered_by_distance,
            key=lambda x: (x.online, x.popularity),
            reverse=True,
        )
        return restaurants_sorted_by_popularity[:take]

    def get_newest_restaurants(self, latlng: tuple, take: int = 10):
        restaurants_filtered_by_distance = self.get_restaurants_filtered_by_distance(
            latlng
        )
        sorted_by_launch = sorted(
            restaurants_filtered_by_distance,
            key=lambda x: (-x.online, x.launch_date),
            reverse=True,
        )

        current_date = datetime.now()
        no_older_than = current_date - relativedelta(months=4)

        filtered_by_max_launch_date = [
            x
            for x in sorted_by_launch
            if datetime.strptime(x.launch_date, "%Y-%m-%d") < no_older_than
        ]
        return filtered_by_max_launch_date[:take]

    def get_nearby_restaurants(self, latlng: tuple, take: int = 10):
        restaurants_filtered_by_distance = self.get_restaurants_filtered_by_distance(
            latlng
        )
        sorted_by_distance = sorted(
            restaurants_filtered_by_distance,
            key=lambda x: (-x.online, self.get_distance(latlng, x.location)),
        )
        return sorted_by_distance[:take]
