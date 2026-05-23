
import streamlit as st
import numpy as np
import plotly.express as px

def render_warning(model):
    st.markdown("<div class='section-title'>Modul Amaran Awal</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Senarai keutamaan tindakan mengikut skor IKM, risiko digital dan kadar hate speech.</div>", unsafe_allow_html=True)

    d = model.copy()
    d["status_amaran"] = np.select(
        [d["IKM_komposit_model"] >= 75, d["IKM_komposit_model"] >= 60, d["IKM_komposit_model"] >= 45],
        ["🚨 Kritikal - Tindakan Segera", "⚠️ Tinggi - Intervensi Keutamaan", "🟡 Pantau Rapi"],
        default="🟢 Stabil"
    )
    st.dataframe(d.sort_values("IKM_komposit_model", ascending=False)[
        ["negeri","daerah","IKM_komposit_model","tahap_risiko_model","risiko_digital","kadar_hate_speech","keutamaan_intervensi","status_amaran"]
    ], use_container_width=True, height=560)

def render_timeline(timeline):
    st.markdown("<div class='section-title'>Milestone Pelaksanaan 18 Bulan</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Setiap fasa dipadankan dengan objektif TOR dan deliverable utama.</div>", unsafe_allow_html=True)

    t = timeline.copy()
    t["start"] = range(len(t))
    t["finish"] = t["start"] + 1
    fig = px.timeline(t, x_start="start", x_end="finish", y="fasa", color="objektif",
                      hover_data=["bulan","deliverable"], title="Garis Masa Pelaksanaan Kajian")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=640, plot_bgcolor="rgba(255,255,255,0)", paper_bgcolor="rgba(255,255,255,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(timeline, use_container_width=True, height=360)
