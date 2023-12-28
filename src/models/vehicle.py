try:
    from src.models.route import Route
    from src.models.route_list import RouteList
except ImportError:
    from route import Route
    from route_list import RouteList
    from city import City
    from city_list import CityList


class Vehicle(): 
    def __init__(self, capacity, depot):
        self.capacity = capacity
        self.trunk = capacity
        self.depot = depot
        self.route_list = RouteList(Route(depot))

    def can_deliver_order(self, city):
        return self.trunk >= city.order
    
    def visit_depot(self, depot):
        self.route_list.add_city(depot)
        self.route_list.add_route(Route(depot))
        self.trunk = self.capacity
    
    def back_to_depot(self, depot):
        self.route_list.add_city(depot)
        self.trunk = self.capacity

    def deliver_order(self, city, city_list):
        if self.can_deliver_order(city):
            self.trunk -= city.order
            self.route_list.add_city(city)
        else:
            depot = city_list.random_depot
            self.visit_depot(depot)
            self.route_list.add_city(depot)
    
    def get_all_valid_routes(self):
        return self.route_list.get_all_valid_routes()

    @property
    def position(self):
        return self.route_list.last_city
    
    @property
    def distance_travelled(self):
        return self.route_list.length
    
    def __str__(self):
        return f'<Vehicle: capacity: {self.trunk}/{self.capacity}, position: {self.position}, travel: {self.distance_travelled} >'
    
    def __repr__(self):
        return f'<Vehicle: capacity: {self.trunk}/{self.capacity}, position: {self.position}, travel: {self.distance_travelled} >'
    

if __name__ == "__main__":
    # Create City and Depot instances
    depot1 = City("Depot1", 0, 42.0, -77.0, True)
    depot2 = City("Depot2", 0, 43.0, -78.0, True)
    city1 = City("City1", 10, 40.0, -75.0, False)
    city2 = City("City2", 20, 41.0, -76.0, False)
    city3 = City("City3", 30, 39.0, -74.0, False)

    # Create a CityList including the depots and cities
    city_list = CityList.from_dict_list([
        {"name": "Depot1", "order": 0, "lat": 42.0, "lon": -77.0, "is_depot": True},
        {"name": "Depot2", "order": 0, "lat": 43.0, "lon": -78.0, "is_depot": True},
        {"name": "City1", "order": 10, "lat": 40.0, "lon": -75.0, "is_depot": False},
        {"name": "City2", "order": 20, "lat": 41.0, "lon": -76.0, "is_depot": False},
        {"name": "City3", "order": 30, "lat": 39.0, "lon": -74.0, "is_depot": False},
    ])

    # Initialize a Vehicle with a capacity and a starting depot
    vehicle = Vehicle(25, depot1)
    print(vehicle)
    print(vehicle.route_list)
    # vehicle.deliver_order(city1, city_list)
    # vehicle.deliver_order(city3, city_list)
    # Simulate delivering orders to different cities
    # for city in [city1, city2, city3]:
    #     vehicle.deliver_order(city, city_list)

    # Print the vehicle's route list details
    # print("Vehicle's Route List Details:")
    # print(vehicle)