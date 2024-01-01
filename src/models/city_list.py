import csv
import random
from typing import List, Dict

import pandas as pd

try:
    from src.models.iterable import Iterable
    from src.models.city import City
except ImportError:
    from iterable import Iterable
    from city import City


class CityList(Iterable):
    """
    Represents a list of cities, with functionality to create instances.
    It is a singleton-like object with an exception of CityList of depots.

    Attributes:
        _items (List[City]): A list of City objects.
    """

    @classmethod
    def from_csv(cls, city_file: str) -> "CityList":
        """
        Creates a CityList instance from a CSV file.
        Args:
            city_file (str): The path to the CSV file containing city data.
        Returns:
            CityList: A new CityList instance containing cities from the file.

        The CSV file should have columns corresponding to 'city', 'order', '
        latitude', 'longitude' and 'is_depot.
        """

        cities = []
        with open(city_file, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                city = City(
                    name=row["city"],
                    order=int(row["order"]),
                    lat=float(row["latitude"]),
                    lon=float(row["longitude"]),
                    is_depot=(True if row["is_depot"] == "True" else False),
                )
                cities.append(city)
        return cls(cities)

    @property
    def depot(self):
        """
        Get any depot city from the CityList.

        Returns:
            City: The first depot city if available, otherwise None.
        """
        depot_list = [item for item in self._items if item.is_depot]
        if depot_list:
            return depot_list[0]
        return

    def find_nearest_from_list(self, city, lst):
        closest_neighbor = None
        neighbor_distance = 9999999  # magic number
        for neighbor in lst:
            distance = city.calculate_distance_to(neighbor)
            if distance < neighbor_distance:
                closest_neighbor = neighbor
                neighbor_distance = distance
        return closest_neighbor

    def find_nearest_neighbor(self, city):
        non_depots = [c for c in self._items if not c.is_depot and c != city]
        return self.find_nearest_from_list(city, non_depots)

    def find_nearest_depot(self, city):
        depots = [c for c in self._items if c.is_depot]
        return self.find_nearest_from_list(city, depots)

    def __repr__(self):
        rows = [city.to_dict() for city in self._items]
        df = pd.DataFrame(rows)
        return str(df)

    def __str__(self):
        rows = [city.to_dict() for city in self._items]
        df = pd.DataFrame(rows)
        return str(df)


if __name__ == "__main__":
    from iterable import Iterable
    from city import City

    # Test City class
    print("Testing CityList class...")
    # Assuming you have a list of City objects
    cities = [
        City(name="Kraków", order=100, lat=50.0647, lon=19.9450, is_depot=True),
        City(name="Warsaw", order=150, lat=52.2297, lon=21.0122, is_depot=False),
    ]
    # Create CityList from existing list
    city_list = CityList(cities)
    depots = city_list.depot
    print(depots)

    city_list_from_csv = CityList.from_csv("./data/orders_with_depots.csv")
