
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.model_engine import demographic_cross, percentage_table
from utils.charts import donut, bar_compare, RISK_COLORS

def _indicator_cols(df):
    cols = [
        "skor_ekonomi", "skor_politik", "skor_sosial", "skor_digital",
        "skor_keselamatan", "skor_defisit_kepercayaan", "skor_risiko_perpaduan",
        "IKM_survey_model"
    ]
    return [c for c in cols if c in df.columns]

def _nice_name(x):
    return str(x).replace("skor_", "").replace("_", " ").title()

def demographic_profile(resp_model, group_col):
    if len(resp_model) == 0 or group_col not in resp_model.columns:
        return pd.DataFrame()
    g = resp_model.groupby(group_col, dropna=False).agg(
        bilangan=("respondent_id", "count"),
        purata_IKM=("IKM_survey_model", "mean"),
        purata_ekonomi=("skor_ekonomi", "mean"),
        purata_politik=("skor_politik", "mean"),
        purata_sosial=("skor_sosial", "mean"),
        purata_digital=("skor_digital", "mean"),
        purata_keselamatan=("skor_keselamatan", "mean"),
        purata_defisit_kepercayaan=("skor_defisit_kepercayaan", "mean"),
        purata_risiko_perpaduan=("skor_risiko_perpaduan", "mean")
    ).reset_index()
    g[group_col] = g[group_col].fillna("Tidak diketahui").astype(str)
    total = g["bilangan"].sum()
    g["peratus"] = (g["bilangan"] / total * 100).round(2)
    num_cols = g.select_dtypes(include="number").columns
    g[num_cols] = g[num_cols].round(2)
    return g.sort_values("purata_IKM", ascending=False)

def risk_by_group(resp_model, group_col):
    if len(resp_model) == 0:
        return pd.DataFrame()
    tab = resp_model.groupby([group_col, "tahap_risiko_model"], dropna=False).size().reset_index(name="bilangan")
    total = tab.groupby(group_col)["bilangan"].transform("sum")
    tab["peratus_dalam_kumpulan"] = (tab["bilangan"] / total * 100).round(2)
    tab[group_col] = tab[group_col].fillna("Tidak diketahui").astype(str)
    return tab

def render_group_section(resp_model, group_col, title, explanation):
    st.markdown(f"## {title}")
    st.markdown(f"<div class='callout'>{explanation}</div>", unsafe_allow_html=True)

    profile = demographic_profile(resp_model, group_col)
    risk_tab = risk_by_group(resp_model, group_col)

    if profile.empty:
        st.warning(f"Kolum {group_col} tidak ditemui dalam data.")
        return

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Bil. Kategori", f"{profile[group_col].nunique():,}")
    k2.metric("Jumlah Responden", f"{int(profile['bilangan'].sum()):,}")
    k3.metric("IKM Tertinggi", f"{profile['purata_IKM'].max():.2f}")
    k4.metric("Kategori Tertinggi", str(profile.iloc[0][group_col]))

    c1, c2 = st.columns([1.05, .95])
    with c1:
        fig = px.bar(
            profile.sort_values("purata_IKM", ascending=False),
            x=group_col,
            y="purata_IKM",
            color="purata_IKM",
            text_auto=".2f",
            color_continuous_scale="Turbo",
            title=f"Purata IKM Mengikut {title}"
        )
        fig.update_layout(height=430, xaxis_tickangle=-35, plot_bgcolor="rgba(255,255,255,0)", paper_bgcolor="rgba(255,255,255,0)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.pie(profile, names=group_col, values="bilangan", hole=.5, title=f"Komposisi Responden Mengikut {title}")
        fig2.update_traces(textinfo="percent+label", marker=dict(line=dict(color="white", width=2)))
        fig2.update_layout(height=430, paper_bgcolor="rgba(255,255,255,0)")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Pecahan Tahap Risiko Dalam Setiap Kumpulan")
    fig3 = px.bar(
        risk_tab,
        x=group_col,
        y="peratus_dalam_kumpulan",
        color="tahap_risiko_model",
        barmode="stack",
        text_auto=".1f",
        color_discrete_map=RISK_COLORS,
        title=f"Peratus Risiko Mengikut {title}"
    )
    fig3.update_layout(height=430, xaxis_tickangle=-35, plot_bgcolor="rgba(255,255,255,0)", paper_bgcolor="rgba(255,255,255,0)")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### Profil Indikator Mengikut Kumpulan")
    melt_cols = [
        "purata_ekonomi", "purata_politik", "purata_sosial", "purata_digital",
        "purata_keselamatan", "purata_defisit_kepercayaan", "purata_risiko_perpaduan"
    ]
    long = profile[[group_col] + melt_cols].melt(id_vars=group_col, var_name="indikator", value_name="skor")
    long["indikator"] = long["indikator"].str.replace("purata_", "").str.replace("_", " ").str.title()

    fig4 = px.bar(
        long,
        x=group_col,
        y="skor",
        color="indikator",
        barmode="group",
        title=f"Perbandingan Indikator Terperinci Mengikut {title}"
    )
    fig4.update_layout(height=520, xaxis_tickangle=-35, plot_bgcolor="rgba(255,255,255,0)", paper_bgcolor="rgba(255,255,255,0)")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("### Jadual Ringkasan")
    st.dataframe(profile, use_container_width=True, height=360)

def render(resp_model):
    st.markdown("<div class='section-title'>Analisis Demografi Terperinci</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Analisis ini memfokus kepada kaum/etnik, kumpulan pendapatan dan tahap pendidikan. Semua peratus dikira daripada jumlah responden selepas penapis.</div>", unsafe_allow_html=True)

    if len(resp_model) == 0:
        st.warning("Tiada data responden selepas penapis.")
        return

    st.markdown(f"<div class='callout'><b>Formula peratus:</b> bilangan kategori ÷ jumlah responden × 100. <b>Jumlah responden semasa:</b> {len(resp_model):,}.</div>", unsafe_allow_html=True)

    # Top summary cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jumlah Responden", f"{len(resp_model):,}")
    c2.metric("Purata IKM", f"{resp_model['IKM_survey_model'].mean():.2f}")
    c3.metric("Kategori Etnik", f"{resp_model['etnik'].nunique() if 'etnik' in resp_model else 0}")
    c4.metric("Kategori Pendapatan", f"{resp_model['pendapatan'].nunique() if 'pendapatan' in resp_model else 0}")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Kaum / Etnik",
        "Kumpulan Pendapatan",
        "Tahap Pendidikan",
        "Matriks Gabungan"
    ])

    with tab1:
        render_group_section(
            resp_model,
            "etnik",
            "Kaum / Etnik",
            "Paparan ini menunjukkan komposisi responden, purata IKM, pecahan tahap risiko dan indikator pencetus mengikut kaum/etnik."
        )

    with tab2:
        render_group_section(
            resp_model,
            "pendapatan",
            "Kumpulan Pendapatan",
            "Paparan ini menilai sama ada kumpulan B40, M40 dan T20 menunjukkan corak risiko IKM yang berbeza."
        )

    with tab3:
        render_group_section(
            resp_model,
            "pendidikan",
            "Tahap Pendidikan",
            "Paparan ini membandingkan skor IKM, risiko dan indikator utama mengikut tahap pendidikan responden."
        )

    with tab4:
        st.markdown("## Matriks Gabungan Demografi")
        st.markdown("<div class='callout'>Matriks ini lebih berguna untuk briefing kerana ia menunjukkan kumpulan mana yang mempunyai purata IKM lebih tinggi mengikut kombinasi demografi.</div>", unsafe_allow_html=True)

        left, right = st.columns(2)
        with left:
            row_dim = st.selectbox("Dimensi baris", ["etnik", "pendapatan", "pendidikan", "jantina", "kumpulan_umur", "lokasi"], index=0)
        with right:
            col_dim = st.selectbox("Dimensi lajur", ["pendapatan", "pendidikan", "etnik", "jantina", "kumpulan_umur", "lokasi"], index=0)

        if row_dim == col_dim:
            st.warning("Pilih dua dimensi yang berbeza.")
        else:
            pivot_count = pd.pivot_table(
                resp_model,
                index=row_dim,
                columns=col_dim,
                values="respondent_id",
                aggfunc="count",
                fill_value=0
            )
            pivot_ikm = pd.pivot_table(
                resp_model,
                index=row_dim,
                columns=col_dim,
                values="IKM_survey_model",
                aggfunc="mean"
            ).round(2)

            c1, c2 = st.columns(2)
            with c1:
                fig_count = px.imshow(
                    pivot_count,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale="Blues",
                    title=f"Bilangan Responden: {row_dim} × {col_dim}"
                )
                fig_count.update_layout(height=500, paper_bgcolor="rgba(255,255,255,0)")
                st.plotly_chart(fig_count, use_container_width=True)

            with c2:
                fig_ikm = px.imshow(
                    pivot_ikm,
                    text_auto=".2f",
                    aspect="auto",
                    color_continuous_scale="Turbo",
                    title=f"Purata IKM: {row_dim} × {col_dim}"
                )
                fig_ikm.update_layout(height=500, paper_bgcolor="rgba(255,255,255,0)")
                st.plotly_chart(fig_ikm, use_container_width=True)

            st.markdown("### Jadual Bilangan")
            st.dataframe(pivot_count, use_container_width=True)
            st.markdown("### Jadual Purata IKM")
            st.dataframe(pivot_ikm, use_container_width=True)
