
import streamlit as st
from utils.style import apply_premium_style, hero
from utils.data_loader import load_excel, apply_filters, list_options
from utils.model_engine import build_district_model
from modules import executive, model_page, demografi, comparison, intervensi, indicators, social_media, warning_timeline

st.set_page_config(
    page_title="Sistem Pintar IKM Nasional",
    page_icon="🇲🇾",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_premium_style()

with st.sidebar:
    st.markdown("## 🎛️ Kawalan Dashboard")
    st.markdown("Gunakan penapis untuk simulasi briefing kepada panel.")
    uploaded = st.file_uploader("Upload Excel IKM (.xlsx)", type=["xlsx"])

respondent, social, district_old, weights, timeline = load_excel(uploaded)

# Build model from raw data only: avoid wrong hardcoded summaries
model_all, resp_model_all, weights_normal = build_district_model(respondent, social, weights)

with st.sidebar:
    negeri_options, daerah_options_initial = list_options(model_all)
    selected_negeri = st.selectbox("Negeri/Wilayah", negeri_options)
    _, daerah_options = list_options(model_all, selected_negeri)
    selected_daerah = st.selectbox("Daerah", daerah_options)
    selected_risk = st.selectbox("Tahap Risiko", ["Semua", "Rendah", "Sederhana", "Tinggi", "Kritikal"])

    st.markdown("### Modul")
    module = st.radio(
        "Pilih paparan",
        [
            "Executive",
            "Model IKM",
            "Demografi",
            "Perbandingan Negeri/Daerah",
            "Lokasi & Intervensi",
            "Indikator",
            "Media Sosial",
            "Amaran Awal",
            "Milestone"
        ],
        label_visibility="collapsed"
    )

resp_f, social_f, model_f = apply_filters(resp_model_all, social, model_all, selected_negeri, selected_daerah, selected_risk)

hero()

if module == "Executive":
    executive.render(model_f, resp_f, social_f)
elif module == "Model IKM":
    model_page.render(resp_f, weights, model_f)
elif module == "Demografi":
    demografi.render(resp_f)
elif module == "Perbandingan Negeri/Daerah":
    comparison.render(model_f)
elif module == "Lokasi & Intervensi":
    intervensi.render(model_f)
elif module == "Indikator":
    indicators.render(resp_f, model_f)
elif module == "Media Sosial":
    social_media.render(social_f, model_f)
elif module == "Amaran Awal":
    warning_timeline.render_warning(model_f)
elif module == "Milestone":
    warning_timeline.render_timeline(timeline)

st.markdown("<div class='callout'><b>Nota:</b> Semua metrik, peratus demografi, model IKM dan perbandingan dikira semula daripada data Excel yang dimuat naik. Tiada nilai KPI hardcoded.</div>", unsafe_allow_html=True)
