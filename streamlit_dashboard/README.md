# Shark Fisheries Interaction Explorer

An interactive research dashboard exploring shark–longline fishery interactions across three regional fisheries management organisations (RFMOs): IATTC, ICCAT and IOTC, covering 2012–2020.

The project combines fisheries data exploration, preprocessing and Random Forest modelling with a Streamlit interface for exploring spatial patterns, catch trends and model results.

## Features

- Filter the spatial explorer by RFMO, species and year.
- Switch between reported catch and the original dataset's predictions.
- Hover over map points or select a point to inspect environmental conditions.
- Compare annual reported catch and species composition.
- Explore Random Forest performance and feature importance.
- View and download filtered records as CSV.

## Requirements

- Python 3.12 or later. The dashboard has been tested locally with Python 3.14.
- The Python packages listed in `requirements.txt`.
- A web browser. Internet access is needed for initial package installation and Plotly's geographic basemap resources.

The bundled compressed datasets total approximately 4.7 MB. The original large CSV files are not required to run the dashboard.

## First-time setup

Download and extract the repository, or clone it using Git. Open the project in VS Code and choose **Terminal > New Terminal**.

Run the following commands from the folder containing this README, `app.py` and `requirements.txt`. If you opened the full `sharks` project, first run:

```bash
cd streamlit_dashboard
```

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

These commands use the project's virtual environment directly; activation is not required. Make sure the Python interpreter used to create it is version 3.12 or later.

Open the local URL printed in the terminal, normally [http://localhost:8501](http://localhost:8501).

## Starting the dashboard again

Once setup is complete, you do not need to recreate the environment or reinstall packages each time. Open a terminal in this folder and run:

**macOS / Linux:**

```bash
.venv/bin/python -m streamlit run app.py
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Keep the terminal running while using the dashboard. Press **Ctrl+C** to stop it. After closing the terminal or restarting the computer, run the command again before opening the local URL.

## Project structure

```text
streamlit_dashboard/
├── app.py                  # Streamlit interface and charts
├── data_access.py          # Data loading, filtering and aggregation
├── prepare_data.py         # Rebuild compressed data from source CSVs
├── requirements.txt        # Pinned dashboard dependencies
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml          # Theme and application settings
├── data/
│   ├── IATTC.csv.gz
│   ├── ICCAT.csv.gz
│   ├── IOTC.csv.gz
│   └── README.md           # Data provenance
└── tests/
    └── test_app.py
```

The wider research workspace also contains `data_cleaning.ipynb`, which documents the data exploration, preprocessing, model training and evaluation. It is outside this dashboard folder. Include it separately when submitting the full research project; it is not needed to launch the dashboard. These requirements cover the dashboard, not the complete Notebook training environment.

## Data and methodology

The fisheries datasets originate from *Global hotspots of shark interactions with industrial longline fisheries* (Zenodo; Burns, Bradley & Thomas). See [data provenance](data/README.md) for the snapshot details and outstanding source metadata.

The Random Forest models were developed and evaluated using the preprocessed fisheries datasets in the project's Jupyter Notebook. Performance is based on a random 80/20 training–testing split, stratified by species. Model training and evaluation were conducted offline; this dashboard provides an interactive interface for exploring the results.

The displayed performance and feature-importance values match the Notebook's saved outputs, rounded to three decimal places. Further temporal and spatial validation is recommended to assess model generalisability.

### Interpreting the views

- **Overview cards and catch composition:** the selected RFMO, across all available years and species.
- **Map, environmental context and CSV download:** the selected RFMO, species and year.
- **Annual trends:** all three RFMOs, with a choice of all species or the selected species.
- **Model performance:** the three RFMO models. Feature importance follows the selected RFMO.
- **Original model prediction:** the source dataset's `.final_pred` field, separate from this project's Random Forest evaluation results.

Map colours use a logarithmic transformation within each view. Compare original values rather than colours across views. Differences in sampling, reporting, effort and grid resolution limit direct comparisons between RFMOs. Feature importance describes predictive contribution, not causation.

## Sharing the project

### GitHub: source code and local reproduction

Upload this folder's source files, configuration and bundled data as the dashboard project. A reviewer can download the repository and follow the setup instructions above on their own computer, independently of the author's computer.

For a complete research submission, also include the analysis Notebook and relevant supporting documentation. Exclude `.venv`, caches, secrets and temporary build files. The existing `.gitignore` covers the dashboard's local environment and secrets.

GitHub stores the project; a repository link alone does not start the Streamlit application.

### Streamlit Community Cloud: a hosted dashboard

To provide a browser-accessible dashboard independently of your computer:

1. Push the project to GitHub.
2. Open Streamlit Community Cloud and select **Create app**.
3. Select the repository, branch and entrypoint: `app.py` if this folder is the repository root, or `streamlit_dashboard/app.py` if the full project is uploaded.
4. Select Python 3.12 or later in the deployment settings and deploy.
5. Share the generated `streamlit.app` URL.

See the [official deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

### Cloudflare: temporary sharing from your computer

Install `cloudflared` using the [official instructions](https://developers.cloudflare.com/tunnel/downloads/). Start the dashboard, then run this command in a second terminal:

```bash
cloudflared tunnel --url http://localhost:8501
```

Share the generated `trycloudflare.com` URL. No domain is required. Your computer must remain awake and connected, with both Streamlit and `cloudflared` running. The temporary hostname changes when a new tunnel is created. By default, anyone with the URL can access the dashboard.

Quick Tunnels are intended for testing and demonstrations and have no uptime guarantee. See the [Cloudflare Quick Tunnels documentation](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/).

## Troubleshooting

| Issue | What to check |
| --- | --- |
| The local URL does not open | Start Streamlit and keep its terminal running. Use the URL printed in that terminal. |
| `app.py` or `requirements.txt` cannot be found | Change into the folder containing these files before running the commands. |
| `No module named streamlit` | Install requirements using this folder's `.venv` Python, then launch with that same interpreter. |
| Port 8501 is already in use | Add `--server.port 8502` to the launch command and open the URL printed by Streamlit. For tunnel sharing, use the same port in the tunnel command. |
| Dataset file is missing | Ensure all three `.csv.gz` files are present in the dashboard's `data` folder. Keep them compressed. |
| Map background is missing | Check that the browser can access Plotly's geographic resources over the internet. |

## Validation and data preparation

From this folder, run the included tests with:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

To rebuild the bundled snapshots from the original CSVs in the parent research project's `data` folder:

```bash
.venv/bin/python prepare_data.py ../data
```

On Windows, replace `.venv/bin/python` with `.\.venv\Scripts\python.exe`.

Snapshot generation selects the eleven fields needed by the dashboard and compresses them without sampling rows or retraining models. Updating a snapshot does not automatically update the separately stored model metrics.
