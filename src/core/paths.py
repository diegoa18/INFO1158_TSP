from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[2]

DATA: Path = ROOT / "data"
FIGS: Path = ROOT / "figs"
ROUTES: Path = FIGS / "routes"

for folder in (FIGS, ROUTES):
    folder.mkdir(parents=True, exist_ok=True)
