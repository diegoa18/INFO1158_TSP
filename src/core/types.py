from dataclasses import dataclass

@dataclass(frozen=True)
class City:
    name: str
    lat: float
    lon: float
