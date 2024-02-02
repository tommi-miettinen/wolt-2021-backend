from typing import List


class Restaurant:
    def __init__(
        self,
        blurhash: str,
        launch_date: str,
        location: List[float],
        name: str,
        online: bool,
        popularity: float,
    ):
        self.blurhash = blurhash
        self.launch_date = launch_date
        self.location = location
        self.name = name
        self.online = online
        self.popularity = popularity

    @classmethod
    def from_dict(cls, data: dict) -> "Restaurant":
        return cls(
            blurhash=data["blurhash"],
            launch_date=data["launch_date"],
            location=data["location"],
            name=data["name"],
            online=data["online"],
            popularity=data["popularity"],
        )
