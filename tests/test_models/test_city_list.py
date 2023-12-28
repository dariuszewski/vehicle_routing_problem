import pytest
from src.models.city_list import CityList
from src.models.city import City
from unittest.mock import mock_open, patch

# Sample data for testing
sample_dicts = [
    {"name": "City1", "order": 100, "lat": 50.0, "lon": 20.0, "is_depot": False},
    {"name": "Depot", "order": 0, "lat": 51.0, "lon": 21.0, "is_depot": True}
]

sample_csv_data = """city,order,latitude,longitude
City1,100,50.0,20.0
Depot,0,51.0,21.0
"""

def test_from_dict_list():
    city_list = CityList.from_dict_list(sample_dicts)
    assert len(city_list) == 2
    assert isinstance(city_list[0], City)
    assert city_list[1].is_depot

def test_from_csv():
    with patch("builtins.open", mock_open(read_data=sample_csv_data)):
        city_list = CityList.from_csv("dummy.csv", ["Depot"])
    assert len(city_list) == 2
    assert city_list[0].name == "City1"
    assert city_list[1].is_depot

def test_depot_list():
    city_list = CityList.from_dict_list(sample_dicts)
    depots = city_list.depot_list
    assert len(depots) == 1
    assert depots[0].name == "Depot"

def test_depot():
    city_list = CityList.from_dict_list(sample_dicts)
    depot = city_list.depot
    assert depot.name == "Depot"
    assert depot.is_depot
