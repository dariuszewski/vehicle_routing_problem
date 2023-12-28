import pytest
from src.models.fleet import Fleet
from src.models.vehicle import Vehicle
from src.models.city import City
from src.models.route import Route

# Sample data for testing
depot = City("Depot", 0, 42.0, -77.0, True)
city1 = City("City1", 10, 40.0, -75.0, False)
city2 = City("City2", 15, 41.0, -76.0, False)

def test_fleet_initialization():
    fleet = Fleet(2, 25, depot)
    assert len(fleet) == 2
    for vehicle in fleet:
        assert vehicle.capacity == 25
        assert vehicle.depot == depot

def test_fleet_from_list():
    vehicles = [Vehicle(25, depot), Vehicle(30, depot)]
    fleet = Fleet.from_list(vehicles)
    assert len(fleet) == 2
    for vehicle in fleet:
        assert vehicle in vehicles

def test_distance_covered():
    vehicle1 = Vehicle(25, depot)
    vehicle1.deliver_order(city1, None)  # Assuming this adds a route to the vehicle
    vehicle2 = Vehicle(25, depot)
    vehicle2.deliver_order(city2, None)

    fleet = Fleet.from_list([vehicle1, vehicle2])
    assert fleet.distance_covered >= 0

def test_get_all_routes():
    vehicle = Vehicle(25, depot)
    vehicle.deliver_order(city1, None)
    fleet = Fleet.from_list([vehicle])
    routes = fleet.get_all_routes()
    assert len(routes) >= 1
    for route in routes:
        assert isinstance(route, Route)

def test_fleet_iterable():
    fleet = Fleet(2, 25, depot)
    assert all(isinstance(vehicle, Vehicle) for vehicle in fleet)

def test_fleet_indexing():
    fleet = Fleet(2, 25, depot)
    assert isinstance(fleet[0], Vehicle)
    assert isinstance(fleet[1], Vehicle)
