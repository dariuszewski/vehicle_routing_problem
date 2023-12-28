from abc import ABC, abstractmethod


class Algorithm(ABC):
    def __init__(self, fleet, city_list):
        self.fleet = fleet
        self.city_list = city_list

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
