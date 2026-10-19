# Shark Fisheries Interaction Explorer

An interactive Streamlit dashboard exploring shark interactions with industrial longline fisheries across three Regional Fisheries Management Organisations (RFMOs): **IATTC, ICCAT and IOTC**, using data from 2012–2020.

The project includes fisheries data exploration, preprocessing and Random Forest modelling. The dashboard lets users explore catch patterns, environmental conditions, annual trends and model results.

## Main Features

- Explore shark catch data by RFMO, species and year.
- View spatial patterns and environmental information on interactive maps.
- Compare annual catch trends and species composition.
- Examine Random Forest model performance and feature importance.
- Download filtered data as CSV.

## Setup and Run

**Requirements:** Python 3.12 or later, VS Code (or another code editor) and an internet connection for installing packages.

1. Download the repository from GitHub (**Code → Download ZIP**) and extract it.
2. Open the extracted project folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Enter the dashboard folder:

   ```bash
   cd streamlit_dashboard
   ```

5. Create a virtual environment and install the required packages.

   **macOS / Linux:**
   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   ```

   **Windows PowerShell:**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

6. Start the dashboard.

   **macOS / Linux:**
   ```bash
   .venv/bin/python -m streamlit run app.py
   ```

   **Windows PowerShell:**
   ```powershell
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

Open the local address shown in the terminal, usually **http://localhost:8501**. Keep the terminal running while using the dashboard; press **Ctrl+C** to stop it.

**Next time:** Open a terminal in `streamlit_dashboard` and run only the command in Step 6. You do not need to reinstall the packages.

## Project Files

- `streamlit_dashboard/app.py` — Streamlit dashboard.
- `streamlit_dashboard/data/` — Compressed datasets needed to run the dashboard (included in this repository).
- `streamlit_dashboard/requirements.txt` — Required Python packages.
- `data_cleaning.ipynb` — Data exploration, cleaning and modelling notebook; not required to launch the dashboard.

The original large CSV datasets are not required to launch the dashboard.
