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



class TabuSearch():
    def __init__(self, graph_manager: GraphManager, max_iterations: int,
                 tabu_size: int, search_limit_level: float = 0.8) -> None:
        """
        Initialize a Tabu Searcg algorithm instance for the vehicle
        routing problem.

        Args:
            graph_manager (GraphManager) : The fleet of vehicles to be used 
                                           in the routing problem. 
            max_iterations (int)         : The number of iterations to run by 
                                           the algorithm.
            tabu_size (int)              : The size of the tabu list.
        Optional:
            search_limit_level (float)   : A part of max_iterations from which 
                                           the algorithm will lessen the 
                                           search area.
                
        The algorithm iteratively explores the solution space by making local 
        changes (like swapping nodes) to the current solution. 
        It avoids revisiting recent solutions by maintaining a 'tabu list', 
        which helps in exploring new areas and escaping local optima.
        """
        self.graph_manager = graph_manager
        self.current_best = graph_manager
        self.max_iterations = max_iterations
        self.search_limit_level = search_limit_level
        self.tabu_size = tabu_size
        self.tabu_list = [graph_manager]
        #
        self.initial_best = self.current_best

    def optimize(self):
        for i in range(self.max_iterations):
            sn = i > self.max_iterations / self.search_limit_level
            solution = copy.deepcopy(self.current_best)
            # find 2 random nodes to swap
            random_node1 = self.select_random_city(solution.node_list)
            random_node2 = self.select_random_city(solution.node_list)
            # create tabu list entry
            tabu_entries = [
                (random_node1.name, random_node2.name),
                (random_node2.name, random_node1.name)
                ]
            # check if tabu entry is in tabu list
            for tabu_entry in tabu_entries:
                if tabu_entry in self.tabu_list:
                    continue
            else:
                # add tabu entry to tabu list
                for tabu_entry in tabu_entries:
                    self.tabu_list.append(tabu_entry)
                # check if tabu is not full
                while len(self.tabu_list) > self.tabu_size:
                    self.tabu_list.pop(0)
                # handle swap
                solution.handle_swap(random_node1, random_node2, sn)
                # update current_best
                if solution.total_length < self.current_best.total_length:
                    self.current_best = solution
    
    def select_random_city(self, graph):
        choices = [node for node in graph if not node.is_depot]
        if choices:
            return random.choice(choices)
        
    def __str__(self):
        num_cities = len(self.graph_manager.node_list)
        num_depots = len([d for d in self.graph_manager.node_list if d.is_depot]) 
        return ('\n').join([
            '---------------Tabu Search Algorithm---------------',
            f"Iterations           : {self.max_iterations}",
            f"Tabu List Size       : {self.tabu_size}",
            f"Fleet size           : {self.graph_manager.vehicles}",
            f"Vehicle Capacity     : {self.graph_manager.max_cap}", 
            f"Total Locations      : {num_cities}",
            f"Total Depots         : {num_depots}",
            f"Initial Shortest     : {self.initial_best.total_length}",
            f"Current Shortest     : {self.current_best.total_length}",
            '---------------------------------------------------',
        ])
    
if __name__ == "__main__":

    clm = GraphManager(
        node_list='./data/orders_with_depots.csv',
        max_cap=1000,
        vehicles=5
    )

    TS = TabuSearch(graph_manager=clm, max_iterations=1500, tabu_size=100)

    TS.optimize()
    
    print(TS.current_best.total_length)
    print(TS)