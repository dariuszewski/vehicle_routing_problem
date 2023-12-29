# IT IS HERE ONLY FOR CONVIENIENCE DURING DEVELOPMENT!!!
import random
import copy
from math import exp
from typing import List

try:
    from src.algorithms.algorithm import Algorithm
    from src.models.fleet import Fleet
except ImportError:
    from algorithm import Algorithm
    from models.fleet import Fleet
    from models.city_list import CityList
    from models.vehicle import Vehicle


class SimulatedAnnealing(Algorithm):
    def __init__(self, fleet: Fleet, epochs: int, attempts: int, 
                 initial_temp: float, cooling_rate: float,
                 annealing_method: str, store_solutions: bool=False) -> None:
        """
        Initialize a Simulated Annealing algorithm instance for the vehicle 
        routing problem.

        Args:
            fleet (Fleet)         : The fleet of vehicles to be used in the 
                                    routing problem.
            epochs (int)          : The number of epochs (iterations) to run 
                                    the algorithm.
            attempts (int)        : The number of attempts per epoch to find a 
                                    better solution.
            initial_temp (float)  : The initial temperature for the annealing 
                                    process.
            cooling_rate (float)  : The rate at which the temperature cools 
                                    down. Typically between 0.8 and 0.99.
            annealing_method (str): One of 'random', 'nearest_neighbor' and
                                    'city_swap'
        Optional:
            store_solutions (bool): Save individual solutions.

        Attributes:
            temperature (float)          : Current temperature of the annealing 
                                           process.
            epochs (int)                 : Total num of epochs the annealing 
                                           process will run.
            attempts (int)               : Number of attempts per epoch to find
                                           a better solution.
            alpha (float)                : Cooling rate for the annealing 
                                           process.
            current_best (Fleet)         : The current best solution found by 
                                           the algorithm.
            annealing_method (str)       : Annealing method.
            solutions_storage (list)     : List of solutions
            
        The algorithm explores solutions at each temperature level, making a 
        series of attempts. In each attempt, it probabilistically decides 
        whether to accept a new solution based on its quality and the current 
        temperature. The current best solution is updated whenever a better 
        solution is found. At the end of each epoch, the temperature is reduced 
        according to the cooling rate. This process allows the algorithm to 
        potentially accept worse solutions at higher temperatures, providing a 
        mechanism to escape local optima. As the temperature decreases, the 
        algorithm becomes increasingly likely to accept only better solutions, 
        converging towards a global optimum.
        """
        super().__init__(fleet)
        self.temperature = initial_temp
        self.epochs = epochs
        self.attempts = attempts
        self.alpha = cooling_rate
        self.store_solutions = store_solutions
        self.solutions_storage = []
        self.current_best = self.initialize_solution(fleet)
        self.annealing_method = annealing_method
        self.initial_best = self.current_best
        self.initial_temp = initial_temp
    
    @property
    def current_best_solution(self):
        return self.current_best.distance_covered
    
    def anneal(self):
        if self.annealing_method == 'random':
            return self.random_annealing()
        elif self.annealing_method == 'nearest_neighbor':
            return self.nearest_neighbor_annealing()
        elif self.annealing_method == 'city_swap':
            return self.city_swap_annealing()
    
    def promise_nearest_depot(self, city):
        depot = lambda: self.fleet.city_list.find_nearest_depot(city)
        return depot

    
    def initialize_solution(self, fleet):
        # copy the fleet, original one can be reused without re-initialisation
        fleet = copy.deepcopy(fleet)
        # randomly shuffle solutions
        random.shuffle(fleet.city_list)
        # distribute cities between vehicles
        cur_vehicle_idx = 0
        for city in fleet.city_list:
            if city.is_depot:
                continue
            cur_vehicle = fleet[cur_vehicle_idx]
            cur_vehicle.deliver_order(city, self.promise_nearest_depot(city))
            if cur_vehicle_idx < len(fleet) - 1:
                cur_vehicle_idx += 1
            else:
                cur_vehicle_idx = 0
        # go back to depot
        for vehicle in fleet:
            vehicle.back_to_depot(self.promise_nearest_depot(city))
        # save solution if required
        if self.store_solutions:
            self.solutions_storage.append(fleet)
        return fleet

    def optimize(self):
        for _ in range(self.epochs):
            self.run_epoch()
            self.temperature = round(self.temperature * self.alpha, 2)      
        return self.current_best

    def run_epoch(self):
        for _ in range(self.attempts):
            new_solution = self.anneal()
            if new_solution.distance_covered <= self.current_best_solution:
                self.current_best = new_solution
            elif self.accept_worse_solution(new_solution):
                self.current_best = new_solution
            else:
                pass
            if self.store_solutions:
                self.solutions_storage.append(self.current_best)
    
    def accept_worse_solution(self, new_solution):
        new_distance = new_solution.distance_covered
        current_distance = self.current_best_solution
        exponent = -abs((new_distance - current_distance) / self.temperature)
        probability = exp(exponent)
        treshold = random.uniform(0, 1)
        return probability > treshold

    def nearest_neighbor_annealing(self):
        # copy current best solution
        fleet = copy.deepcopy(self.current_best)
        # get a random city to optimize
        all_routes = fleet.get_all_valid_routes()
        route = random.choice(all_routes)
        city, idx = self.select_random_city(route)
        # find a nearest neighbor in km
        neighbor = fleet.city_list.find_nearest_neighbor(city)
        neighbor_route = fleet.get_route_by_city(neighbor)
        # allign city with it's neighbor
        route.insert(idx , neighbor)
        neighbor_route.remove(neighbor)
        # check feasibility
        if route.order <= fleet.vehicle_capacity:
            # if feasible, return solution
            return fleet
        else:
            # if not feasible, go to the next attempt
            return self.current_best
    
    def random_annealing(self):
        # copy current best solution
        fleet = copy.deepcopy(self.current_best)
        # get 2 random cities
        all_routes = fleet.get_all_valid_routes()
        route1, route2 = random.sample(all_routes, 2)
        _, city1_idx = self.select_random_city(route1)
        city2, _ = self.select_random_city(route2)
        # move city2 to route1
        route1.insert(city1_idx , city2)
        route2.remove(city2)
        # check feasibility
        if route1.order <= fleet.vehicle_capacity:
            # if feasible, return solution *maybe merge routes too?
            return fleet
        else:
            # if not feasible, go to the next attempt
            return self.current_best
        
    def city_swap_annealing(self):
        # copy current best solution
        fleet = copy.deepcopy(self.current_best)
        # get 2 random cities
        all_routes = fleet.get_all_valid_routes()
        route1, route2 = random.sample(all_routes, 2)
        city1, idx1 = self.select_random_city(route1)
        city2, idx2 = self.select_random_city(route2)
        # perform swap
        route1[idx1], route2[idx2] = city2, city1
        # check feasibility
        cap = fleet.vehicle_capacity
        if route1.order <= cap and route2.order <= cap:
            return fleet
        else:
            return self.current_best 
            
    def select_random_city(self, route):
        choices = [city for city in route if not city.is_depot]
        if choices:
            choice = random.choice(choices)
            choice_idx = route.index(choice)
            return choice, choice_idx

    def __str__(self):
        num_cities = len(self.fleet.city_list)
        num_depots = len([d for d in self.fleet.city_list if d.is_depot]) 
        return ('\n').join([
            '-----------Simulated Annealing Algorithm-----------',
            f'Current Temperature  : {self.temperature}',
            f'Initial Temperature  : {self.initial_temp}',
            f'Cooling Factor       : {self.alpha}',
            f"Epochs               : {self.epochs}",
            f"Attempts             : {self.attempts}",
            f"Fleet size           : {len(self.fleet)}",
            f"Vehicle Capacity     : {self.fleet[0].capacity}",
            f"Total Locations      : {num_cities}",
            f"Total Depots         : {num_depots}",
            f"Initial Shortest     : {self.initial_best.distance_covered}",
            f"Current Shortest     : {self.current_best_solution}",
            '---------------------------------------------------',
        ])

if __name__ == "__main__":
    csv_path = './temp/orders_multiple_depots.csv'
    city_list = CityList.from_csv(city_file=csv_path)
    print(city_list)

    depot = city_list.depot
    fleet = Fleet(num_vehicles=5, vehicle_capacity=1000, city_list=city_list)

    
    SA = SimulatedAnnealing(
        fleet=fleet, epochs=20, attempts=5, initial_temp=1000, 
        cooling_rate=0.9, annealing_method='nearest_neighbor', 
        store_solutions=True
    )

    SA.optimize()
    print(SA)
    # for s in SA.solutions_storage:
    #     for v in s:
    #         for r in v.route_list:
    #             print(r)
    #         print('============================================================')

    