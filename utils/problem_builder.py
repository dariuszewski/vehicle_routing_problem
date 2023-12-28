# to be deleted
import networkx as nx
import numpy as np
import pandas as pd


def generate_graph(orders_data, distance_matrix):
    G = nx.Graph()
    for city in orders_data['city']:
        row = orders_data[orders_data['city'] == city]
        location = (row['longitude'].iloc[0], row['latitude'].iloc[0])
        order = row['order']
        G.add_node(city, location=location, order=order)

    for origin in orders_data['city']:
        for destination in orders_data['city']:
            if origin != destination:
                distance = distance_matrix.at[origin, destination]
                G.add_edge(origin, destination, distance=distance)
    
    return G



class Vehicle():
    def __init__(self, capacity, depot):
        self.trunk = capacity
        self.capacity = capacity
        self.depot = depot
        self.route = [depot]

    def drop_order(self, order):
        self.trunk -= order
    
    def top_up_trunk(self):
        self.trunk = self.capacity

    def can_deliver_order(self, demand):
        return self.trunk >= demand
    
    def add_city_to_route(self, city, demand):
        if self.can_deliver_order(demand):
            self.route.append(city)
            self.drop_order(demand)
        else:
            self.route.append(self.depot)
            self.top_up_trunk()
            self.route.append(city)
            self.drop_order(demand)

    def segment_route(self):
        arr = np.array(self.route)
        idx = np.where(arr == self.depot)[0]
        subroutes = np.split(arr, idx+1)
        segments = [
            list(segment)[:-1] for segment in subroutes if len(segment) > 1
            ] 
        return segments
    
    def is_segment_feasible(self, segment, G):
        total_order = sum([int(G.nodes[city]['order'].iloc[0]) for city in segment])
        return total_order <= self.capacity

    def remove_empty_segments(self):
        self.routes = [route for route in self.route if route]

    def transform_segments_to_route(self, segments):
        new_route = [self.depot]
        for segment in segments:
            for route in segment:
                new_route.append(route)
            new_route.append(self.depot)
        self.route = new_route

    def __str__(self):
        return f"{(self.route)}"
        

    def get_route(self):
        return self.route
    