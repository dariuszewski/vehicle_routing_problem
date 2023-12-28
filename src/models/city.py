from math import radians, sin, asin, cos, sqrt

    
class City():
    def __init__(
            self, name: str, order: int, lat: float, lon: float, is_depot: bool
            ) -> None:
        """
        Initialize a new City instance.

        Args:
        name (str): The name of the city.
        order (int): The order quantity associated with the city.
        lat (float): The latitude of the city.
        lon (float): The longitude of the city.
        is_depot (bool): Flag indicating whether the city is a depot.
        """
        self.name = name
        self.order = order
        self.lat = lat
        self.lon = lon
        self.is_depot = is_depot


    def calculate_distance_to(self, other):
        """
        Calclulates distance to another city using Haversine formula.

        Args:
        other (City): The other city to which the distance is calculated.

        Returns:
        float: The distance to the other city in kilometers.    
        """
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(
            radians, [self.lon, self.lat, other.lon, other.lat]
            )
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371 # Radius of Earth in kilometers
        return c * r

    def to_dict(self):
        return {
            'city': self.name,
            'lat': self.lat,
            'lon': self.lon,
            'order': self.order,
            'is_depot': self.is_depot
        }

    def __repr__(self):
        return f"<City: {self.name}, order: {self.order}, is_depot: {self.is_depot}>"

    def __str__(self):
        return f"{self.name}, order: {self.order}"


if __name__ == "__main__":
    print("Testing City class...")
    depot = City("Depot", 0, 40.7128, -74.0060, True)  # New York
    city1 = City("City1", 10, 34.0522, -118.2437, False)  # Los Angeles
    city2 = City("City2", 20, 41.8781, -87.6298, False)  # Chicago
    print("Distance Depot to City1:", depot.calculate_distance_to(city1))
    print("Distance City1 to City2:", city1.calculate_distance_to(city2))