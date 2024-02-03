# Wolt Summer 2021 Internship assignment

### FastAPI python backend for restaurant discovery feature.

#### Live demo 
https://wolt-backend-2021.azurewebsites.net/discovery?lat=24.935326&lng=60.155631

### Installation

```
python -m venv venv
```

```
.\venv\Scripts\activate
```

```
pip install -r requirements.txt
```

### Running locally

```
uvicorn main:app --reload
```

### Specification

_restaurants.json_ in the repository contains one hundred restaurants from the Helsinki area.

Your task is to create an **API endpoint** _/discovery_ that takes coordinates of the customer as an input and then **returns a page (JSON response)** containing _most popular, newest and nearby_ restaurants (based on given coordinates).

Location of a customer needs to be provided as **request parameters** _lat_ (latitude) and _lon_ (longitude), e.g. _/discovery?lat=60.1709&lon=24.941_. Both parameters accept float values.

An JSON object returned by the _/discovery_ -endpoint must have the following structure:

```
{
   "sections": [
      {
           "title": "Popular Restaurants",
           "restaurants": [.. add max 10 restaurant objects..]
      },
      {
           "title": "New Restaurants",
           "restaurants": [..add max 10 restaurant objects..]
      },
 	{
           "title": "Nearby Restaurants",
           "restaurants": [.. add max 10 restaurant objects..]
      }

   ]
}
```

For each _restaurants_-list you need to add **maximum 10** restaurant objects. A list can also contain fewer restaurants (or even be empty) if there are not enough objects matching given conditions. A section with an empty _restaurants_-list should be removed from the response.

**So how do you know which restaurants to add to each list?**

There are two main rules to follow:

- All restaurants returned by the endpoint must be **closer than 1.5 kilometers** from given coordinates, measured as a straight line between coordinates and the location of the restaurant.
- Open restaurants (_online=true_) are **more important** than closed ones. Every list must be first populated with open restaurants, and only adding closed ones if there is still capacity left.

In addition each list has a specific **sorting rule**:

- “Popular Restaurants”: highest _popularity_ value first (descending order)
- “New Restaurants”: Newest _launch_date_ first (descending). This list has also a special rule: _launch_date_ must be no older than 4 months.
- “Nearby Restaurants”: Closest to the given location first (ascending).

Remember to **cap each list to max. 10** best matching restaurants. The same restaurant can obviously be in multiple lists (if it matches given criteria).

See _discovery_page.json_ for an example of the format the API should return. **Note: the sample is not based on any particular location on the map, so the data there might not be accurate.**
