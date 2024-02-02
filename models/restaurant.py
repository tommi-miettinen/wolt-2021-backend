from pydantic import BaseModel
from typing import List


class Restaurant(BaseModel):
    blurhash: str
    launch_date: str
    location: List[float]
    name: str
    online: bool
    popularity: float
