from typing import Any, List

try:
    from src.models.iterable import Iterable
    from src.models.vehicle import Vehicle
    from src.models.city import City
except ImportError:
    from iterable import Iterable
    from vehicle import Vehicle
    from city import City


class Fleet(Iterable):
    def __init__(self, num_vehicles: int, vehicle_capacity: int, depot: City, city_list=None):
        """
        Initialize a Fleet with a specified number of vehicles.

        Args:
            num_vehicles (int): The number of vehicles in the fleet.
            vehicle_capacity (int): The capacity of each vehicle in the fleet.
            depot (City): The depot city where all vehicles start.
        
        State of the fleet is a solution of an algirithm.
        """
        super().__init__(self.build_fleet(num_vehicles, vehicle_capacity, depot, city_list))
        self.vehicle_capacity = vehicle_capacity
        self.num_vehicles = num_vehicles
        self.city_list = city_list

    def build_fleet(self, num_vehicles: int, vehicle_capacity: int, depot: City, city_list) -> List[Vehicle]:
        """
        Build a fleet of vehicles.

        Args:
            num_vehicles (int): The number of vehicles to create.
            vehicle_capacity (int): The capacity of each vehicle.
            depot (City): The depot city for each vehicle.

        Returns:
            List[Vehicle]: A list of vehicles.
        """
        return [Vehicle(capacity=vehicle_capacity, depot=depot) for _ in range(num_vehicles)]
    
    @classmethod
    def from_list(cls, items: List[Vehicle]) -> 'Fleet':
        """
        Build a fleet of vehicles from a list of vehicles.

        Args:
            List[Vehicle]: A list of vehicles.
        """
        fleet = cls(0, 0, None)  # Create an empty Fleet instance
        fleet._items = items     # Set the provided list of vehicles
        return fleet

    @property
    def distance_covered(self) -> float:
        """
        Calculate the total distance covered by all vehicles in the fleet.

        Returns:
            float: The total distance covered.
        """
        return round(
            sum(vehicle.route_list.length for vehicle in self._items), 3
        )

    def get_all_valid_routes(self) -> List[Any]:
        """
        Get all valid routes from all vehicles in the fleet. Valid route is
        one which doesn't contain only depots.

        Returns:
            List[Any]: A list of all routes.
        """
        routes = []
        for vehicle in self._items:
            routes.extend(vehicle.get_all_valid_routes())
        return routes

    def get_all_routes(self) -> List[Any]:
        """
        Get all valid routes from all vehicles in the fleet. Valid route is
        one which doesn't contain only depots.

        Returns:
            List[Any]: A list of all routes.
        """
        routes = []
        for vehicle in self._items:
            routes.extend(vehicle.route_list)
        return routes
    
    def get_route_by_city(self, city):
        routes = self.get_all_routes()
        for route in routes:
            if city in route:
                return route
    

if __name__ == "__main__":
    # Assuming you have a list of Vehicle instances
    depot = City("Depot", 0, 40.7128, -74.0060, True) 
    existing_vehicles = [Vehicle(25, depot), Vehicle(30, depot)]

    # Create a Fleet from the existing list of vehicles
    fleet = Fleet.from_list(existing_vehicles)

    # Display information about the fleet
    print("Fleet Details:")
    print(fleet)

    # Print total distance covered by the fleet
    print(f"Total Distance Covered: {fleet.distance_covered}")
