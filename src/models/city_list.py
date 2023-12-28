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
    def from_csv(cls, city_file: str, depot_name_list: List[str] = []) -> 'CityList':
        """
        Creates a CityList instance from a CSV file.

        Args:
            city_file (str): The path to the CSV file containing city data.
            depot_name_list (str): Names of cities which are depots.

        Returns:
            CityList: A new CityList instance containing cities from the file.

        The CSV file should have columns corresponding to 'city', 'order', '
        latitude', and 'longitude'.
        Rows where 'city' matches 'depot_name' will be marked as depots.
        """

        cities = []
        with open(city_file, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                city = City(
                    name=row['city'],
                    order=int(row['order']),
                    lat=float(row['latitude']),
                    lon=float(row['longitude']), 
                    is_depot=(True if row['is_depot'] == 'True' else False)
                )
                cities.append(city)
        return cls(cities)

    @classmethod
    def from_dict_list(cls, city_list: List[Dict]) -> 'CityList':
        """
        Create a CityList instance from a list of dictionaries.     
        Args:
            city_list (List[Dict]): A list of dicts, each representing a city.      
        Returns:
            CityList: A new CityList instance.      
        Each dictionary in 'city_list' should have keys for 'name', 'order', 
        'lat', 'lon', and 'is_depot'.
        """
        cities = [City(**city_dict) for city_dict in city_list]
        return cls(cities)

    @property
    def random_depot(self):
        return random.choice(self.depot_list)

    @property
    def depot_list(self):
        """
        Get a CityList containing only the depot cities.

        Returns:
            CityList: A new CityList instance containing only the depots.
        """
        depot_list = [item for item in self._items if item.is_depot]
        return CityList(depot_list)
    
    @property
    def depot(self):
        """
        Get the first depot city from the CityList.

        Returns:
            City: The first depot city if available, otherwise None.
        """
        depots = self.depot_list
        if depots: 
            return depots[0]
        else: 
            return
    
    def find_closest_neighbor(self, city):
        non_depots = [n for n in self._items if not n.is_depot and not n.name == city.name]
        random.shuffle(non_depots)
        closest_neighbor = None
        neighbor_distance = 9999999 # magic number
        for neighbor in non_depots:
            distance = city.calculate_distance_to(neighbor)
            if distance < neighbor_distance:
                closest_neighbor = neighbor
                neighbor_distance = distance 
        return closest_neighbor

    
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
        City(name="Warsaw", order=150, lat=52.2297, lon=21.0122, is_depot=False)
    ]
    # Create CityList from existing list
    city_list = CityList(cities)
    depots = city_list.depot_list
    print(depots)

    # # Iterate through CityList
    # for city in city_list:
    #     print(city)

    print(city_list.find_closest_neighbor(cities[0]))
    # Create CityList from a CSV file
    city_list_from_csv = CityList.from_csv("./src/temp/orders_with_depots.csv")


    # print(city_list_from_csv)
    # print(city_list_from_csv.depot_list)
    # Iterate and print cities
    # for city in city_list_from_csv:
    #     print(city)


    # # List of dictionaries representing cities
    # city_dicts = [
    #     {"name": "Kraków", "order": 100, "lat": 50.0647, "lon": 19.9450, "is_depot": True},
    #     {"name": "Warsaw", "order": 150, "lat": 52.2297, "lon": 21.0122, "is_depot": False}
    # ]

    # # Create CityList from dictionaries
    # city_list_from_dicts = CityList.from_dict_list(city_dicts)

    # # Iterate and print cities
    # for city in city_list_from_dicts:
    #     print(city)

    # # Create an empty CityList
    # empty_city_list = CityList()

    # # Append cities
    # empty_city_list.append(City(
    #     name="Gdańsk", order=50, lat=54.3520, lon=18.6466, is_depot=False))

    # # Iterate and print cities
    # for city in empty_city_list:
    #     print(city)