import pytest
from src.models.vehicle import Vehicle
from src.models.city import City
from src.models.city_list import CityList
from src.models.route import Route

# Sample data for testing
depot = City("Depot", 0, 42.0, -77.0, True)
city1 = City("City1", 10, 40.0, -75.0, False)
city2 = City("City2", 15, 41.0, -76.0, False)
city_list = CityList([city1, city2])


def test_vehicle_initialization():
    vehicle = Vehicle(25, depot)
    assert vehicle.capacity == 25
    assert vehicle.trunk == 25
    assert vehicle.depot == depot


def test_can_deliver_order():
    vehicle = Vehicle(25, depot)
    assert vehicle.can_deliver_order(city1)
    assert not vehicle.can_deliver_order(City("LargeOrder", 30, 45.0, -79.0, False))


def test_visit_depot():
    vehicle = Vehicle(25, depot)
    vehicle.trunk = 0  # Simulate having delivered some orders
    vehicle.visit_depot(depot)
    assert vehicle.trunk == vehicle.capacity


def test_deliver_order():
    vehicle = Vehicle(25, depot)
    vehicle.deliver_order(
        city1, city_list
    )  # Assuming city_list is not needed for this test
    assert vehicle.trunk == 15  # 25 - 10

    # Test delivering an order that exceeds the vehicle's capacity
    vehicle.deliver_order(city1, city_list)
    # Assuming appropriate logic is implemented for this scenario in deliver_order


def test_vehicle_string_representation():
    vehicle = Vehicle(25, depot)
    assert isinstance(str(vehicle), str)
    assert isinstance(repr(vehicle), str)
