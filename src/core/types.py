from dataclasses import dataclass

#objeto city inmutable
@dataclass(frozen=True)
class City:
    name: str
    lat: float
    lon: float
