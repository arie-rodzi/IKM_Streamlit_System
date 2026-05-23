
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.charts import heatmap_corr, bar_compare

def render(resp_model, model):
    st.markdown("<div class='section-title'>Analisis Indikator IKM</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Penerangan indikator, skor purata, korelasi dan hubungan dengan tahap risiko.</div>", unsafe_allow_html=True)

    desc = pd.DataFrame({
        "Indikator": ["Ekonomi","Politik","Sosial","Digital/Media","Keselamatan","Defisit Kepercayaan","Risiko Perpaduan"],
        "Maksud": [
            "Tekanan kos sara hidup, pekerjaan dan kerentanan ekonomi.",
            "Polarisasi politik, persepsi konflik dan isu tadbir urus.",
            "Hubungan komuniti, interaksi sosial dan penerimaan antara kumpulan.",
            "Sentimen digital, naratif media sosial dan penyebaran isu sensitif.",
            "Persepsi keselamatan, insiden setempat dan rasa aman komuniti.",
            "Tahap kurang percaya terhadap institusi, dasar dan mekanisme penyelesaian.",
            "Risiko kemerosotan perpaduan, kurang kohesi dan potensi konflik sosial."
        ],
        "Interpretasi Skor Tinggi": [
            "Tekanan ekonomi lebih kuat",
            "Polarisasi lebih ketara",
            "Kerapuhan sosial meningkat",
            "Risiko digital lebih tinggi",
            "Kebimbangan keselamatan meningkat",
            "Kepercayaan institusi lebih rendah",
            "Kerapuhan perpaduan lebih tinggi"
        ]
    })
    st.dataframe(desc, use_container_width=True, height=260)

    cols = ["skor_ekonomi","skor_politik","skor_sosial","skor_digital","skor_keselamatan","skor_defisit_kepercayaan","skor_risiko_perpaduan","IKM_survey_model"]
    mean = resp_model[cols].mean().reset_index()
    mean.columns = ["Indikator","Purata Skor"]
    mean["Indikator"] = mean["Indikator"].str.replace("skor_","").str.replace("_"," ").str.title()

    col1, col2 = st.columns([1,.95])
    with col1:
        fig = bar_compare(mean.sort_values("Purata Skor", ascending=False), x="Indikator", y="Purata Skor", title="Purata Skor Indikator", height=430)
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.plotly_chart(heatmap_corr(resp_model[cols], "Korelasi Indikator Dengan IKM"), use_container_width=True)

    st.markdown("### Indikator Mengikut Tahap Risiko")
    risk_mean = resp_model.groupby("tahap_risiko_model")[cols[:-1]].mean().reset_index().melt(id_vars="tahap_risiko_model")
    fig2 = px.bar(risk_mean, x="variable", y="value", color="tahap_risiko_model", barmode="group",
                  title="Perbandingan Indikator Mengikut Risiko")
    fig2.update_layout(height=520, xaxis_tickangle=-35, plot_bgcolor="rgba(255,255,255,0)", paper_bgcolor="rgba(255,255,255,0)")
    st.plotly_chart(fig2, use_container_width=True)
