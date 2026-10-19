"""Shark Fisheries Interaction Explorer — run with streamlit run app.py."""
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from data_access import REGIONS, annual_totals, load_region, select_rows

st.set_page_config(page_title="Shark Fisheries | Interaction Explorer", page_icon="🦈", layout="wide")


@st.cache_data(show_spinner=False)
def region_data(region):
    return load_region(region)


COLORS = {"IATTC": "#4e79d9", "ICCAT": "#ef8354", "IOTC": "#28a892"}
IMPORTANCE = {
    "IATTC": [.185, .100, .030, .455, .230],
    "ICCAT": [.137, .098, .069, .311, .384],
    "IOTC": [.087, .048, .035, .342, .488],
}
MODEL = pd.DataFrame({"RFMO": REGIONS, "R² (log catch)": [.885, .655, .811],
                      "RMSE (original scale)": [16.516, 984.780, 361.723]})


def chart(fig, **kwargs):
    fig.update_layout(margin=dict(l=8, r=8, t=30, b=8), paper_bgcolor="rgba(0,0,0,0)")
    return st.plotly_chart(fig, width="stretch", **kwargs)


with st.sidebar:
    st.title("🦈 Shark Fisheries")
    st.caption("INTERACTION EXPLORER")
    rfmo = st.selectbox("Regional fisheries organisation", REGIONS)
    try:
        data = region_data(rfmo)
    except (OSError, ValueError) as exc:
        st.error(f"Could not load the bundled data: {exc}")
        st.stop()
    options = sorted(data.species_commonname.dropna().unique())
    species = st.selectbox("Species", options, index=options.index("BLUE SHARK") if "BLUE SHARK" in options else 0)
    years = sorted(data.loc[data.species_commonname == species, "year"].unique().tolist())
    year = st.select_slider("Map year", years, value=years[-1])
    layer = st.radio("Map layer", ["Reported catch", "Original model prediction"], key="layer")
    st.divider()
    st.caption("Map and environmental context follow all three filters. Overview cards and catch composition cover the selected RFMO across all years and species.")

st.caption("GLOBAL LONGLINE FISHERIES · RESEARCH EXPLORER")
st.title("Where sharks and fisheries meet")
st.write("Explore reported catch, published predictions and environmental conditions across three tuna RFMOs.")
st.caption(f"{rfmo} · {int(data.year.min())}–{int(data.year.max())} · All species overview")
cards = st.columns(4)
cards[0].metric("Observations", f"{len(data):,}")
cards[1].metric("Total reported catch", f"{data['catch'].sum():,.0f}")
cards[2].metric("Zero catch records", f"{data['catch'].dropna().eq(0).mean():.1%}")
cards[3].metric("Species categories", data.species_commonname.nunique())

spatial, trends, methods = st.tabs(["Spatial explorer", "Catch patterns", "Model & methods"])
rows = select_rows(data, species, year).reset_index(drop=True)
metric = "catch" if layer == "Reported catch" else ".final_pred"

with spatial:
    st.subheader(f"Interaction hotspots · {year}")
    st.caption(f"{rfmo} / {species.title()} · {len(rows):,} records. Hover for details; click a point to inspect its environment.")
    valid = rows.loc[rows.latitude.between(-90, 90) & rows.longitude.between(-180, 180) & np.isfinite(rows[metric])].copy()
    if valid.empty:
        st.info("No valid map observations for this selection.")
    else:
        # Colour transform only: exported and hovered values retain the original scale.
        valid["Colour intensity"] = np.log1p(valid[metric].clip(lower=0))
        left, right = st.columns([3, 1])
        with left:
            fig = px.scatter_geo(valid, lat="latitude", lon="longitude", color="Colour intensity",
                custom_data=["catch", ".final_pred", "mean_sst", "mean_chla", "mean_ssh", "original_effort"],
                hover_data={"Colour intensity": False, metric: ":,.2f"},
                color_continuous_scale="YlOrRd", projection="natural earth", height=490)
            fig.update_traces(marker=dict(size=6, opacity=.75))
            fig.update_geos(showland=True, landcolor="#d9e3e8", showocean=True, oceancolor="#eef6fa", showcountries=True, countrycolor="white")
            fig.update_layout(coloraxis_colorbar=dict(title="log(1 + value)"), clickmode="event+select")
            event = chart(fig, key=f"map-{rfmo}-{species}-{year}-{metric}", on_select="rerun", selection_mode="points")
            st.caption("Colours use log(1 + max(value, 0)) within this view; compare original values, not colours, across views. Invalid coordinates or missing layer values are excluded.")
        with right:
            selected = event.selection.points
            st.markdown("#### Environmental context")
            if selected:
                point = selected[0]
                context = valid.iloc[int(point["point_index"])].to_dict()
                st.caption(f"Selected record · {point['lat']:.1f}°, {point['lon']:.1f}°")
            else:
                context = rows.mean(numeric_only=True).to_dict()
                st.caption("Mean across all filtered records")
            for label, key in [(layer, metric), ("Sea surface temperature", "mean_sst"), ("Chlorophyll-a", "mean_chla"), ("Sea surface height", "mean_ssh"), ("Fishing effort", "original_effort")]:
                value = context.get(key)
                st.metric(label, "N/A" if value is None or pd.isna(value) else f"{value:,.2f}")
            st.caption("Environmental and effort values retain source units.")
    with st.expander("Explore and download filtered records"):
        st.dataframe(rows, hide_index=True, width="stretch")
        st.download_button("Download CSV", rows.to_csv(index=False).encode(), file_name=f"{rfmo}-{year}-{species.lower().replace(' ', '-')}.csv", mime="text/csv")

with trends:
    st.subheader("Annual reported catch")
    scope = st.radio("Trend scope", ["All species", "Selected species"], horizontal=True, key="trend_scope")
    series = []
    for region in REGIONS:
        frame = region_data(region)
        if scope == "Selected species":
            frame = frame.loc[frame.species_commonname == species]
        series.append(annual_totals(frame).assign(RFMO=region))
    chart(px.line(pd.concat(series), x="year", y="catch", color="RFMO", markers=True,
                  color_discrete_map=COLORS, labels={"year": "Year", "catch": "Total reported catch"}))
    st.caption("Missing species/year combinations are absent, not zero. Source catch scales and grid resolutions differ across RFMOs.")
    st.subheader(f"Catch composition · {rfmo}")
    composition = data.groupby("species_commonname", as_index=False)["catch"].sum().nlargest(10, "catch").sort_values("catch")
    chart(px.bar(composition, x="catch", y="species_commonname", orientation="h",
                 color_discrete_sequence=[COLORS[rfmo]], labels={"catch": "Total reported catch", "species_commonname": "Species"}))
    st.caption("Top ten categories · all available years")

with methods:
    st.subheader("Random Forest Model Performance")
    st.write("The Random Forest models were developed and evaluated using the preprocessed fisheries datasets in this project's Jupyter Notebook. The results presented below summarise model performance based on a random 80/20 training–testing split, stratified by species.")
    st.write("Model training and evaluation were conducted offline, while this dashboard provides an interactive interface for exploring the results. Further temporal and spatial validation is recommended to assess model generalisability.")
    st.dataframe(MODEL, hide_index=True, width="stretch")
    importance = pd.DataFrame({"Feature": ["SST", "Chlorophyll-a", "SSH", "Fishing effort", "Species"], "Importance": IMPORTANCE[rfmo]}).sort_values("Importance")
    chart(px.bar(importance, x="Importance", y="Feature", orientation="h", title=f"Feature importance · {rfmo}", color_discrete_sequence=[COLORS[rfmo]]))
    st.caption("Impurity-based feature importance from the Random Forest models developed in the project's Notebook, aggregated by predictor group. Predictive contribution does not establish causation.")
    st.markdown("""
**Reported catch** is the observed catch field in the supplied RFMO datasets. These data are strongly zero-inflated; totals are not population estimates or standardized catch rates.

**Original model prediction** uses the supplied `.final_pred` field. It is separate from the notebook model metrics above; this dashboard does not train models or generate new predictions.

**Spatial comparisons:** the project's data exploration identifies 5° grids for ICCAT/IOTC and 1° grids for IATTC. Differences in sampling, effort, coverage and reporting limit direct comparisons.

**Data and analysis:** the fisheries datasets originate from *Global hotspots of shark interactions with industrial longline fisheries* (Zenodo; Burns, Bradley & Thomas). Data exploration, preprocessing, model training and evaluation were carried out in this project's `data_cleaning.ipynb`. This dashboard presents the fisheries data alongside the resulting model performance and feature importance. The bundled snapshot retains the source CSV values for the eleven displayed fields. See `data/README.md` for provenance and reproduction.
""")

st.divider()
st.caption("SHARK FISHERIES INTERACTION EXPLORER · Built with Streamlit & Plotly · Research portfolio")
