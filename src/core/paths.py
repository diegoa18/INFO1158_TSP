from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] #[2] -> subir dos niveles desde /core

DATA = ROOT / "data"
FIGS = ROOT / "figs"
ROUTES = FIGS / "routes"

for folder in (FIGS, ROUTES):
    folder.mkdir(parents=True, exist_ok=True)
