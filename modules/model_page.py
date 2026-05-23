
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.model_engine import explain_model_text, normalise_weights
from utils.charts import bar_compare, heatmap_corr

def render(resp_model, weights, model):
    st.markdown("<div class='section-title'>Model Pengiraan IKM</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Bahagian ini menjelaskan formula, pemberat indikator, klasifikasi risiko dan semakan pengiraan.</div>", unsafe_allow_html=True)

    exp = explain_model_text()
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='dark-card'><b>Model Survey</b><br><br>{exp['survey']}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='dark-card'><b>Model Komposit</b><br><br>{exp['komposit']}</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='dark-card'><b>Klasifikasi Risiko</b><br><br>{exp['risk']}</div>", unsafe_allow_html=True)

    w = normalise_weights(weights)
    col1, col2 = st.columns([.9, 1.1])
    with col1:
        st.markdown("#### Pemberat Indikator")
        st.dataframe(w[["domain","berat_simulasi","berat_normal","kaedah_dicadangkan","justifikasi_ringkas"]], use_container_width=True, height=360)
    with col2:
        fig = px.bar(w, x="domain", y="berat_normal", color="domain", text_auto=".2%",
                     title="Pemberat Normal Indikator IKM")
        fig.update_layout(height=360, showlegend=False, xaxis_tickangle=-30, plot_bgcolor="rgba(255,255,255,0)", paper_bgcolor="rgba(255,255,255,0)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Semakan Pengiraan Responden")
    cols = ["respondent_id","negeri","daerah","IKM_survey_model","tahap_risiko_model",
            "skor_ekonomi","skor_politik","skor_sosial","skor_digital","skor_keselamatan","skor_defisit_kepercayaan","skor_risiko_perpaduan"]
    st.dataframe(resp_model[cols].head(500), use_container_width=True, height=360)

    st.markdown("#### Model Daerah")
    show = model[["negeri","daerah","bil_responden","bil_post","IKM_survey","risiko_digital","kadar_hate_speech","IKM_komposit_model","tahap_risiko_model","keutamaan_intervensi"]].sort_values("IKM_komposit_model", ascending=False)
    st.dataframe(show, use_container_width=True, height=420)
