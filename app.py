import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sistem Pintar IKM Nasional", page_icon="🇲🇾", layout="wide")
st.markdown("""
<style>
.block-container{padding-top:1rem}.hero{background:linear-gradient(135deg,#061735,#0b3d66 65%,#c5962f);padding:28px;border-radius:24px;color:white;box-shadow:0 15px 38px rgba(0,0,0,.18);margin-bottom:18px}.hero h1{font-size:36px;margin:0}.hero p{font-size:16px;opacity:.92}.card{background:white;border:1px solid #dbe7f3;border-radius:20px;padding:18px;box-shadow:0 10px 26px rgba(11,31,58,.07);margin-bottom:14px}.kpi{font-size:30px;font-weight:900;color:#061735}.label{font-size:13px;color:#536b84;font-weight:800}.small{font-size:13px;color:#52616b}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file=None):
    xls = pd.ExcelFile(file if file else "IKM_Simulation_Data_Malaysia.xlsx")
    return {
        "resp": pd.read_excel(xls, "respondent_data"),
        "soc": pd.read_excel(xls, "social_media_data"),
        "dist": pd.read_excel(xls, "district_summary"),
        "w": pd.read_excel(xls, "parameter_weighting"),
        "time": pd.read_excel(xls, "timeline_18_bulan"),
    }

def risk_label(x):
    if x < 40: return "Rendah"
    if x < 60: return "Sederhana"
    if x < 75: return "Tinggi"
    return "Kritikal"

def color_map():
    return {"Rendah":"#0b6b43","Sederhana":"#b88720","Tinggi":"#d35400","Kritikal":"#c0392b"}

def calc_ikm(df, w):
    mp = {str(r.domain).lower(): float(r.berat_simulasi) for r in w.itertuples()}
    cols = {"ekonomi":"skor_ekonomi","politik":"skor_politik","sosial":"skor_sosial","digital/media":"skor_digital","keselamatan":"skor_keselamatan","defisit kepercayaan":"skor_defisit_kepercayaan","risiko perpaduan":"skor_risiko_perpaduan"}
    out = np.zeros(len(df))
    for k, c in cols.items(): out += df[c].fillna(0).to_numpy() * mp.get(k, 0)
    return np.round(out, 2)

def intervention(row):
    vals = {
        "Ekonomi": row.get("purata_ekonomi", 0),
        "Politik": row.get("purata_politik", 0),
        "Sosial": row.get("purata_sosial", 0),
        "Digital/Media": row.get("purata_digital", 0),
        "Toksik Media Sosial": row.get("purata_toksik", 0),
        "Hate Speech": row.get("kadar_hate_speech", 0) * 100 if pd.notna(row.get("kadar_hate_speech", np.nan)) else 0,
    }
    top = sorted(vals.items(), key=lambda x: x[1], reverse=True)[:3]
    actions = []
    for k, v in top:
        if k in ["Digital/Media", "Toksik Media Sosial", "Hate Speech"]:
            actions.append("Aktifkan pemantauan digital, counter-narrative, fact-checking dan laporan sentimen mingguan.")
        elif k == "Ekonomi": actions.append("Laksanakan engagement kos sara hidup, bantuan bersasar dan komunikasi dasar ekonomi setempat.")
        elif k == "Politik": actions.append("Adakan dialog rentas komuniti, pemetaan naratif dan pengurusan isu sensitif.")
        elif k == "Sosial": actions.append("Perkukuh program kohesi sosial, mediator komuniti dan aktiviti rentas kumpulan.")
        else: actions.append("Tingkatkan saluran aduan pantas, koordinasi keselamatan dan rondaan komuniti.")
    risk = row.get("tahap_risiko", "Sederhana")
    urgency = {
        "Kritikal":"TINDAKAN SEGERA: taskforce daerah, pemantauan harian dan laporan kepada agensi penyelaras.",
        "Tinggi":"TINDAKAN KEUTAMAAN: intervensi 30 hari, pemantauan mingguan dan komunikasi risiko.",
        "Sederhana":"PANTAUAN BERKALA: engagement bulanan dan pengesanan isu berulang.",
        "Rendah":"KEKALKAN: pemantauan ringan dan program perpaduan berkala.",
    }.get(risk, "Pantau")
    return urgency, top, list(dict.fromkeys(actions))[:3]

st.sidebar.title("🇲🇾 Sistem IKM")
upload = st.sidebar.file_uploader("Muat naik Excel .xlsx", type=["xlsx"])
data = load_data(upload)
resp, soc, dist, w, time = data["resp"], data["soc"], data["dist"], data["w"], data["time"]

negeri = ["Semua"] + sorted(dist.negeri.dropna().unique())
sel_n = st.sidebar.selectbox("Negeri/Wilayah", negeri)
daerah = ["Semua"] + sorted((dist.loc[dist.negeri == sel_n, "daerah"] if sel_n != "Semua" else dist.daerah).dropna().unique())
sel_d = st.sidebar.selectbox("Daerah", daerah)
sel_r = st.sidebar.selectbox("Tahap Risiko", ["Semua", "Rendah", "Sederhana", "Tinggi", "Kritikal"])

fd, fr, fs = dist.copy(), resp.copy(), soc.copy()
if sel_n != "Semua":
    fd = fd[fd.negeri == sel_n]; fr = fr[fr.negeri == sel_n]; fs = fs[fs.negeri == sel_n]
if sel_d != "Semua":
    fd = fd[fd.daerah == sel_d]; fr = fr[fr.daerah == sel_d]; fs = fs[fs.daerah == sel_d]
if sel_r != "Semua":
    fd = fd[fd.tahap_risiko == sel_r]; fr = fr[fr.tahap_risiko == sel_r]

st.markdown('<div class="hero"><h1>Sistem Pintar Indeks Ketegangan Masyarakat (IKM)</h1><p>Prototype nasional berasaskan Python + Streamlit: pengiraan indeks, media sosial big data, hotspot, amaran awal dan cadangan intervensi mengikut lokasi.</p></div>', unsafe_allow_html=True)

avg = fd.IKM_komposit.mean() if len(fd) else 0
rnow = risk_label(avg) if avg else "-"
metrics = [("Purata IKM", f"{avg:.2f}"), ("Tahap Risiko", rnow), ("Responden", f"{int(fd.bil_responden.sum()) if len(fd) else len(fr):,}"), ("Data Media Sosial", f"{int(fd.bil_post.sum()) if len(fd) else len(fs):,}"), ("Daerah Dipaparkan", f"{len(fd):,}")]
for c, (a, b) in zip(st.columns(5), metrics):
    c.markdown(f'<div class="card"><div class="label">{a}</div><div class="kpi">{b}</div></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 Nasional", "🧮 Pengiraan IKM", "📍 Intervensi Lokasi", "📊 Indikator", "🌐 Big Data Media Sosial", "🚨 Amaran Awal", "🗓️ Milestone"])

with tabs[0]:
    c1, c2 = st.columns([1.35, 1])
    with c1:
        p = fd.sort_values("IKM_komposit", ascending=False).head(30)
        fig = px.bar(p, x="IKM_komposit", y="daerah", color="tahap_risiko", orientation="h", hover_data=["negeri", "bil_responden", "bil_post"], color_discrete_map=color_map(), title="Top Daerah Mengikut IKM Komposit")
        fig.update_layout(height=650, yaxis={"categoryorder":"total ascending"}, plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        rc = fd.tahap_risiko.value_counts().reset_index(); rc.columns = ["Tahap Risiko", "Bilangan Daerah"]
        st.plotly_chart(px.pie(rc, names="Tahap Risiko", values="Bilangan Daerah", color="Tahap Risiko", color_discrete_map=color_map(), title="Taburan Risiko"), use_container_width=True)
        ss = fd.groupby("negeri", as_index=False).IKM_komposit.mean().sort_values("IKM_komposit", ascending=False)
        st.plotly_chart(px.bar(ss, x="negeri", y="IKM_komposit", title="Purata IKM Mengikut Negeri"), use_container_width=True)

with tabs[1]:
    st.info("IKM = Σ(berat indikator × skor indikator). IKM Komposit Daerah = 60% Survey + 30% Risiko Digital + 10% Hotspot.")
    c1, c2 = st.columns(2)
    c1.dataframe(w, use_container_width=True)
    c2.plotly_chart(px.bar(w, x="domain", y="berat_simulasi", text_auto=".2f", title="Berat Indikator"), use_container_width=True)
    sm = fr.head(500).copy()
    if len(sm):
        sm["skor_IKM_dikira_semula"] = calc_ikm(sm, w)
        st.dataframe(sm[["respondent_id", "negeri", "daerah", "skor_IKM", "skor_IKM_dikira_semula", "tahap_risiko"]], use_container_width=True, height=320)

with tabs[2]:
    st.subheader("Cadangan Intervensi Mengikut Lokasi")
    if len(fd):
        locs = fd.sort_values("IKM_komposit", ascending=False).apply(lambda x: f"{x.negeri} | {x.daerah}", axis=1).tolist()
        loc = st.selectbox("Pilih lokasi", locs)
        n, d = [x.strip() for x in loc.split("|")]
        row = fd[(fd.negeri == n) & (fd.daerah == d)].iloc[0]
        c1, c2, c3 = st.columns(3); c1.metric("IKM Komposit", f"{row.IKM_komposit:.2f}"); c2.metric("Tahap Risiko", row.tahap_risiko); c3.metric("Keutamaan", row.hotspot_keutamaan)
        urgency, top, actions = intervention(row)
        st.warning(urgency) if row.tahap_risiko in ["Tinggi", "Kritikal"] else st.info(urgency)
        st.dataframe(pd.DataFrame(top, columns=["Indikator Pencetus", "Skor"]), use_container_width=True)
        for i, a in enumerate(actions, 1): st.markdown(f"**{i}. {a}**")
        names = ["Ekonomi", "Politik", "Sosial", "Digital", "Toksik", "Risiko Digital"]
        vals = [row.get(x, 0) for x in ["purata_ekonomi", "purata_politik", "purata_sosial", "purata_digital", "purata_toksik", "purata_risiko_digital"]]
        fig = go.Figure(go.Scatterpolar(r=vals, theta=names, fill="toself")); fig.update_layout(polar=dict(radialaxis=dict(range=[0,100], visible=True)), height=420, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else: st.warning("Tiada data untuk penapis ini.")

with tabs[3]:
    cols = ["skor_ekonomi", "skor_politik", "skor_sosial", "skor_digital", "skor_keselamatan", "skor_defisit_kepercayaan", "skor_risiko_perpaduan"]
    isum = fr[cols].mean().reset_index(); isum.columns = ["Indikator", "Purata Skor"]; isum.Indikator = isum.Indikator.str.replace("skor_", "").str.replace("_", " ").str.title()
    st.plotly_chart(px.bar(isum.sort_values("Purata Skor", ascending=False), x="Indikator", y="Purata Skor", text_auto=".2f", title="Purata Skor Indikator"), use_container_width=True)
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.box(fr, x="tahap_risiko", y="skor_IKM", color="tahap_risiko", color_discrete_map=color_map(), title="Taburan IKM"), use_container_width=True)
    c2.plotly_chart(px.imshow(fr[cols + ["skor_IKM"]].corr(), text_auto=".2f", title="Korelasi Indikator"), use_container_width=True)

with tabs[4]:
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.bar(fs.platform.value_counts().reset_index().rename(columns={"platform":"Platform", "count":"Bilangan"}), x="Platform", y="Bilangan", title="Sumber Media Sosial"), use_container_width=True)
    c2.plotly_chart(px.bar(fs.isu.value_counts().reset_index().rename(columns={"isu":"Isu", "count":"Bilangan"}), x="Isu", y="Bilangan", title="Isu Paling Kerap"), use_container_width=True)
    sample = fs.sample(min(5000, len(fs))) if len(fs) > 0 else fs
    st.plotly_chart(px.scatter(sample, x="sentiment_score", y="toxicity_score", color="tahap_risiko_digital", size="engagement", hover_data=["negeri", "daerah", "platform", "isu"], title="Sentimen vs Toksisiti"), use_container_width=True)
    tr = fs.copy(); tr["bulan"] = pd.to_datetime(tr.tarikh).dt.to_period("M").astype(str); tr = tr.groupby("bulan", as_index=False).risk_signal.mean()
    st.plotly_chart(px.line(tr, x="bulan", y="risk_signal", markers=True, title="Trend Risiko Digital Bulanan"), use_container_width=True)

with tabs[5]:
    ad = fd.copy(); ad["status_amaran"] = np.select([ad.IKM_komposit >= 75, ad.IKM_komposit >= 60, ad.IKM_komposit >= 45], ["🚨 Kritikal - Tindakan Segera", "⚠️ Tinggi - Intervensi Keutamaan", "🟡 Pantau Rapi"], default="🟢 Stabil")
    st.dataframe(ad.sort_values("IKM_komposit", ascending=False)[["negeri", "daerah", "IKM_komposit", "tahap_risiko", "status_amaran", "purata_toksik", "kadar_hate_speech", "bil_post"]], use_container_width=True, height=540)
    st.markdown("**Logik:** Kritikal ≥75; Tinggi ≥60; Pantau Rapi ≥45; Stabil <45.")

with tabs[6]:
    st.dataframe(time, use_container_width=True)
    tm = time.assign(start=np.arange(len(time)), finish=np.arange(len(time)) + 1)
    fig = px.timeline(tm, x_start="start", x_end="finish", y="fasa", color="objektif", hover_data=["bulan", "deliverable"], title="Garis Masa Pelaksanaan 18 Bulan")
    fig.update_yaxes(autorange="reversed"); fig.update_layout(height=620)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="card small"><b>Nota:</b> Data simulasi boleh diganti dengan data sebenar melalui upload Excel. Sesuai untuk demo proposal, pitching dan pembangunan sistem seterusnya.</div>', unsafe_allow_html=True)
