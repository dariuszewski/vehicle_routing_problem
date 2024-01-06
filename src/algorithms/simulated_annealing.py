import random
import copy
from math import exp
from typing import List

try:
    from src.algorithms.models.graph_manager import GraphManager
    from src.algorithms.models.vehicle import Vehicle
except:
    from models.graph_manager import GraphManager
    from models.vehicle import Vehicle



class SimulatedAnnealing():
    def __init__(self, graph_manager: GraphManager, epochs: int, attempts: int, 
                 initial_temp: float, cooling_rate: float,
                 store_solutions: bool=False
                 ) -> None:
        """
        Initialize a Simulated Annealing algorithm instance for the vehicle 
        routing problem.

        Args:
            graph_manager (GraphManager) : The fleet of vehicles to be used 
                                           in the routing problem. 
            epochs (int)                 : The number of epochs (iterations) 
                                           to run the algorithm.
            attempts (int)               : The number of attempts per epoch to 
                                           find a better solution.
            initial_temp (float)         : The initial temperature for 
                                           the annealing process.
            cooling_rate (float)         : The rate at which the temperature 
                                           cools down.

        Optional:
            store_solutions (bool): Save individual solutions.
            
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
        self.graph_manager = graph_manager
        self.temperature = initial_temp
        self.epochs = epochs
        self.attempts = attempts
        self.alpha = cooling_rate
        self.store_solutions = store_solutions
        self.solutions_storage = []
        self.current_best = graph_manager
        # Initial data for logging
        self.initial_best = self.current_best
        self.initial_temp = initial_temp
    
    @property
    def current_best_solution(self):
        return self.current_best.total_length

    def optimize(self):
        for _ in range(self.epochs):
            self.run_epoch()
            self.temperature = round(self.temperature * self.alpha, 2)      
        return self.current_best


    def run_epoch(self):
        for _ in range(self.attempts):
            new_solution = self.anneal()
            if new_solution.total_length <= self.current_best_solution:
                self.current_best = new_solution
            elif self.accept_worse_solution(new_solution):
                self.current_best = new_solution
            else:
                pass
            if self.store_solutions:
                self.solutions_storage.append(self.current_best)
    
    def accept_worse_solution(self, new_solution):
        new_distance = new_solution.total_length
        current_distance = self.current_best_solution
        exponent = -abs((new_distance - current_distance) / self.temperature)
        probability = exp(exponent)
        treshold = random.uniform(0, 1)
        return probability > treshold
        
    def anneal(self):
        # copy current best solution
        solution = copy.deepcopy(self.current_best)
        # find 2 random nodes to swap
        random_node1 = self.select_random_city(solution.node_list)
        random_node2 = self.select_random_city(solution.node_list)
        # handle swap
        solution.handle_swap(random_node1, random_node2)

        return solution
    
    def select_random_city(self, graph):
        choices = [node for node in graph if not node.is_depot]
        if choices:
            return random.choice(choices)
    
    def to_fleet(self):
        fleet = [Vehicle(i+1) for i in range(self.graph_manager.vehicles)]

        cur_veh_idx = 0
        for cycle in self.current_best.cycles:
            fleet[cur_veh_idx].add_route(cycle)
            if cur_veh_idx < self.graph_manager.vehicles-1:
                cur_veh_idx += 1
            else:
                cur_veh_idx = 0
        
        return fleet
        
    def __str__(self):
        num_cities = len(self.graph_manager.node_list)
        num_depots = len([d for d in self.graph_manager.node_list if d.is_depot]) 
        return ('\n').join([
            '-----------Simulated Annealing Algorithm-----------',
            f'Current Temperature  : {self.temperature}',
            f'Initial Temperature  : {self.initial_temp}',
            f'Cooling Factor       : {self.alpha}',
            f"Epochs               : {self.epochs}",
            f"Attempts             : {self.attempts}",
            f"Fleet size           : {self.graph_manager.vehicles}",
            f"Vehicle Capacity     : {self.graph_manager.max_cap}", 
            f"Total Locations      : {num_cities}",
            f"Total Depots         : {num_depots}",
            f"Initial Shortest     : {self.initial_best.total_length}",
            f"Current Shortest     : {self.current_best_solution}",
            '---------------------------------------------------',
        ])

if __name__ == "__main__": 
    clm = GraphManager(
        node_list='./temp/orders_with_depots.csv',
        max_cap=1000,
        vehicles=5
    )
    # print(clm)

    SA = SimulatedAnnealing(graph_manager=clm, epochs=35, attempts=30, 
                            initial_temp=1, cooling_rate=0.9)
    print(SA.current_best)
    SA.optimize()
    print(SA.current_best)
    print(SA)

    fleet = SA.to_fleet()
    print(len(fleet))
