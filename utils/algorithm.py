# to be deleted

import random

from utils.problem_builder import Vehicle


CAPACITY = 500


class Algorithm():
    
    def generate_initial_route(self, G, depot='Kraków', vehicles=5):
        cities = [city for city in list(G.nodes) if city != depot]
        random.shuffle(cities)
        solution = [Vehicle(CAPACITY, depot) for _ in range(vehicles)]
        current_vehicle_index = 0
        for city in cities:
            order = int(G.nodes[city]['order'].iloc[0])
            solution[current_vehicle_index].add_city_to_route(city, order)
            if current_vehicle_index < len(solution) - 1:
                current_vehicle_index += 1
            else:
                current_vehicle_index = 0
        for vehicle in solution:
            vehicle.add_city_to_route(depot, 0)
        return solution
        # routes = [vehicle.route for vehicle in solution]
        # return (solution, routes)

    def calculate_total_distance(self, G, vehicles):
        routes_lengths = []
        for vehicle in vehicles:
            route_length = 0
            route = vehicle.route
            for i in range(len(route) - 1):
                route_length += G[route[i]][route[i+1]]['distance']
            routes_lengths.append(route_length)
        total_distance = sum(routes_lengths)
        return total_distance
