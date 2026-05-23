
import streamlit as st
import plotly.express as px
from utils.charts import bar_compare

def render(social, model):
    st.markdown("<div class='section-title'>Analitik Media Sosial & Big Data</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Simulasi analisis digital: sentimen, toksisiti, hate speech, platform, topik dan trend risiko.</div>", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Jumlah Rekod", f"{len(social):,}")
    c2.metric("Purata Risiko Digital", f"{social['risk_signal'].mean():.2f}" if len(social) else "0.00")
    c3.metric("Purata Toksik", f"{social['toxicity_score'].mean():.2f}" if len(social) else "0.00")
    hate = (social["hate_speech_flag"].astype(str).str.lower()=="ya").mean()*100 if len(social) else 0
    c4.metric("Kadar Hate Speech", f"{hate:.2f}%")

    col1, col2 = st.columns(2)
    with col1:
        platform = social["platform"].value_counts().reset_index()
        platform.columns = ["platform","bilangan"]
        st.plotly_chart(bar_compare(platform, x="platform", y="bilangan", title="Bilangan Rekod Mengikut Platform", height=430), use_container_width=True)
    with col2:
        isu = social["isu"].value_counts().reset_index()
        isu.columns = ["isu","bilangan"]
        st.plotly_chart(bar_compare(isu, x="isu", y="bilangan", title="Topik / Isu Digital", height=430), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        sample = social.sample(min(6000, len(social)), random_state=7) if len(social) else social
        fig = px.scatter(sample, x="sentiment_score", y="toxicity_score", size="engagement",
                         color="tahap_risiko_digital", hover_data=["negeri","daerah","platform","isu"],
                         title="Sentimen vs Toksisiti vs Engagement")
        fig.update_layout(height=520, plot_bgcolor="rgba(255,255,255,0)", paper_bgcolor="rgba(255,255,255,0)")
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        s = social.copy()
        if "tarikh" in s.columns:
            s["bulan"] = s["tarikh"].dt.to_period("M").astype(str)
            trend = s.groupby("bulan", as_index=False).agg(risiko=("risk_signal","mean"), toksik=("toxicity_score","mean"))
            fig = px.line(trend, x="bulan", y=["risiko","toksik"], markers=True, title="Trend Bulanan Risiko Digital")
            fig.update_layout(height=520, plot_bgcolor="rgba(255,255,255,0)", paper_bgcolor="rgba(255,255,255,0)")
            st.plotly_chart(fig, use_container_width=True)
