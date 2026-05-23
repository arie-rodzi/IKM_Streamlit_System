
import streamlit as st
from data_loader import load_excel, apply_filters
from analytics import national_kpis
from styles import inject_css, hero, kpi_card, RISK_COLORS
from pages import page_executive, page_demographic, page_location, page_indicators, page_social, page_warning, page_timeline

st.set_page_config(page_title="Sistem Pintar IKM Nasional", page_icon="🇲🇾", layout="wide", initial_sidebar_state="expanded")
inject_css()

uploaded = st.sidebar.file_uploader("Muat naik Excel IKM (.xlsx)", type=["xlsx"])
respondent, social, district, weights, timeline = load_excel(uploaded)

st.sidebar.markdown("## 🎛️ Kawalan Dashboard")
st.sidebar.caption("Gunakan penapis untuk simulasi briefing kepada panel.")
negeri_opts = ["Semua"] + sorted(district["negeri"].dropna().unique().tolist())
negeri = st.sidebar.selectbox("Negeri/Wilayah", negeri_opts)
if negeri != "Semua":
    daerah_opts = ["Semua"] + sorted(district.loc[district["negeri"] == negeri, "daerah"].dropna().unique().tolist())
else:
    daerah_opts = ["Semua"] + sorted(district["daerah"].dropna().unique().tolist())
daerah = st.sidebar.selectbox("Daerah", daerah_opts)
risiko = st.sidebar.selectbox("Tahap Risiko", ["Semua", "Rendah", "Sederhana", "Tinggi", "Kritikal"])

resp_f, social_f, district_f = apply_filters(respondent, social, district, negeri, daerah, risiko)

hero()
kpis = national_kpis(resp_f, social_f, district_f)
cols = st.columns(7)
with cols[0]: kpi_card("Purata IKM", f"{kpis['avg_ikm']:.2f}", "IKM komposit", RISK_COLORS.get(kpis['risk'], '#fff'))
with cols[1]: kpi_card("Tahap Risiko", kpis['risk'], "berdasarkan purata", RISK_COLORS.get(kpis['risk'], '#fff'))
with cols[2]: kpi_card("Responden", f"{kpis['respondents']:,}", "survey simulasi", "#00B4D8")
with cols[3]: kpi_card("Media Sosial", f"{kpis['posts']:,}", "rekod digital", "#C9952B")
with cols[4]: kpi_card("Daerah", f"{kpis['districts']:,}", "liputan lokasi", "#F77F00")
with cols[5]: kpi_card("Hotspot", f"{kpis['hotspots']:,}", "risiko ≥ sederhana", "#C0392B")
with cols[6]: kpi_card("Hate Speech", f"{kpis['hate_rate']:.1f}%", "isyarat digital", "#F72585")

menu = st.sidebar.radio(
    "Modul",
    ["Executive", "Demografi", "Lokasi & Intervensi", "Indikator", "Media Sosial", "Amaran Awal", "Milestone"],
    index=0
)

if menu == "Executive":
    page_executive(resp_f, social_f, district_f)
elif menu == "Demografi":
    page_demographic(resp_f)
elif menu == "Lokasi & Intervensi":
    page_location(resp_f, social_f, district_f)
elif menu == "Indikator":
    page_indicators(resp_f, district_f)
elif menu == "Media Sosial":
    page_social(resp_f, social_f, district_f)
elif menu == "Amaran Awal":
    page_warning(district_f)
elif menu == "Milestone":
    page_timeline(timeline)

st.sidebar.markdown("---")
st.sidebar.success("Prototype premium: modular 7 fail .py, colourful, demografi, perbandingan negeri/daerah, big data dan intervensi lokasi.")
