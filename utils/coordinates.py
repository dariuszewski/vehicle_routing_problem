# this is to fetch city coords
from opencage.geocoder import OpenCageGeocode
import pandas as pd


key = ""
geocoder = OpenCageGeocode(key)

CITIES = [
    {"city": "Kraków", "order": 0},
    {"city": "Białystok", "order": 500},
    {"city": "Bielsko-Biała", "order": 50},
    {"city": "Chrzanów", "order": 400},
    {"city": "Gdańsk", "order": 200},
    {"city": "Gdynia", "order": 100},
    {"city": "Gliwice", "order": 40},
    {"city": "Gromnik", "order": 200},
    {"city": "Katowice", "order": 300},
    {"city": "Kielce", "order": 30},
    {"city": "Krosno", "order": 60},
    {"city": "Krynica", "order": 50},
    {"city": "Lublin", "order": 60},
    {"city": "Łódź", "order": 160},
    {"city": "Malbork", "order": 100},
    {"city": "Nowy Targ", "order": 120},
    {"city": "Olsztyn", "order": 300},
    {"city": "Poznań", "order": 100},
    {"city": "Puławy", "order": 200},
    {"city": "Radom", "order": 100},
    {"city": "Rzeszów", "order": 60},
    {"city": "Sandomierz", "order": 200},
    {"city": "Szczecin", "order": 150},
    {"city": "Szczucin", "order": 60},
    {"city": "Szklarska Poręba", "order": 50},
    {"city": "Tarnów", "order": 70},
    {"city": "Warszawa", "order": 200},
    {"city": "Wieliczka", "order": 90},
    {"city": "Wrocław", "order": 40},
    {"city": "Zakopane", "order": 200},
    {"city": "Zamość", "order": 300},
]


def fetch_city_coordinates(city):
    results = geocoder.geocode(city)
    lat = results[0]["geometry"]["lat"]
    lng = results[0]["geometry"]["lng"]
    return (lat, lng)


def create_coordinates_matrix(cities=CITIES, depots=["Kraków"]):
    results = []

    for city in cities:
        coords = fetch_city_coordinates(city=city["city"])
        result = {
            "city": city["city"],
            "order": city["order"],
            "latitude": coords[0],
            "longitude": coords[1],
            "is_depot": city["city"] in depots,
        }

        results.append(result)

    df = pd.DataFrame(results)
    df.to_csv("./orders_with_depots.csv", index=False)

    print(df)
    return df


if __name__ == "__main__":
    create_coordinates_matrix()
