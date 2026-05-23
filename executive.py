
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.style import metric_card
from utils.charts import bar_compare, donut, RISK_COLORS
from utils.model_engine import risk_label

def render(model, resp_model, social):
    st.markdown("<div class='section-title'>Executive Intelligence Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Ringkasan nasional yang dikira terus daripada data semasa, bukan nilai hardcoded.</div>", unsafe_allow_html=True)

    avg = model["IKM_komposit_model"].mean() if len(model) else 0
    risk = risk_label(avg)
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(metric_card("IKM Komposit", f"{avg:.2f}", "Purata lokasi terpilih", risk), unsafe_allow_html=True)
    c2.markdown(metric_card("Tahap Risiko", risk, "Berdasarkan skor purata", risk), unsafe_allow_html=True)
    c3.markdown(metric_card("Responden", f"{len(resp_model):,}", "Jumlah selepas penapis"), unsafe_allow_html=True)
    c4.markdown(metric_card("Rekod Digital", f"{len(social):,}", "Media sosial / portal"), unsafe_allow_html=True)
    c5.markdown(metric_card("Lokasi Dipantau", f"{len(model):,}", "Daerah dalam paparan"), unsafe_allow_html=True)

    col1, col2 = st.columns([1.35, .9])
    with col1:
        top = model.sort_values("IKM_komposit_model", ascending=False).head(20)
        fig = bar_compare(top, x="IKM_komposit_model", y="daerah", color="tahap_risiko_model",
                          title="Perbandingan Top 20 Daerah Mengikut IKM Komposit", orientation="h", height=620)
        fig.update_layout(yaxis={"categoryorder":"total ascending"})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        risk_tab = model["tahap_risiko_model"].value_counts().reset_index()
        risk_tab.columns = ["Tahap Risiko", "Bilangan Daerah"]
        st.plotly_chart(donut(risk_tab, "Tahap Risiko", "Bilangan Daerah", "Komposisi Risiko Daerah"), use_container_width=True)

        state = model.groupby("negeri", as_index=False).agg(IKM=("IKM_komposit_model","mean")).sort_values("IKM", ascending=False)
        fig2 = px.bar(state, x="negeri", y="IKM", text_auto=".1f", title="Ranking Negeri/Wilayah")
        fig2.update_layout(height=330, xaxis_tickangle=-45, plot_bgcolor="rgba(255,255,255,0)", paper_bgcolor="rgba(255,255,255,0)")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='callout'><b>Output brief panel:</b> Paparan ini menunjukkan kedudukan negeri/daerah, lokasi hotspot, tahap risiko dan keutamaan intervensi berdasarkan model IKM komposit.</div>", unsafe_allow_html=True)
