import pytest
from src.models.city import City
from src.models.route import Route
from src.models.route_list import RouteList

# Sample data for testing
depot = City("Depot", 0, 42.0, -77.0, True)
city1 = City("City1", 10, 40.0, -75.0, False)
city2 = City("City2", 20, 41.0, -76.0, False)

def test_routelist_initialization():
    initial_route = Route(depot)
    route_list = RouteList(initial_route)
    assert len(route_list) == 1

def test_add_route():
    route_list = RouteList(Route(depot))
    new_route = Route(depot)
    route_list.add_route(new_route)
    assert len(route_list) == 2

def test_add_city():
    route_list = RouteList(Route(depot))
    route_list.add_city(city1)
    assert route_list.last_city == city1

def test_complete_route():
    route_list = RouteList(Route(depot))
    route_list.add_city(city1)
    route_list.complete_route(depot)
    assert route_list.last_city == depot

def test_route_list_length():
    route_list = RouteList(Route(depot))
    route_list.add_city(city1)
    route_list.complete_route(depot)
    new_route = Route(depot)
    new_route.add_city(city2)
    route_list.add_route(new_route)
    assert route_list.length > 0  # Length depends on actual city distances
