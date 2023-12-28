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
    def __init__(self, fleet: Fleet, city_list: List[CityList], epochs: int, 
                 attempts: int, initial_temp: float, cooling_rate: float,
                 store_solutions: bool = False):
        """
        Initialize a Simulated Annealing algorithm instance for the vehicle 
        routing problem.

        Args:
            fleet (Fleet)       : The fleet of vehicles to be used in the 
                                  routing problem.
            city_list (CityList): A list of cities to be visited in the routing 
                                  problem.
            epochs (int)        : The number of epochs (iterations) to run the 
                                  algorithm.
            attempts (int)      : The number of attempts per epoch to find a 
                                  better solution.
            initial_temp (float): The initial temperature for the annealing 
                                  process.
            cooling_rate (float): The rate at which the temperature cools down, 
                                  typically a small value close to 0 but less 
                                  than 1
        Optional:
            store_solutions (bool): save individual solutions.

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
            current_best_solution (float): The distance covered by the current 
                                           best solution.
            solutions_storage (list)     : List of solutions.

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
        super().__init__(fleet, city_list)
        self.temperature = initial_temp
        self.epochs = epochs
        self.attempts = attempts
        self.alpha = cooling_rate
        self.store_solutions = store_solutions
        self.solutions_storage = []
        self.current_best = self.initialize_solution()
        self.current_best_solution = self.current_best.distance_covered
    
    def initialize_solution(self):
        # randomly shuffle solutions
        random.shuffle(self.city_list)
        # distribute cities between vehicles
        current_vehicle_index = 0
        for city in self.city_list:
            if city.is_depot:
                continue
            current_vehicle = self.fleet[current_vehicle_index]
            current_vehicle.deliver_order(city, self.city_list)
            if current_vehicle_index < len(self.fleet) - 1:
                current_vehicle_index += 1
            else:
                current_vehicle_index = 0
        # go back to depot
        for vehicle in self.fleet:
            vehicle.back_to_depot(self.city_list.random_depot) # back to closest depot? multiple depots is easy to implement with current code.
        # save solution if required
        if self.store_solutions:
            self.solutions_storage.append(copy.copy(self.fleet))
        return self.fleet

    def optimize(self):
        for _ in range(self.epochs):
            self.run_epoch()
            self.temperature = round(self.temperature * self.alpha, 3)      
        return self.current_best_solution

    def store(self, solution):
        if self.store_solutions:
            self.solutions_storage.append(solution)

    def run_epoch(self):
        for _ in range(self.attempts):
            new_solution = self.swap_cities()
            if new_solution.distance_covered > self.current_best_solution:
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
        probability = exp(
            round((current_distance - new_distance) / self.temperature, 2)
            )
        return probability > random.uniform(0, 1)

    def swap_cities(self, counter=0):
        if counter == 3:
            raise BaseException('Cannot swap cities! There is a bug.')
        # prepare copy of solution to avoid changing current best
        new_fleet = copy.copy(self.fleet)
        # randomly select 2 routes and 2 cities
        all_routes = new_fleet.get_all_valid_routes()
        route1, route2 = random.sample(all_routes, 2)
        city1, city1_idx = self.select_random_city(route1)
        city2, city2_idx = self.select_random_city(route2)
        # swap cities
        route1[city1_idx], route2[city2_idx] = city2, city1
        # check routes feasibility
        if (route1.order <= self.fleet[0].capacity) \
            and (route1.order <= self.fleet[0].capacity):
            return new_fleet
        else:
            print('eohoooo')
            self.swap_cities(counter=counter+1)
            
    def select_random_city(self, route):
        choices = [city for city in route if not city.is_depot]
        if choices:
            choice = random.choice(choices)
            choice_idx = route.index(choice)
            return choice, choice_idx

    def __str__(self):
        num_cities = len(self.city_list)
        num_depots = len(city_list.depot_list)
        return ('\n').join([
            '-----------Simulated Annealing Algorithm-----------',
            f'Current Temperature  : {self.temperature}',
            f'Cooling Factor       : {self.alpha}',
            f"Epochs               : {self.epochs} / Attempts: {self.attempts}",
            f"Fleet size           : {len(self.fleet)}",
            f"Vehicle Capacity     : {self.fleet[0].capacity}",
            f"Cities               : {num_cities} with {num_depots} depots.",
            f"Current Shortest     : {self.current_best_solution}",
            '---------------------------------------------------',
        ])

if __name__ == "__main__":
    csv_path = './src/temp/orders_with_depots.csv'
    city_list = CityList.from_csv(city_file=csv_path)
    print(city_list)

    depot = city_list.depot
    fleet = Fleet(num_vehicles=5, vehicle_capacity=1000, depot=depot)
    print(fleet)
    
    SA = SimulatedAnnealing(
        fleet=fleet, city_list=city_list, epochs=5, attempts=3, initial_temp=1, 
        cooling_rate=0.9
    )

    print(SA)
    SA.optimize()
    print(SA)

    