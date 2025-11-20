from pathlib import Path
import csv
from typing import List
from .paths import DATA
from .types import City

#LISTA DE OBJETOS CITY
#CADA FILA -> name, lat, lon
def load_cities(file_name: str = "cities.csv") -> List[City]:
    cities: List[City] = []
    path: Path = DATA / file_name

    if not path.exists():
        raise FileNotFoundError(f"city data file not found at {path}")

    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            #cada ciudad se convierte en objeto city
            cities.append(City(
                name=row["name"],
                lat=float(row["lat"]),
                lon=float(row["lon"])
            ))

    return cities
