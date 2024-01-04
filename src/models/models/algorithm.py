from abc import ABC, abstractmethod


class Algorithm(ABC):
    def __init__(self, fleet):
        self.fleet = fleet
        
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
