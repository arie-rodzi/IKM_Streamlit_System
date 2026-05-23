
from pathlib import Path
import pandas as pd
import streamlit as st

DEFAULT_FILE = Path("IKM_Simulation_Data_Malaysia.xlsx")

@st.cache_data(show_spinner=False)
def load_excel(file=None):
    source = file if file is not None else DEFAULT_FILE
    xls = pd.ExcelFile(source)
    respondent = pd.read_excel(xls, "respondent_data")
    social = pd.read_excel(xls, "social_media_data")
    district = pd.read_excel(xls, "district_summary")
    weights = pd.read_excel(xls, "parameter_weighting")
    timeline = pd.read_excel(xls, "timeline_18_bulan")
    for df in [respondent, social]:
        if "tarikh" in df.columns:
            df["tarikh"] = pd.to_datetime(df["tarikh"], errors="coerce")
        if "tarikh_kutipan" in df.columns:
            df["tarikh_kutipan"] = pd.to_datetime(df["tarikh_kutipan"], errors="coerce")
    return respondent, social, district, weights, timeline

def apply_filters(respondent, social, district, negeri, daerah, risiko):
    r, s, d = respondent.copy(), social.copy(), district.copy()
    if negeri != "Semua":
        r = r[r["negeri"] == negeri]
        s = s[s["negeri"] == negeri]
        d = d[d["negeri"] == negeri]
    if daerah != "Semua":
        r = r[r["daerah"] == daerah]
        s = s[s["daerah"] == daerah]
        d = d[d["daerah"] == daerah]
    if risiko != "Semua":
        if "tahap_risiko" in r.columns:
            r = r[r["tahap_risiko"] == risiko]
        if "tahap_risiko" in d.columns:
            d = d[d["tahap_risiko"] == risiko]
    return r, s, d
