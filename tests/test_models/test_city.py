import pytest
from src.models.city import City


def test_city_initialization():
    city = City(name="Test", order=0, lat=40.7, lon=-74.0, is_depot=True)

    assert city.name == "Test"
    assert city.order == 0
    assert city.lat == 40.7
    assert city.lon == -74.0
    assert city.is_depot


def test_calculate_distance_to():
    krakow = City(name="Kraków", order=50, lat=50.0647, lon=19.9450, is_depot=False)
    warsaw = City(name="Warszawa", order=50, lat=52.2297, lon=21.0122, is_depot=False)

    distance = krakow.calculate_distance_to(warsaw)

    # The distance is approximately 252 kilometers
    assert distance == pytest.approx(252, rel=1e-3)
