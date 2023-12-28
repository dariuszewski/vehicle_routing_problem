# to be delted, my initial solutions
import random
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from math import radians, sin, asin, cos, sqrt, exp
import copy

class Algorithm(ABC):
    def __init__(self, fleet, cities):
        self.fleet = fleet
        self.cities = cities

    @abstractmethod
    def initialize_solution(self):
        """
        Initialize the solution. Subclasses must provide an implementation.
        """
        pass

    @abstractmethod
    def optimize(self):
        """
        Perform the optimization process. Subclasses must provide an implementation.
        """
        pass

    def evaluate_solution(self):
        """
        Evaluate the current solution. This has a default implementation,
        but subclasses can override it.
        """
        # Default implementation
        pass

    def log_solution(self):
        """
        Log or print the current state of the solution. This has a default implementation,
        but subclasses can override it.
        """
        # Default implementation
        print("Logging current solution...")


class SimulatedAnnealing(Algorithm):
    def __init__(self, vehicles, cities, epochs, attempts, initial_temp, 
                 cooling_rate):
        super().__init__(vehicles, cities)
        self.temperature = initial_temp
        self.epochs = epochs
        self.attempts = attempts
        self.alpha = cooling_rate
        self.current_best = self.initialize_solution()
        self.current_best_solution = self.current_best.distance_covered
    
    def initialize_solution(self):
        cities = self.cities[:]
        random.shuffle(cities)
        current_vehicle_index = 0
        for city in cities:
            current_vehicle = self.fleet[current_vehicle_index]
            current_vehicle.deliver_order(city)
            if current_vehicle_index < len(self.fleet) - 1:
                current_vehicle_index += 1
            else:
                current_vehicle_index = 0
        for vehicle in self.fleet:
            vehicle.go_to_depot()
        return self.fleet
    
    def cool_down(self):
        self.temperature *= self.alpha

    def optimize(self):
        """
        Perform the optimization process. Subclasses must provide an implementation.
        """
        print('initial solution', self.current_best.distance_covered)
        for epoch in range(self.epochs):
            self.run_epoch(epoch)
            self.temperature *= self.alpha
        
        print('solultion:', self.current_best_solution)
        return self.current_best_solution

    
    def run_epoch(self, epoch_num):
        # print('Running epoch:', epoch_num)
        for attempt in range(self.attempts):
            new_solution = self.swap_cities()
            if new_solution and new_solution.distance_covered > self.current_best_solution:
                self.current_best = new_solution
            elif new_solution and self.accept_worse_solution(new_solution):
                self.current_best = new_solution
            else:
                pass
    
    def accept_worse_solution(self, new_solution):
        new_distance = new_solution.distance_covered()
        current_distance = self.current_best_solution
        probability = exp((current_distance - new_distance) / self.temperature)
        return probability > random.uniform(0, 1)

    def swap_cities(self):
        new_fleet = copy.copy(self.fleet)
        route_list = new_fleet.get_all_routes()

        # randomly select 2 routes
        route1, route2 = random.sample(route_list, 2)
        city1 = self.select_random_city(route1)
        city2 = self.select_random_city(route2)
        if city1 and city2:
            new_route1 = copy.copy(route1)
            new_route2 = copy.copy(route2)
            # replace city1 with city2
            # find index
            old_city1_index = route1.route.index(city1)
            old_city2_index = route2.route.index(city2)
            new_route1.route[old_city1_index] = city2
            new_route2.route[old_city2_index] = city1
            # check feasibility
            if new_route1.order <= self.fleet.vehicle_capacity \
                and new_route2.order <= self.fleet.vehicle_capacity:
                route1 = new_route1
                route2 = new_route2
                return new_fleet      
            else:
                pass
                # print('smt go wrong')
        else:
            pass
            # print('!:', route1.route, route2.route)

    
    def select_random_city(self, route):
        choices = [city for city in route.route if not city.is_depot]
        if choices:
            choice = random.choice(choices)
            # print('choice:', choice)
            return choice

    

class Fleet():
    def __init__(self, num_vehicles, vehicle_capacity, depot):
        self.num_vehicles = num_vehicles
        self.vehicle_capacity = vehicle_capacity
        self.depot = depot
        self.vehicles = self.build_fleet()

    def build_fleet(self):
        fleet = []
        for i in range(self.num_vehicles):
            vehicle = Vehicle(capacity=self.vehicle_capacity, depot=self.depot)
            fleet.append(vehicle)
        return fleet
    
    @property
    def distance_covered(self):
        return sum([vehicle.route_list.length for vehicle in self.vehicles])
    
    def get_all_routes(self):
        routes = []
        for vehicle in self.vehicles:
            for route in vehicle.route_list.route_list:
                routes.append(route)
        return routes

    def __iter__(self):
        return iter(self.vehicles)
    def __getitem__(self, index):
        return self.vehicles[index]
    def __len__(self):
        return len(self.vehicles)
    def __str__(self):
        return str(self.vehicles) 

class Vehicle(): 
    def __init__(self, capacity, depot):
        self.capacity = capacity
        self.trunk = capacity
        self.depot = depot
        self.route_list = RouteList(Route(depot))

    def can_deliver_order(self, city):
        return self.trunk >= city.order
    
    def go_to_depot(self):
        self.route_list.add_route(Route(self.depot))
        self.trunk = self.capacity

    def deliver_order(self, city):
        if self.can_deliver_order(city):
            self.trunk -= city.order
            self.route_list.add_city(city)
        else:
            self.route_list.complete_route(self.depot)
            self.go_to_depot()
            self.route_list.add_city(city)
    
    def __str__(self):
        return self.route_list.__str__()
    
    def __repr__(self):
        return f'<Vehicle: t: {self.trunk}, p: {self.route_list.last_city} >'


class RouteList():
    def __init__(self, route):
        self.route_list = [route]
    
    @property
    def last(self):
        return self.route_list[-1]

    @property
    def last_city(self):
        return self.last.route[-1]
    
    @property
    def length(self):
        return sum([route.length for route in self.route_list])
    
    def add_route(self, route):
        self.route_list.append(route)

    def add_city(self, city):
        self.last.add_city(city)
    
    def complete_route(self, depot):
        self.last.add_city(depot)

    def __str__(self):
        return "\n".join(str(route) for route in self.route_list)

    def __repr__(self):
        return f"<RouteList: {len(self.route_list)} routes>"   

class Route():
    def __init__(self, depot):
        self.route = [depot]
    
    def from_list(self, lst, depot):
        for city in lst:
            self.add_city(city)
        self.add_city(depot)

    @property
    def length(self):
        """
        Calcluates route length.
        """
        total_distance = 0
        for i in range(len(self.route)-1):
            distance = self.route[i].calculate_distance_to(self.route[i+1])
            total_distance += distance
        return total_distance
    
    @property
    def order(self):
        """
        Calculates total order in route.
        """
        return sum([city.order for city in self.route])

    def add_city(self, city):
        self.route.append(city)

    def __repr__(self):
        return f"{self.route}, length: {self.length}, order: {self.order}"

    def __str__(self):
        return f"{self.route}, length: {self.length}, order: {self.order}"

class CityList:
    def __init__(self, city_file, depot_name):
        self.city_file = city_file
        self.depot_name = depot_name
        self.cities = self.build_cities(depot_name)

    def build_cities(self, depot_name):
        df = pd.read_csv(self.city_file)
        return [
            City(
                name=row['city'],
                order=row['order'],
                lat=row['latitude'],
                lon=row['longitude'],
                is_depot=(row['city'] == depot_name)
            )
            for _, row in df.iterrows()
        ]
    def __iter__(self):
        return iter(self.cities)

    def __getitem__(self, index):
        return self.cities[index]

    def __len__(self):
        return len(self.cities)

    def __str__(self):
        return str(self.cities)
    
    @property
    def depot(self):
        return next((city for city in self.cities if city.is_depot), None)
    
class City():
    def __init__(self, name, order, lat, lon, is_depot):
        self.name = name
        self.order = order
        self.lat = lat
        self.lon = lon
        self.is_depot = is_depot

    def calculate_distance_to(self, other):
        """
        Calclulates distance to another city using Haversine formula.
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
    
    def __repr__(self):
        return f"{self.name}, order: {self.order}"

    def __str__(self):
        return f"{self.name}, order: {self.order}"
    






def main():
    # Test City class
    print("Testing City class...")
    depot = City("Depot", 0, 40.7128, -74.0060, True)  # Example coordinates for New York
    city1 = City("City1", 10, 34.0522, -118.2437, False)  # Example coordinates for Los Angeles
    city2 = City("City2", 20, 41.8781, -87.6298, False)  # Example coordinates for Chicago

    print("Distance Depot to City1:", depot.calculate_distance_to(city1))
    print("Distance City1 to City2:", city1.calculate_distance_to(city2))

    # Test Route class
    print("\nTesting Route class...")
    route = Route(depot)
    route.add_city(city1)
    route.add_city(city2)

    print("Route:", route)
    print("Route Length:", route.length)
    print("Total Order in Route:", route.order)

    # Test RouteList class
    print("\nTesting RouteList class...")
    route_list = RouteList(route)
    print("Initial RouteList:", route_list)

    new_route = Route(depot)
    new_route.add_city(city2)
    route_list.add_route(new_route)

    print("Updated RouteList:", route_list)

    # Test Vehicle class
    print("\nTesting Vehicle class...")
    vehicle = Vehicle(25, depot)
    vehicle.deliver_order(city1)
    vehicle.deliver_order(city2)

    print("Vehicle after deliveries:", vehicle)

    print("\nTesting CityList and Fleet class...")
    city_list = CityList('./orders.csv', 'Kraków')
    depot = city_list.depot
    fleet = Fleet(num_vehicles=5, vehicle_capacity=1000, depot=depot)

    print('Vehicles:', fleet)
    print('Cities:', city_list)

    print("\nTesting SimulatedAnnealing class...")
    a = SimulatedAnnealing(fleet, city_list, epochs=3, attempts=5, initial_temp=1, cooling_rate=0.9)
    s = a.initialize_solution()

    print(s)
    for i in s:
        print(i)
    a.optimize()
if __name__ == "__main__":
    main()








# class Segment():
#     def __init__(self, depot):
#         self.segment = [depot]
    
#     @property
#     def length(self):
#         """
#         Calcluates route length.
#         """
#         total_distance = 0
#         for i in range(len(self.route)-1):
#             distance = self.route[i].calculate_distance_to(self.route[i+1])
#             total_distance += distance
#         return total_distance
    
#     @property
#     def weight(self):
#         """
#         Calculate segment total order.
#         """
#         total_order = 0
#         for city in self.segment:
#             total_order += city.order
# class Vehicle():
#     def __init__(self, capacity, depot):
#         self.trunk = capacity
#         self.capacity = capacity
#         self.depot = depot
#         self.route = [depot]

#     def drop_order(self, order):
#         self.trunk -= order
    
#     def top_up_trunk(self):
#         self.trunk = self.capacity

#     def can_deliver_order(self, demand):
#         return self.trunk >= demand
    
#     def add_city_to_route(self, city, demand):
#         if self.can_deliver_order(demand):
#             self.route.append(city)
#             self.drop_order(demand)
#         else:
#             self.route.append(self.depot)
#             self.top_up_trunk()
#             self.route.append(city)
#             self.drop_order(demand)

#     def segment_route(self):
#         arr = np.array(self.route)
#         idx = np.where(arr == self.depot)[0]
#         subroutes = np.split(arr, idx+1)
#         segments = [
#             list(segment)[:-1] for segment in subroutes if len(segment) > 1
#             ] 
#         return segments
    
#     def is_segment_feasible(self, segment, G):
#         total_order = sum([int(G.nodes[city]['order'].iloc[0]) for city in segment])
#         return total_order <= self.capacity

#     def remove_empty_segments(self):
#         self.routes = [route for route in self.route if route]

#     def transform_segments_to_route(self, segments):
#         new_route = [self.depot]
#         for segment in segments:
#             for route in segment:
#                 new_route.append(route)
#             new_route.append(self.depot)
#         self.route = new_route

#     def __str__(self):
#         return f"{(self.route)}"
        

#     def get_route(self):
#         return self.route
    
# class Fleet():
#     def __init__(self, num_vehicles, vehicle_capacity, depot):
#         self.num_vehicles = num_vehicles
#         self.vehicle_capacity = vehicle_capacity
#         self.depot = depot

#     @property
#     def fleet(self):
#         fleet = []
#         for i in range(self.num_vehicles):
#             vehicle = Vehicle(capacity=self.vehicle_capacity, depot=self.depot)
#             fleet.append(vehicle)
#         return fleet
    
#     def __iter__(self):
#         return iter(self.fleet)

#     def __getitem__(self, index):
#         return self.fleet[index]

#     def __len__(self):
#         return len(self.fleet)

#     def __str__(self):
#         return str(self.fleet)

# def build_fleet(num_vehicles, vehicle_capacity, depot):
#     fleet = []
#     for i in range(num_vehicles):
#         vehicle = Vehicle(capacity=vehicle_capacity, depot=depot)
#         fleet.append(vehicle)
#     return fleet