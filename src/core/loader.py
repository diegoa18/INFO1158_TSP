from pathlib import Path
import csv
from typing import List, Optional
from .paths import DATA
from .types import City

#LISTA DE OBJETOS CITY
#CADA FILA -> name, lat, lon
def load_cities(file_name: str = "cities.csv", n_cities: Optional[int] = None) -> List[City]:
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

    if n_cities is not None:
        if n_cities < 2:
             pass
        cities = cities[:n_cities]

    return cities
