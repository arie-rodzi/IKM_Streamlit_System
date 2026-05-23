
import streamlit as st
import pandas as pd
from pathlib import Path

REQUIRED_SHEETS = [
    "respondent_data",
    "social_media_data",
    "district_summary",
    "parameter_weighting",
    "timeline_18_bulan"
]

@st.cache_data(show_spinner=False)
def load_excel(source=None):
    if source is None:
        source = Path("IKM_Simulation_Data_Malaysia.xlsx")
    xls = pd.ExcelFile(source)
    missing = [s for s in REQUIRED_SHEETS if s not in xls.sheet_names]
    if missing:
        raise ValueError(f"Sheet tiada dalam Excel: {missing}")

    respondent = pd.read_excel(xls, "respondent_data")
    social = pd.read_excel(xls, "social_media_data")
    district = pd.read_excel(xls, "district_summary")
    weights = pd.read_excel(xls, "parameter_weighting")
    timeline = pd.read_excel(xls, "timeline_18_bulan")

    respondent = clean_columns(respondent)
    social = clean_columns(social)
    district = clean_columns(district)
    weights = clean_columns(weights)
    timeline = clean_columns(timeline)

    for df in [respondent, social]:
        for col in ["tarikh", "tarikh_kutipan"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

    return respondent, social, district, weights, timeline

def clean_columns(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df

def apply_filters(respondent, social, district, negeri="Semua", daerah="Semua", risk="Semua"):
    r = respondent.copy()
    s = social.copy()
    d = district.copy()

    if negeri != "Semua":
        r = r[r["negeri"] == negeri]
        s = s[s["negeri"] == negeri]
        d = d[d["negeri"] == negeri]

    if daerah != "Semua":
        r = r[r["daerah"] == daerah]
        s = s[s["daerah"] == daerah]
        d = d[d["daerah"] == daerah]

    if risk != "Semua":
        if "tahap_risiko" in r.columns:
            r = r[r["tahap_risiko"] == risk]
        if "tahap_risiko" in d.columns:
            d = d[d["tahap_risiko"] == risk]

    return r, s, d

def list_options(district, selected_negeri="Semua"):
    negeri = ["Semua"] + sorted(district["negeri"].dropna().astype(str).unique().tolist())
    if selected_negeri != "Semua":
        daerah = ["Semua"] + sorted(district.loc[district["negeri"] == selected_negeri, "daerah"].dropna().astype(str).unique().tolist())
    else:
        daerah = ["Semua"] + sorted(district["daerah"].dropna().astype(str).unique().tolist())
    return negeri, daerah
