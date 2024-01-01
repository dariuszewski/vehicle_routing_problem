from typing import Any, List, Dict

try:
    from src.models.iterable import Iterable
    from src.models.city import City
except:
    from iterable import Iterable
    from city import City


class Route(Iterable):
    def __init__(self, *args: City):
        """
        Initialize a Route with a variable number of City objects.

        Args:
            *args (City): An arbitrary number of City objects.
        """
        super().__init__(list(args))
        if args and args[0].is_depot:
            self.depot = args[0]
        else:
            raise BaseException("Route has to start with a depot.")

    @classmethod
    def from_list(cls, lst):
        """
        Create a Route instance from a list of cities and a depot.

        Args:
            lst (List[City]): The list of cities in the route.
            depot (City): The depot city.

        Returns:
            Route: A new Route instance.
        """
        if not lst or not lst[0].is_depot:
            raise BaseException("Route has to start with a depot.")
        return cls(*lst)

    @property
    def length(self) -> float:
        """
        Calculates the total length of the route.

        Returns:
            float: The total distance of the route.
        """
        total_distance = 0
        for i in range(len(self._items) - 1):
            distance = self._items[i].calculate_distance_to(self._items[i + 1])
            total_distance += distance
        return total_distance

    @property
    def is_empty(self) -> bool:
        """
        Check if route is empty.

        Returns:
            bool: True if route is empty.
        """
        return self.length <= 0

    @property
    def order(self) -> int:
        """
        Calculates the total order quantity in the route.

        Returns:
            int: The total order quantity.
        """
        return sum(city.order for city in self._items)

    def add_city(self, city):
        """
        Add a city to the route.

        Args:
            city (City): The city to add.
        """
        self._items.append(city)

    def merge_routes(self, other):
        self._items = self._items[:-1] + other._items[1:]

    def __str__(self):
        order_str = f"Order: {self.order}"
        len_str = f"Length: {self.length}"
        items_reprs = [f"{item.name} ({item.order})" for item in self._items]
        items_str = " -> ".join(items_reprs)
        return f"{order_str} | {len_str} | {items_str}"


if __name__ == "__main__":
    # Test City class
    depot = City("Depot", 0, 42.0, -77.0, True)
    cities = [
        depot,
        City("City1", 10, 40.0, -75.0, False),
        City("City2", 20, 41.0, -76.0, False),
    ]
    route = Route.from_list(cities)

    # Add a city
    new_city = City("City3", 15, 43.0, -78.0, False)
    route.add_city(new_city)
    print(route.is_empty)

    # Print route information
    print(route)

    # from city
    route = Route(depot)
    print(route.is_empty)
