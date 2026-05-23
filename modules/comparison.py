
import streamlit as st
import plotly.express as px
from utils.charts import bar_compare, radar
from utils.model_engine import intervention_plan

def render(model):
    st.markdown("<div class='section-title'>Perbandingan Negeri & Daerah</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Bandingkan prestasi IKM antara negeri, daerah dan indikator pencetus risiko.</div>", unsafe_allow_html=True)

    state = model.groupby("negeri", as_index=False).agg(
        IKM=("IKM_komposit_model","mean"),
        survey=("IKM_survey","mean"),
        digital=("risiko_digital","mean"),
        toksik=("toksik","mean"),
        bil_responden=("bil_responden","sum"),
        bil_post=("bil_post","sum")
    ).sort_values("IKM", ascending=False)
    for c in ["IKM","survey","digital","toksik"]:
        state[c] = state[c].round(2)

    col1, col2 = st.columns([1.2, .8])
    with col1:
        fig = bar_compare(state, x="negeri", y="IKM", title="Perbandingan IKM Antara Negeri/Wilayah", height=500)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.dataframe(state, use_container_width=True, height=500)

    st.markdown("### Perbandingan Dua Lokasi")
    labels = model.apply(lambda r: f"{r['negeri']} | {r['daerah']}", axis=1).tolist()
    a,b = st.columns(2)
    loc1 = a.selectbox("Lokasi 1", labels, index=0 if labels else None)
    loc2 = b.selectbox("Lokasi 2", labels, index=min(1, len(labels)-1) if labels else None)

    if loc1 and loc2:
        r1 = model.iloc[labels.index(loc1)]
        r2 = model.iloc[labels.index(loc2)]
        dims = ["ekonomi","politik","sosial","digital","keselamatan","defisit_kepercayaan","risiko_perpaduan","risiko_digital"]
        names = ["Ekonomi","Politik","Sosial","Digital","Keselamatan","Kepercayaan","Perpaduan","Risiko Digital"]
        fig = px.line_polar(
            r=model.loc[[r1.name, r2.name], dims].melt(ignore_index=False).reset_index()["value"],
            theta=names*2
        )
        fig = radar(names, [r1[d] for d in dims], f"Radar {loc1}")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Jadual Ranking Daerah")
    st.dataframe(model.sort_values("IKM_komposit_model", ascending=False), use_container_width=True, height=520)
