import random
import copy
from math import exp
from typing import List

try:
    from src.algorithms.algorithm import Algorithm
    from src.models.fleet import Fleet
except ImportError:
    from algorithm import Algorithm
    from node import NodeList
    from graph import Graph
    from graph_manager import GraphManager


class SimulatedAnnealing():
    def __init__(self, fleet: GraphManager, epochs: int, attempts: int, 
                 initial_temp: float, cooling_rate: float,
                 annealing_method: str='random', store_solutions: bool=False) -> None:
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
        self.fleet = fleet
        self.temperature = initial_temp
        self.epochs = epochs
        self.attempts = attempts
        self.alpha = cooling_rate
        self.store_solutions = store_solutions
        self.solutions_storage = []
        self.current_best = fleet
        ###
        self.annealing_method = annealing_method
        self.initial_best = self.current_best
        self.initial_temp = initial_temp
    
    @property
    def current_best_solution(self):
        return self.current_best.distance_covered
    
    def promise_nearest_depot(self, city):
        depot = lambda: self.fleet.city_list.find_nearest_depot(city)
        return depot


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
        
    def anneal(self):
        # copy current best solution
        fleet = copy.deepcopy(self.current_best)
        random_node1 = self.select_random_city(fleet)
        random_node2 = self.select_random_city(fleet)
        if random_node1 == random_node2:
            print('same nodes what to do')
            return fleet
        print('go to exchened')
        fleet.exchange_edges(random_node1, random_node2)

        return fleet
    
    def select_random_city(self, graph):
        choices = [node for node in graph.nodes if not node.is_depot]
        if choices:
            return random.choice(choices)
        
    def __str__(self):
        num_cities = len(self.fleet.city_list)
        num_depots = len([d for d in self.fleet.city_list if d.is_depot]) 
        return ('\n').join([
            '-----------Simulated Annealing Algorithm-----------',
            f'Anneling Method      : {self.annealing_method}',
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
    import itertools
    graph = GraphManager('./temp/orders_with_depots.csv', 5, 1000)
    # print(data)
    SA = SimulatedAnnealing(fleet=graph, epochs=35, attempts=30 , initial_temp=1,
                            cooling_rate=0.9)
    SA.optimize()
    print(SA.initial_best.distance_covered)
    print(SA.current_best_solution)
    print(sum([len(item.to_list()) for item in SA.current_best.graphs]))
    # for graph in SA.current_best.graphs:
    #     print(graph)
    #     print(graph.length)
    # nds = [i.lst() for i in SA.current_best.graphs]
    # fl = []
    # for i in nds:
    #     fl.extend(i)
    # ndsn = [i.name for i in fl]
    # print(len(ndsn))
    # for g in graph.graphs:
    #     print(g)
    # print()
    # try:
    #     a = SA.anneal()
    # except Exception as e:
    #     print(e)
    # for graph in a.graphs:
    #     print(graph)    
    # try:
    #     SA.optimize()
    # except Exception as e:
    #     print(e)
    #     print(graph)
    #     for graph in SA.current_best.graphs:
    #         print(graph)
            


    # nds = [i.lst() for i in graph.graphs]
    # fl = []
    # for i in nds:
    #     fl.extend(i)
    # ndsn = [i.name for i in fl]
    # print(len(ndsn))
    # ls = [n.name for n in graph.nodes]
    # print(len(ls))
    # for i in ls:
    #     if i not in ndsn:
    #         print(i)