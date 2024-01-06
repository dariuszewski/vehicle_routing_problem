import csv
import copy
from typing import List

try:
    from src.algorithms.models.iterable import Iterable
except:
    from iterable import Iterable

class Node:
    def __init__(self, 
                 name: str, 
                 lat: float, 
                 lon: float, 
                 weight: int, 
                 is_depot: bool) -> None:
        """
        A simple Node. Graph representation of a city.

        Args:
            name    : The name of the city.
            lat     : The latitude of the city.
            lon     : The longitude of the city.
            weight  : The order quantity associated with the city.
            is_depot: Flag indicating whether the city is a depot.
        """
        self.name = name
        self.lat = lat
        self.lon = lon
        self.weight = weight
        self.is_depot = is_depot
        self.next = None
        self.prev = None

    def __repr__(self):
        is_depot = '-Depot' if self.is_depot else '' 
        return f'<Node{is_depot} {self.name}, w: {self.weight}>'
    
    def __str__(self) -> str:
        is_depot = ', depot' if self.is_depot else '' 
        return f"{self.name} ({self.weight})"


class NodeList(Iterable):
    def __init__(self, items: List[Node]) -> None:
        self._items = items

    @classmethod
    def from_flie(cls, file_path):
        nodes = []
        with open(file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                node = Node(
                    name=row['city'],
                    weight=int(row['order']),
                    lat=float(row['latitude']),
                    lon=float(row['longitude']), 
                    is_depot=(True if row['is_depot'] == 'True' else False)
                )
                nodes.append(node)
        return cls(nodes)
    
    def get_node_by_name(self, node_name):
        for item in self._items:
            if item.name == node_name:
                return item
    
    def get_closest_depot(self, node):
        depots = [node for node in self._items if node.is_depot]
        depot_node = depots[0]
        depot = copy.deepcopy(depot_node)
        depot.next, depot.prev = None, None
        return depot
    
    @property
    def depot(self):
        depots = [node for node in self._items if node.is_depot]
        return copy.deepcopy(depots[0])
    
    def __str__(self) -> str:
        return ('\n').join([str(item) for item in self._items])


if __name__ == "__main__":
    # Load nodes from a file
    file_path = './data/orders_with_depots.csv'
    node_list = NodeList.from_flie(file_path)

    # Print all nodes
    print("All Nodes:")
    print(node_list)

    # Get a specific node by name
    node_name = 'Białystok'  # Replace with an actual city name from your file
    specific_node = node_list.get_node_by_name(node_name)
    print(f"\nNode by name '{node_name}':")
    print(specific_node)

    # Find the closest depot to a specific node
    if specific_node:
        closest_depot = node_list.get_closest_depot(specific_node)
        print(f"\nClosest depot to {specific_node.name}:")
        print(closest_depot)
    else:
        print(f"Node with name '{node_name}' not found.")
