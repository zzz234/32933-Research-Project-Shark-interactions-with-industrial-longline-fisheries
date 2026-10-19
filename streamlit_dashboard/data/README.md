# Data provenance

The three compressed CSVs are reduced-column snapshots of the existing project's
`data/IATTC.csv`, `data/ICCAT.csv` and `data/IOTC.csv`, prepared on 2026-10-14.
No rows are sampled, no predictions are retrained and no values are intentionally
rounded. CSV serialization preserves numeric values to pandas parsing precision.

| RFMO | Rows |
| --- | ---: |
| IATTC | 339,300 |
| ICCAT | 8,592 |
| IOTC | 13,500 |

Fields: `rfmo`, `year`, `latitude`, `longitude`, `species_commonname`, `catch`,
`original_effort`, `mean_sst`, `mean_chla`, `mean_ssh`, `.final_pred`.
The snapshot contains years 2012–2020. Missing values are retained.

The project's fisheries data source is *Global hotspots of shark
interactions with industrial longline fisheries*, Burns, Bradley & Thomas,
Zenodo. A reference PDF exists in the parent research workspace. The exact
record DOI, version, catch/effort units and reuse licence have not yet been
verified; these should be documented from the original record before public
redistribution. No licence for the third-party data is invented here.

Rebuild from the original CSV directory using `python prepare_data.py ../data`.
Data exploration, preprocessing, model training and evaluation are documented in
the project's `data_cleaning.ipynb` in the parent research workspace. The model
performance and feature-importance values in `app.py` match that Notebook's saved
outputs (rounded to three decimal places). Random Forest models use a random
80/20 training–testing split stratified by species; feature importances are
aggregated by predictor group. Training and evaluation take place offline, and
the dashboard provides interactive exploration of the data and analytical results.
The map's `.final_pred` field remains the source dataset's supplied prediction,
separate from the Random Forest evaluation results produced by this project.
