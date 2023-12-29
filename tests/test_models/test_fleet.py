import pytest
from src.models.fleet import Fleet
from src.models.vehicle import Vehicle
from src.models.city import City
from src.models.city_list import CityList


@pytest.fixture
def sample_city_list():
    return CityList.from_csv('./temp/orders_multiple_depots.csv')

@pytest.fixture
def sample_fleet(sample_city_list):
    # Create a sample Fleet for testing
    depot = sample_city_list.depot
    return Fleet(3, 100, sample_city_list, depot)

def test_build_fleet(sample_city_list):
    fleet = Fleet(3, 100, sample_city_list)
    assert len(fleet) == 3
    assert all(isinstance(vehicle, Vehicle) for vehicle in fleet)

def test_get_all_valid_routes(sample_fleet):
    valid_routes = sample_fleet.get_all_valid_routes()
    assert isinstance(valid_routes, list)
    # Add more checks based on what you define as a 'valid route'

def test_get_route_by_city(sample_fleet):
    city = sample_fleet.city_list[0]  # Assuming this city is in one of the routes
    route = sample_fleet.get_route_by_city(city)
    assert city in route


