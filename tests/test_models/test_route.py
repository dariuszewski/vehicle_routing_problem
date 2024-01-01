import pytest
from src.models.city import City
from src.models.route import Route

# Sample data for testing
depot = City("Depot", 0, 42.0, -77.0, True)
city1 = City("City1", 10, 40.0, -75.0, False)
city2 = City("City2", 20, 41.0, -76.0, False)


def test_route_initialization():
    route = Route(depot)
    assert len(route) == 1
    assert route[0] == depot


def test_route_from_list():
    with pytest.raises(BaseException):
        Route.from_list(
            [city1]
        )  # Should raise an exception as it doesn't start with a depot

    route = Route.from_list([depot, city1, city2])
    assert len(route) == 3
    assert route[0] == depot
    assert route[1] == city1
    assert route[2] == city2


def test_route_length():
    route = Route.from_list([depot, city1, city2])
    assert route.length > 0  # The actual length depends on the coordinates


def test_route_is_empty():
    empty_route = Route(depot)
    assert empty_route.is_empty

    non_empty_route = Route.from_list([depot, city1])
    assert not non_empty_route.is_empty


def test_route_order():
    route = Route.from_list([depot, city1, city2])
    assert route.order == 30  # 10 (City1) + 20 (City2)


def test_add_city():
    route = Route(depot)
    route.add_city(city1)
    assert len(route) == 2
    assert route[1] == city1
