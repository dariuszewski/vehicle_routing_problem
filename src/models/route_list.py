from typing import List

try:
    from src.models.iterable import Iterable
    from src.models.route import Route
    from src.models.city import City
except:
    from iterable import Iterable
    from route import Route
    from city import City

class RouteList(Iterable):
    def __init__(self, route: Route):
        """
        Initialize a RouteList with an initial route.

        Args:
            route (Route): The initial route to add to the route list.
        """
        super().__init__([route])

    @property
    def last(self) -> Route:
        """
        Get the last route in the route list.

        Returns:
            Route: The last route object.
        """
        if self._items:
            return self._items[-1]
        return None

    @property
    def last_city(self) -> City:
        """
        Get the last city in the last route.

        Returns:
            City: The last city in the last route.
        """
        if self.last:
            return self.last[-1]
        return None

    @property
    def length(self) -> float:
        """
        Calculates the total length of all routes.

        Returns:
            float: The total distance of all routes.
        """
        return round(sum(route.length for route in self._items), 3)

    def add_route(self, start):
        """
        Add a new route to the route list.

        Args:
            route (Route): The route to add.
        """
        if isinstance(start, Route):
            self._items.append(start)
        else:
            self._items.append(Route(start))

    def add_city(self, city: City):
        """
        Add a city to the last route in the route list.

        Args:
            city (City): The city to add.
        """
        if self.last:
            self.last.add_city(city)

    def complete_route(self, depot: City):
        """
        Complete the last route by returning to the depot.

        Args:
            depot (City): The depot to return to.
        """
        if self.last and (not self.last.is_empty) and (self.last_city != depot):
            self.last.add_city(depot)
    
    def get_all_valid_routes(self):
        valid_routes = []
        for route in self._items:
            if not all(city.is_depot for city in route):
                valid_routes.append(route)
        return valid_routes

    def __str__(self) -> str:
        return "\n".join(str(route) for route in self._items)

    def __repr__(self) -> str:
        return f"<RouteList: {len(self._items)} routes>"

if __name__ == "__main__":
    # Create some City instances
    depot = City("Depot", 0, 42.0, -77.0, True)
    city1 = City("City1", 10, 40.0, -75.0, False)
    city2 = City("City2", 20, 41.0, -76.0, False)
    city3 = City("City3", 15, 43.0, -78.0, False)

    # Initialize a Route with the depot
    initial_route = Route(depot)

    # Create a RouteList with the initial route
    route_list = RouteList(initial_route)

    # Add a city to the current route
    print('here')
    route_list.add_city(city1)

    # Complete the current route and start a new one
    new_route = Route(depot)
    route_list.add_route(new_route)
    print(route_list)

    # Add more cities to the new route
    route_list.add_city(city2)
    route_list.add_city(city3)


    # Print the route list details
    print("Route List Details:")
    print(route_list)

    # Print total length of all routes
    print(f"Total Length of All Routes: {route_list.length}")

    print(route_list[0].is_empty)
