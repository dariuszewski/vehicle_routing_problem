import pytest
from src.models.city_list import CityList
from src.models.city import City


@pytest.fixture
def city_list():
    return CityList.from_csv("./data/orders_multiple_depots.csv")


# Test for creating CityList from CSV
def test_city_list_from_csv(city_list):
    assert len(city_list) == 31  # Assuming 31 cities in CSV
    assert isinstance(city_list[0], City)


# Test for finding the nearest neighbor
def test_find_nearest_neighbor(city_list):
    city1 = city_list[5]
    nearest_neighbor = city_list.find_nearest_neighbor(city1)
    assert nearest_neighbor.name != city1.name  # Ensure it's a different city
    assert not nearest_neighbor.is_depot  # Ensure it's not a depot


# Test for finding the nearest depot
def test_find_nearest_depot(city_list):
    city1 = city_list[5]
    nearest_depot = city_list.find_nearest_depot(city1)
    assert nearest_depot.is_depot  # Ensure it's a depot


# Test for depot property
def test_depot_property(city_list):
    depot = city_list.depot
    assert depot.is_depot  # Ensure it returns a depot


# You can add more tests for other methods or edge cases as needed.
