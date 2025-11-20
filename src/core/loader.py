from pathlib import Path
from .paths import DATA
import csv
#LOADER DE CIUDADES CSV
def load_cities(file_name="cities.csv"):
    cities = []
    path = DATA / file_name

    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cities.append({ #diccionario
                "name": row["name"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"])
            })

    return cities
