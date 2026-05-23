
import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import demographic_summary, state_comparison, indicator_summary, district_rank, monthly_trends, INDICATOR_COLS, INDICATOR_LABELS
from interventions import recommend, build_intervention_table
from visualizations import bar, pie, line, heatmap, radar, scatter_social, apply_layout
from styles import glass_open, glass_close, RISK_COLORS, COLORWAY


def page_executive(resp, social, district):
    c1,c2 = st.columns([1.25,1])
    with c1:
        glass_open("Perbandingan Negeri/Wilayah", "Ranking purata IKM komposit untuk mengenal pasti negeri berisiko tinggi.")
        sc = state_comparison(district)
        fig = bar(sc.head(16), x="purata_IKM", y="negeri", color="tahap_risiko", orientation="h", title="Ranking IKM Mengikut Negeri/Wilayah", height=560, text="purata_IKM")
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)
        glass_close()
    with c2:
        glass_open("Komposisi Risiko Daerah", "Taburan daerah mengikut tahap risiko.")
        rc = district["tahap_risiko"].value_counts().reset_index(); rc.columns=["Tahap Risiko","Bilangan"]
        st.plotly_chart(pie(rc, "Tahap Risiko", "Bilangan", "Taburan Risiko Daerah", 360), use_container_width=True)
        st.dataframe(sc, use_container_width=True, height=245)
        glass_close()

    glass_open("Top Hotspot Daerah", "Daerah paling tinggi berdasarkan IKM komposit, risiko digital dan kadar hotspot.")
    top = district_rank(district, 30)
    fig2 = bar(top.head(20), x="IKM_komposit", y="daerah", color="tahap_risiko", orientation="h", title="Top 20 Hotspot Daerah", height=650, text="IKM_komposit")
    fig2.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(top, use_container_width=True, height=360)
    glass_close()


def page_demographic(resp):
    st.markdown("### Analisis Demografi Responden")
    demos = demographic_summary(resp)
    a,b,c = st.columns(3)
    cards = [("Jantina", "jantina"), ("Kumpulan Umur", "kumpulan_umur"), ("Etnik", "etnik")]
    for col, (title, key) in zip([a,b,c], cards):
        with col:
            glass_open(title, "Bilangan dan purata IKM")
            if key in demos:
                st.plotly_chart(bar(demos[key], x=key, y="bilangan", title=f"Taburan {title}", height=300, text="bilangan"), use_container_width=True)
                st.plotly_chart(bar(demos[key], x=key, y="purata_IKM", title=f"Purata IKM {title}", height=300, text="purata_IKM"), use_container_width=True)
            glass_close()
    d,e,f = st.columns(3)
    cards2 = [("Pendidikan", "pendidikan"), ("Pendapatan", "pendapatan"), ("Lokasi", "lokasi")]
    for col, (title, key) in zip([d,e,f], cards2):
        with col:
            glass_open(title, "Segmentasi risiko mengikut profil")
            if key in demos:
                st.plotly_chart(bar(demos[key], x=key, y="purata_IKM", title=f"Purata IKM {title}", height=330, text="purata_IKM"), use_container_width=True)
                st.dataframe(demos[key], use_container_width=True, height=165)
            glass_close()


def page_location(resp, social, district):
    left, right = st.columns([1,1])
    with left:
        glass_open("Perbandingan Antara Daerah", "Bandingkan daerah dalam negeri/penapis semasa.")
        top = district.sort_values("IKM_komposit", ascending=False).head(35)
        fig = bar(top, x="IKM_komposit", y="daerah", color="tahap_risiko", orientation="h", title="Ranking Daerah", height=720, text="IKM_komposit")
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)
        glass_close()
    with right:
        glass_open("Intervensi Lokasi", "Pilih satu lokasi untuk pelan tindakan automatik.")
        if len(district):
            opts = district.sort_values("IKM_komposit", ascending=False).apply(lambda r: f"{r['negeri']} | {r['daerah']}", axis=1).tolist()
            chosen = st.selectbox("Pilih negeri | daerah", opts)
            n,d = [x.strip() for x in chosen.split('|')]
            row = district[(district.negeri==n)&(district.daerah==d)].iloc[0]
            alert, sla, top, actions = recommend(row)
            st.markdown(f"<div class='critical-box'><h3>{d}, {n}</h3><b>Amaran:</b> {alert}<br><b>SLA:</b> {sla}<br><b>IKM:</b> {row['IKM_komposit']:.2f}</div>", unsafe_allow_html=True)
            st.write("**Pencetus utama:**")
            st.dataframe(pd.DataFrame(top, columns=["Pencetus", "Skor"]), use_container_width=True, height=150)
            labels = ["Ekonomi","Politik","Sosial","Digital","Toksik","Risiko Digital"]
            vals = [row.get("purata_ekonomi",0),row.get("purata_politik",0),row.get("purata_sosial",0),row.get("purata_digital",0),row.get("purata_toksik",0),row.get("purata_risiko_digital",0)]
            st.plotly_chart(radar(labels, vals, "Radar Pencetus Risiko", 380), use_container_width=True)
            for i,(t,desc) in enumerate(actions,1):
                st.markdown(f"<div class='insight'><b>{i}. {t}</b><br>{desc}</div>", unsafe_allow_html=True)
        glass_close()


def page_indicators(resp, district):
    l,r = st.columns([1,1])
    with l:
        glass_open("Indikator Utama IKM", "Purata skor indikator survey.")
        ind = indicator_summary(resp)
        st.plotly_chart(bar(ind, x="indikator", y="purata", title="Purata Indikator Nasional", height=440, text="purata"), use_container_width=True)
        st.dataframe(ind, use_container_width=True)
        glass_close()
    with r:
        glass_open("Korelasi Indikator", "Hubungan antara domain skor dan IKM.")
        cols = [c for c in INDICATOR_COLS + ["skor_IKM"] if c in resp.columns]
        corr = resp[cols].corr()
        corr.index = [INDICATOR_LABELS.get(x,x) for x in corr.index]
        corr.columns = [INDICATOR_LABELS.get(x,x) for x in corr.columns]
        st.plotly_chart(heatmap(corr, "Matriks Korelasi Indikator", 520), use_container_width=True)
        glass_close()
    glass_open("Perbandingan Indikator Mengikut Negeri", "Membantu lihat driver utama setiap negeri.")
    if len(resp):
        tmp = resp.groupby("negeri")[INDICATOR_COLS].mean().reset_index()
        tmp_long = tmp.melt(id_vars="negeri", var_name="indikator", value_name="skor")
        tmp_long["indikator"] = tmp_long["indikator"].map(INDICATOR_LABELS)
        fig = px.bar(tmp_long, x="negeri", y="skor", color="indikator", barmode="group", title="Indikator Mengikut Negeri")
        fig.update_layout(height=600, template="plotly_dark", colorway=COLORWAY, xaxis_tickangle=-35, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,.03)")
        st.plotly_chart(fig, use_container_width=True)
    glass_close()


def page_social(resp, social, district):
    a,b,c = st.columns(3)
    with a:
        glass_open("Platform", "Sumber data digital")
        platform = social["platform"].value_counts().reset_index(); platform.columns=["platform","bilangan"]
        st.plotly_chart(bar(platform, x="platform", y="bilangan", title="Platform Media Sosial", height=350, text="bilangan"), use_container_width=True)
        glass_close()
    with b:
        glass_open("Isu", "Topik paling aktif")
        isu = social["isu"].value_counts().reset_index(); isu.columns=["isu","bilangan"]
        st.plotly_chart(bar(isu, x="isu", y="bilangan", title="Topik / Isu", height=350, text="bilangan"), use_container_width=True)
        glass_close()
    with c:
        glass_open("Hate Speech", "Isyarat toksik digital")
        hs = social["hate_speech_flag"].value_counts().reset_index(); hs.columns=["hate_speech_flag","bilangan"]
        st.plotly_chart(pie(hs, "hate_speech_flag", "bilangan", "Kadar Hate Speech", 350), use_container_width=True)
        glass_close()
    glass_open("Big Data Scatter", "Hubungan sentimen, toksisiti dan engagement.")
    st.plotly_chart(scatter_social(social, height=520), use_container_width=True)
    glass_close()
    glass_open("Trend Bulanan Survey vs Digital", "Mengesan perubahan risiko sepanjang tempoh simulasi.")
    tr = monthly_trends(resp, social)
    st.plotly_chart(line(tr, "bulan", [c for c in tr.columns if c!="bulan"], "Trend IKM dan Risiko Digital", 460), use_container_width=True)
    glass_close()


def page_warning(district):
    glass_open("Pusat Amaran Awal", "Senarai daerah mengikut SLA intervensi.")
    tbl = build_intervention_table(district)
    st.dataframe(tbl, use_container_width=True, height=520)
    count = tbl["amaran"].value_counts().reset_index(); count.columns=["amaran","bilangan"]
    st.plotly_chart(bar(count, x="amaran", y="bilangan", title="Bilangan Daerah Mengikut Tahap Amaran", height=380, text="bilangan"), use_container_width=True)
    glass_close()


def page_timeline(timeline):
    glass_open("Milestone 18 Bulan", "Hubungan aktiviti, objektif TOR dan deliverable.")
    st.dataframe(timeline, use_container_width=True, height=300)
    df = timeline.copy()
    df["start"] = range(len(df)); df["finish"] = df["start"] + 1
    fig = px.timeline(df, x_start="start", x_end="finish", y="fasa", color="objektif", hover_data=["bulan","deliverable"], title="Pelaksanaan Mengikut Bulan dan Objektif")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(apply_layout(fig, 650), use_container_width=True)
    glass_close()
