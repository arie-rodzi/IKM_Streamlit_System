
import streamlit as st
import pandas as pd
from utils.model_engine import intervention_plan
from utils.charts import radar

def render(model):
    st.markdown("<div class='section-title'>Lokasi & Cadangan Intervensi</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Setiap lokasi dijana cadangan intervensi berdasarkan indikator pencetus utama.</div>", unsafe_allow_html=True)

    if len(model) == 0:
        st.warning("Tiada data lokasi selepas penapis.")
        return

    model_sorted = model.sort_values("IKM_komposit_model", ascending=False)
    labels = model_sorted.apply(lambda r: f"{r['negeri']} | {r['daerah']} | IKM {r['IKM_komposit_model']:.2f}", axis=1).tolist()
    selected = st.selectbox("Pilih lokasi", labels)
    idx = labels.index(selected)
    row = model_sorted.iloc[idx]

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("IKM Komposit", f"{row['IKM_komposit_model']:.2f}")
    c2.metric("Tahap Risiko", row["tahap_risiko_model"])
    c3.metric("Keutamaan", row["keutamaan_intervensi"])
    c4.metric("Bil. Responden", f"{int(row['bil_responden']):,}")

    drivers, actions = intervention_plan(row)
    col1, col2 = st.columns([.85, 1.15])
    with col1:
        st.markdown("#### Indikator Pencetus Utama")
        drv = pd.DataFrame(drivers, columns=["Indikator", "Skor"])
        st.dataframe(drv, use_container_width=True, height=230)

        labels_r = ["Ekonomi","Politik","Sosial","Digital","Keselamatan","Kepercayaan","Perpaduan","Risiko Digital"]
        vals = [row["ekonomi"], row["politik"], row["sosial"], row["digital"], row["keselamatan"], row["defisit_kepercayaan"], row["risiko_perpaduan"], row["risiko_digital"]]
        st.plotly_chart(radar(labels_r, vals, "Profil Risiko Lokasi"), use_container_width=True)
    with col2:
        st.markdown("#### Pelan Intervensi Dicadangkan")
        for i, (title, desc) in enumerate(actions, 1):
            st.markdown(f"""
            <div class="glass-card">
                <b>{i}. {title}</b><br>
                {desc}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Jadual Tindakan Ringkas")
        plan = pd.DataFrame({
            "Fasa": ["0–30 hari", "1–3 bulan", "3–6 bulan"],
            "Tindakan": ["Amaran awal & taskforce setempat", "Program intervensi komuniti", "Penilaian impak & kemas kini model"],
            "Pemilik": ["JPNIN/Agensi berkaitan", "Komuniti + NGO + Agensi", "Penyelidik + Kerajaan"],
            "Output": ["Laporan risiko", "Pengurangan indikator pencetus", "Skor IKM dikemas kini"]
        })
        st.dataframe(plan, use_container_width=True)
