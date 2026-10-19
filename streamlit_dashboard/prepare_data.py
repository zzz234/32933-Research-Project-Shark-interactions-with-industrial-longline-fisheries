"""Rebuild portable snapshots: python prepare_data.py ../data"""
import argparse
from pathlib import Path
import pandas as pd
from data_access import DATA_DIR, REGIONS

COLUMNS = ["rfmo", "year", "latitude", "longitude", "species_commonname", "catch",
           "original_effort", "mean_sst", "mean_chla", "mean_ssh", ".final_pred"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    DATA_DIR.mkdir(exist_ok=True)
    for region in REGIONS:
        frame = pd.read_csv(args.source / f"{region}.csv", usecols=COLUMNS)
        frame.to_csv(DATA_DIR / f"{region}.csv.gz", index=False,
                     compression={"method": "gzip", "mtime": 0})
        print(f"{region}: {len(frame):,} records")
