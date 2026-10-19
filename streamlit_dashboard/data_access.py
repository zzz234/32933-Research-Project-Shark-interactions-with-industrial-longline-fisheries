"""Load the portable data snapshot and keep filtering independent of the UI."""
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"
REGIONS = ("IATTC", "ICCAT", "IOTC")


def load_region(region: str) -> pd.DataFrame:
    if region not in REGIONS:
        raise ValueError(f"Unknown RFMO: {region}")
    return pd.read_csv(DATA_DIR / f"{region}.csv.gz")


def select_rows(data: pd.DataFrame, species: str, year: int) -> pd.DataFrame:
    return data.loc[(data.species_commonname == species) & (data.year == year)].copy()


def annual_totals(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby("year", as_index=False)["catch"].sum(min_count=1).sort_values("year")
