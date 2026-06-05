import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =========================================================
# IKM COMMAND CENTRE - PROTOTYPE
# Baca Excel/CSV 20,000 responden ATAU jana data simulasi 20,000
# =========================================================

st.set_page_config(
    page_title="IKM Command Centre",
    page_icon="🇲🇾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS PREMIUM TANPA SIDEBAR
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
header, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"], #MainMenu, footer {visibility:hidden; display:none;}
.block-container {padding-top:0.3rem !important; padding-bottom:3rem; max-width:1550px;}
.stApp {
    background:
        radial-gradient(circle at 8% 6%, rgba(253,230,138,.22), transparent 28%),
        radial-gradient(circle at 90% 7%, rgba(34,197,94,.18), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(14,165,233,.18), transparent 35%),
        linear-gradient(135deg, #020617 0%, #071426 42%, #0B2545 78%, #123C69 100%);
    color:#F8FAFC;
}
.hero {
    padding:30px 36px 24px 36px;
    border-radius:0 0 34px 34px;
    background:linear-gradient(135deg, rgba(255,255,255,.17), rgba(255,255,255,.055));
    border:1px solid rgba(255,255,255,.20);
    box-shadow:0 28px 80px rgba(0,0,0,.42);
    margin-bottom:20px;
}
.hero h1 {color:#FDE68A !important; font-size:38px; line-height:1.08; font-weight:950; margin:0; letter-spacing:-1.1px;}
.hero p {color:#DDEBFF; font-weight:600; font-size:15px; max-width:1150px; margin-top:10px;}
.badge {display:inline-block; padding:8px 13px; border-radius:999px; background:rgba(15,23,42,.58); border:1px solid rgba(253,230,138,.42); color:#FDE68A; font-weight:850; font-size:12px; margin-right:8px; margin-top:12px;}
.kpi-card {min-height:138px; padding:20px; border-radius:26px; background:linear-gradient(145deg, rgba(255,255,255,.19), rgba(255,255,255,.055)), radial-gradient(circle at top right, rgba(253,230,138,.20), transparent 42%); border:1px solid rgba(255,255,255,.23); box-shadow:0 22px 52px rgba(0,0,0,.34);}
.kpi-label {color:#E0F2FE; font-size:12px; font-weight:850; text-transform:uppercase; letter-spacing:.5px;}
.kpi-value {color:#FDE68A; font-size:35px; font-weight:950; margin-top:8px; line-height:1;}
.kpi-note {color:#BBF7D0; font-size:12px; font-weight:700; margin-top:12px;}
.panel {padding:20px 22px; border-radius:26px; background:rgba(255,255,255,.095); border:1px solid rgba(255,255,255,.18); box-shadow:0 18px 46px rgba(0,0,0,.30); margin-bottom:18px;}
.alert-red {background:linear-gradient(135deg, rgba(239,68,68,.22), rgba(255,255,255,.07)); border-left:7px solid #EF4444;}
.alert-orange {background:linear-gradient(135deg, rgba(245,158,11,.22), rgba(255,255,255,.07)); border-left:7px solid #F59E0B;}
.alert-green {background:linear-gradient(135deg, rgba(34,197,94,.18), rgba(255,255,255,.07)); border-left:7px solid #22C55E;}
h1,h2,h3 {color:#FDE68A !important; font-weight:950 !important;}
.stTabs [data-baseweb="tab-list"] {gap:8px; flex-wrap:wrap;}
.stTabs [data-baseweb="tab"] {border-radius:999px; padding:10px 17px; background:rgba(255,255,255,.08); color:#E0F2FE; border:1px solid rgba(255,255,255,.14); font-weight:800;}
.stTabs [aria-selected="true"] {background:linear-gradient(135deg, #FDE68A, #F59E0B) !important; color:#111827 !important; font-weight:950;}
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {background-color:rgba(255,255,255,.94); border-radius:16px; min-height:50px;}
.stDataFrame {border-radius:18px; overflow:hidden;}
.small {font-size:12px; color:#CBD5E1;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# KONFIGURASI DIMENSI, TEORI DAN INTERVENSI
# =========================================================
DIMENSIONS = {
    "D1_Sosial_Identiti": {"label":"D1 Sosial & Identiti", "theory":"Social Identity Theory", "weight":0.13},
    "D2_Agama_Budaya": {"label":"D2 Agama & Budaya", "theory":"Social Identity Theory", "weight":0.10},
    "D3_Ekonomi": {"label":"D3 Ketegangan Ekonomi", "theory":"Relative Deprivation Theory", "weight":0.18},
    "D4_Politik_Kuasa": {"label":"D4 Politik & Kuasa", "theory":"Conflict Theory", "weight":0.12},
    "D5_Generasi": {"label":"D5 Ketegangan Generasi", "theory":"General Strain Theory", "weight":0.10},
    "D6_Digital_Media": {"label":"D6 Digital & Media", "theory":"Media Ecology Theory", "weight":0.14},
    "D7_Institusi_Governans": {"label":"D7 Institusi & Governans", "theory":"Institutional Trust / Conflict Theory", "weight":0.11},
    "D8_Ketahanan_Sosial": {"label":"D8 Ketahanan Sosial", "theory":"Social Cohesion Theory", "weight":0.12},
}

INTERVENTION_BANK = {
    "D1_Sosial_Identiti": ["Dialog komuniti rentas etnik", "Program kejiranan harmoni", "Mediator komuniti di lokaliti berisiko"],
    "D2_Agama_Budaya": ["Sesi libat urus pemimpin agama", "Kempen hormat perbezaan budaya", "Protokol komunikasi isu sensitif"],
    "D3_Ekonomi": ["Program ekonomi komuniti setempat", "Pemetaan bantuan sosial", "Townhall kos sara hidup bersama agensi berkaitan"],
    "D4_Politik_Kuasa": ["Forum literasi sivik non-partisan", "Pemantauan naratif politik lokal", "Dialog kepercayaan institusi"],
    "D5_Generasi": ["Intervensi belia dan pekerjaan", "Program mentor komuniti belia", "Ruang dialog belia–komuniti"],
    "D6_Digital_Media": ["Literasi media dan fact-checking", "Counter-narrative harmoni", "Pemantauan isu viral setempat"],
    "D7_Institusi_Governans": ["Kaunter aduan bergerak", "Sesi penerangan perkhidmatan kerajaan", "Audit respons aduan komuniti"],
    "D8_Ketahanan_Sosial": ["Aktiviti sukarelawan komuniti", "Program patriotisme lokal", "Pengukuhan rukun tetangga"],
}

NEGERI_DAERAH = {
    "Johor":["Johor Bahru","Batu Pahat","Muar","Kluang","Segamat"],
    "Kedah":["Kota Setar","Kuala Muda","Kulim","Langkawi","Baling"],
    "Kelantan":["Kota Bharu","Pasir Mas","Tumpat","Bachok","Gua Musang"],
    "Melaka":["Melaka Tengah","Alor Gajah","Jasin"],
    "Negeri Sembilan":["Seremban","Port Dickson","Rembau","Jempol","Tampin"],
    "Pahang":["Kuantan","Temerloh","Bentong","Pekan","Raub"],
    "Pulau Pinang":["Timur Laut","Barat Daya","Seberang Perai Utara","Seberang Perai Tengah"],
    "Perak":["Kinta","Larut Matang Selama","Manjung","Hilir Perak","Kerian"],
    "Perlis":["Kangar","Arau","Padang Besar"],
    "Sabah":["Kota Kinabalu","Sandakan","Tawau","Lahad Datu","Keningau"],
    "Sarawak":["Kuching","Miri","Sibu","Bintulu","Sri Aman"],
    "Selangor":["Petaling","Klang","Gombak","Hulu Langat","Sepang"],
    "Terengganu":["Kuala Terengganu","Kemaman","Dungun","Besut"],
    "Kuala Lumpur":["Bukit Bintang","Titiwangsa","Cheras","Setiawangsa"],
    "Putrajaya":["Putrajaya"],
    "Labuan":["Labuan"]
}

AGE_GROUPS = [(15,24,"Belia"),(25,39,"Dewasa Muda"),(40,59,"Dewasa"),(60,90,"Warga Emas")]

def age_group(age):
    for lo, hi, label in AGE_GROUPS:
        if lo <= age <= hi:
            return label
    return "Lain-lain"

# =========================================================
# DATA HANDLING
# =========================================================
@st.cache_data(show_spinner=False)
def generate_survey_data(n=20000, seed=2026):
    rng = np.random.default_rng(seed)
    negeri_list = list(NEGERI_DAERAH.keys())
    weights = np.array([0.10,0.05,0.04,0.03,0.04,0.05,0.05,0.07,0.01,0.09,0.09,0.14,0.04,0.10,0.05,0.01])
    weights = weights / weights.sum()
    rows = []
    for i in range(n):
        negeri = rng.choice(negeri_list, p=weights)
        daerah = rng.choice(NEGERI_DAERAH[negeri])
        locality = f"Lokaliti {rng.integers(1, 21):02d}"
        umur = int(np.clip(rng.normal(38, 15), 15, 80))
        etnik = rng.choice(["Melayu","Cina","India","Bumiputera Sabah/Sarawak","Lain-lain"], p=[.58,.22,.07,.10,.03])
        jantina = rng.choice(["Lelaki","Perempuan"], p=[.49,.51])
        pendapatan = rng.choice(["B40","M40","T20"], p=[.55,.36,.09])
        bandar = rng.choice(["Bandar","Luar Bandar"], p=[.68,.32])
        base = rng.normal(55, 10)
        state_shock = {
            "Selangor":7,"Kuala Lumpur":8,"Johor":5,"Pulau Pinang":5,"Sabah":3,"Sarawak":2,
            "Kelantan":1,"Terengganu":0,"Pahang":0,"Perak":2,"Kedah":1,"Negeri Sembilan":1,
            "Melaka":1,"Perlis":0,"Putrajaya":-2,"Labuan":1
        }.get(negeri,0)
        econ = 62 + state_shock + (8 if pendapatan=="B40" else 2 if pendapatan=="M40" else -5) + rng.normal(0,9)
        digital = 58 + state_shock + (7 if umur<35 else 0) + rng.normal(0,10)
        generasi = 55 + (10 if umur<30 else 2 if umur<45 else -4) + rng.normal(0,10)
        sosial = 50 + state_shock*.45 + rng.normal(0,10)
        agama = 48 + state_shock*.35 + rng.normal(0,10)
        politik = 54 + state_shock*.55 + rng.normal(0,10)
        institusi = 52 + state_shock*.45 + rng.normal(0,10)
        ketahanan = 68 - state_shock*.40 + rng.normal(0,9)  # tinggi = baik
        vals = [sosial, agama, econ, politik, generasi, digital, institusi, ketahanan]
        vals = [float(np.clip(v, 0, 100)) for v in vals]
        rows.append([i+1, negeri, daerah, locality, umur, age_group(umur), etnik, jantina, pendapatan, bandar] + vals)
    df = pd.DataFrame(rows, columns=["Respondent_ID","Negeri","Daerah","Lokaliti","Umur","Kumpulan_Umur","Etnik","Jantina","Pendapatan","Bandar_LuarBandar"] + list(DIMENSIONS.keys()))
    return compute_scores(df)

def compute_scores(df):
    df = df.copy()
    for col in DIMENSIONS:
        if col not in df.columns:
            df[col] = 50
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(50).clip(0,100)
    weights = {k:v["weight"] for k,v in DIMENSIONS.items()}
    # D8 ketahanan sosial adalah protective. Untuk risk IKM, guna 100-D8.
    df["IKM_Score"] = (
        df["D1_Sosial_Identiti"]*weights["D1_Sosial_Identiti"] +
        df["D2_Agama_Budaya"]*weights["D2_Agama_Budaya"] +
        df["D3_Ekonomi"]*weights["D3_Ekonomi"] +
        df["D4_Politik_Kuasa"]*weights["D4_Politik_Kuasa"] +
        df["D5_Generasi"]*weights["D5_Generasi"] +
        df["D6_Digital_Media"]*weights["D6_Digital_Media"] +
        df["D7_Institusi_Governans"]*weights["D7_Institusi_Governans"] +
        (100-df["D8_Ketahanan_Sosial"])*weights["D8_Ketahanan_Sosial"]
    ) / sum(weights.values())
    df["IKM_Score"] = df["IKM_Score"].clip(0,100)
    df["Status_Risiko"] = pd.cut(df["IKM_Score"], bins=[-1,49.99,59.99,69.99,79.99,101], labels=["Monitor","Pain Point","Tension Point","Hotspot","Kritikal"])
    risk_dims = [d for d in DIMENSIONS if d != "D8_Ketahanan_Sosial"] + ["D8_Rendah_Ketahanan"]
    temp = df.copy()
    temp["D8_Rendah_Ketahanan"] = 100 - temp["D8_Ketahanan_Sosial"]
    df["Pain_Point_Dominan"] = temp[risk_dims].idxmax(axis=1).replace({"D8_Rendah_Ketahanan":"D8_Ketahanan_Sosial"})
    df["Pain_Point_Label"] = df["Pain_Point_Dominan"].map(lambda x: DIMENSIONS.get(x, {"label":"Ketahanan Sosial Rendah"})["label"])
    return df

@st.cache_data(show_spinner=False)
def load_uploaded(file):
    if file is None:
        return None
    name = file.name.lower()
    if name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    if "Kumpulan_Umur" not in df.columns and "Umur" in df.columns:
        df["Kumpulan_Umur"] = df["Umur"].apply(age_group)
    return compute_scores(df)

def status_color(status):
    return {"Kritikal":"#EF4444","Hotspot":"#F97316","Tension Point":"#F59E0B","Pain Point":"#EAB308","Monitor":"#22C55E"}.get(str(status),"#94A3B8")

def kpi(label, value, note=""):
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def plotly_layout(fig, height=420):
    fig.update_layout(
        template="plotly_dark", height=height,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"), title_font=dict(color="#FDE68A", size=21),
        margin=dict(l=20,r=20,t=65,b=25), legend=dict(orientation="h", y=-.18)
    )
    return fig

def aggregate_geo(df, group_cols):
    agg = df.groupby(group_cols, as_index=False).agg(
        Responden=("Respondent_ID","count"),
        IKM_Score=("IKM_Score","mean"),
        D1_Sosial_Identiti=("D1_Sosial_Identiti","mean"),
        D2_Agama_Budaya=("D2_Agama_Budaya","mean"),
        D3_Ekonomi=("D3_Ekonomi","mean"),
        D4_Politik_Kuasa=("D4_Politik_Kuasa","mean"),
        D5_Generasi=("D5_Generasi","mean"),
        D6_Digital_Media=("D6_Digital_Media","mean"),
        D7_Institusi_Governans=("D7_Institusi_Governans","mean"),
        D8_Ketahanan_Sosial=("D8_Ketahanan_Sosial","mean"),
    )
    agg["Status_Risiko"] = pd.cut(agg["IKM_Score"], bins=[-1,49.99,59.99,69.99,79.99,101], labels=["Monitor","Pain Point","Tension Point","Hotspot","Kritikal"])
    risk_cols = [c for c in DIMENSIONS if c != "D8_Ketahanan_Sosial"]
    temp = agg[risk_cols].copy()
    temp["D8_Ketahanan_Sosial"] = 100 - agg["D8_Ketahanan_Sosial"]
    agg["Pain_Point_Dominan"] = temp.idxmax(axis=1)
    agg["Pain_Point_Label"] = agg["Pain_Point_Dominan"].map(lambda x: DIMENSIONS[x]["label"])
    return agg.sort_values("IKM_Score", ascending=False)

def intervention_for(row):
    dim = row.get("Pain_Point_Dominan", "D3_Ekonomi")
    items = INTERVENTION_BANK.get(dim, INTERVENTION_BANK["D3_Ekonomi"])
    if row["IKM_Score"] >= 80:
        level = "TINDAKAN SEGERA 7-14 HARI"
    elif row["IKM_Score"] >= 70:
        level = "INTERVENSI SASARAN 30 HARI"
    elif row["IKM_Score"] >= 60:
        level = "PEMANTAUAN AKTIF 60 HARI"
    else:
        level = "MONITOR & PENCEGAHAN"
    return level, items

# =========================================================
# HERO + DATA INPUT
# =========================================================
st.markdown("""
<div class="hero">
  <h1>National IKM Intelligence Command Centre</h1>
  <p>Prototype dashboard Indeks Ketegangan Masyarakat: survey 20,000 responden, SEM constructs, skor nasional/negeri/daerah/lokaliti, hotspot, pain point dan cadangan intervensi automatik.</p>
  <span class="badge">Tanpa Sidebar</span><span class="badge">Excel 20,000 Responden</span><span class="badge">Hotspot + Intervensi</span><span class="badge">SEM-Ready</span>
</div>
""", unsafe_allow_html=True)

with st.expander("📤 Upload data survey Excel/CSV 20,000 responden atau guna data simulasi", expanded=False):
    st.markdown("**Format minimum Excel:** `Respondent_ID, Negeri, Daerah, Lokaliti, Umur, Kumpulan_Umur, Etnik, Jantina, Pendapatan, Bandar_LuarBandar, D1_Sosial_Identiti ... D8_Ketahanan_Sosial`")
    uploaded = st.file_uploader("Upload Excel/CSV survey", type=["xlsx","csv"])

uploaded_df = load_uploaded(uploaded) if 'uploaded' in locals() else None
if uploaded_df is None:
    df = generate_survey_data(20000)
    data_mode = "Data simulasi 20,000 responden"
else:
    df = uploaded_df
    data_mode = f"Data upload: {uploaded.name}"

# =========================================================
# FILTER ATAS TANPA SIDEBAR
# =========================================================
filter_cols = st.columns([1.2,1.2,1.2,1.2])
with filter_cols[0]:
    negeri_filter = st.selectbox("Negeri", ["Semua"] + sorted(df["Negeri"].dropna().unique().tolist()))
with filter_cols[1]:
    temp_df = df if negeri_filter == "Semua" else df[df["Negeri"] == negeri_filter]
    daerah_filter = st.selectbox("Daerah", ["Semua"] + sorted(temp_df["Daerah"].dropna().unique().tolist()))
with filter_cols[2]:
    umur_filter = st.selectbox("Kumpulan umur", ["Semua"] + sorted(df["Kumpulan_Umur"].dropna().unique().tolist()))
with filter_cols[3]:
    etnik_filter = st.selectbox("Etnik", ["Semua"] + sorted(df["Etnik"].dropna().unique().tolist()))

fdf = df.copy()
if negeri_filter != "Semua": fdf = fdf[fdf["Negeri"] == negeri_filter]
if daerah_filter != "Semua": fdf = fdf[fdf["Daerah"] == daerah_filter]
if umur_filter != "Semua": fdf = fdf[fdf["Kumpulan_Umur"] == umur_filter]
if etnik_filter != "Semua": fdf = fdf[fdf["Etnik"] == etnik_filter]

# =========================================================
# TABS UTAMA
# =========================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "01 Executive", "02 SEM & Teori", "03 Negeri-Daerah", "04 Hotspot", "05 Intervensi", "06 Media Monitor", "07 Data"
])

with tab1:
    st.subheader("Executive Dashboard")
    st.caption(data_mode)
    nat_score = fdf["IKM_Score"].mean()
    geo_negeri = aggregate_geo(fdf, ["Negeri"])
    geo_daerah = aggregate_geo(fdf, ["Negeri","Daerah"])
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi("IKM Score", f"{nat_score:.1f}", "0 rendah, 100 kritikal")
    with c2: kpi("Responden", f"{len(fdf):,}", "Data survey aktif")
    with c3: kpi("Negeri", f"{fdf['Negeri'].nunique()}", "Liputan geografi")
    with c4: kpi("Daerah", f"{fdf['Daerah'].nunique()}", "Unit analisis")
    with c5: kpi("Hotspot/Kritikal", f"{(geo_daerah['IKM_Score']>=70).sum()}", "Daerah perlu perhatian")

    a,b = st.columns([1.3,1])
    with a:
        top_dims = pd.DataFrame({"Dimensi":[DIMENSIONS[d]["label"] for d in DIMENSIONS], "Skor":[fdf[d].mean() if d != "D8_Ketahanan_Sosial" else 100-fdf[d].mean() for d in DIMENSIONS]})
        top_dims["Nota"] = ["Tension" if "D8" not in x else "Rendah Ketahanan" for x in top_dims["Dimensi"]]
        fig = px.bar(top_dims.sort_values("Skor", ascending=True), x="Skor", y="Dimensi", orientation="h", text="Skor", title="Pain Point Nasional Mengikut Dimensi")
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        st.plotly_chart(plotly_layout(fig, 470), use_container_width=True)
    with b:
        status_counts = geo_daerah["Status_Risiko"].value_counts().reset_index()
        status_counts.columns = ["Status", "Bilangan"]
        fig = px.pie(status_counts, values="Bilangan", names="Status", title="Taburan Status Daerah")
        st.plotly_chart(plotly_layout(fig, 470), use_container_width=True)

with tab2:
    st.subheader("SEM, Teori, Konstruk dan Skor")
    theory_map = pd.DataFrame([
        [DIMENSIONS[k]["theory"], DIMENSIONS[k]["label"], k, DIMENSIONS[k]["weight"], fdf[k].mean()] for k in DIMENSIONS
    ], columns=["Teori", "Konstruk/Dimensi", "Kod Data", "Berat SEM/Indeks", "Purata Skor"])
    st.dataframe(theory_map, use_container_width=True, hide_index=True)
    c1,c2 = st.columns([1,1])
    with c1:
        fig = px.bar(theory_map, x="Konstruk/Dimensi", y="Purata Skor", color="Teori", title="Skor Konstruk SEM")
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(plotly_layout(fig, 460), use_container_width=True)
    with c2:
        st.markdown("""
        <div class="panel">
        <h3>Logik SEM yang dicadangkan</h3>
        <p><b>Relative Deprivation</b>, <b>Conflict</b>, <b>Media Ecology</b> dan <b>Institutional Trust</b> menjadi pemacu ketegangan.</p>
        <p><b>Social Cohesion</b> bertindak sebagai faktor pelindung. Sebab itu D8 dikira sebagai <b>100 - Ketahanan Sosial</b> dalam skor risiko.</p>
        <p>Model SEM boleh menguji laluan: <br><b>Ekonomi → Konflik → Ketegangan</b><br><b>Digital → Konflik → Ketegangan</b><br><b>Ketahanan Sosial → Ketegangan</b> secara negatif.</p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"IKM_i = \sum_{j=1}^{7} w_jD_{ij} + w_8(100-D_{i8})")

with tab3:
    st.subheader("Analisis Negeri, Daerah dan Lokaliti")
    level = st.radio("Pilih tahap analisis", ["Negeri", "Daerah", "Lokaliti"], horizontal=True)
    group = ["Negeri"] if level == "Negeri" else ["Negeri","Daerah"] if level == "Daerah" else ["Negeri","Daerah","Lokaliti"]
    geo = aggregate_geo(fdf, group)
    c1,c2 = st.columns([1.1,1])
    with c1:
        fig = px.bar(geo.head(20).sort_values("IKM_Score"), x="IKM_Score", y=level, orientation="h", color="Status_Risiko", title=f"Top 20 Risiko Mengikut {level}", text="IKM_Score")
        fig.update_traces(texttemplate="%{text:.1f}")
        st.plotly_chart(plotly_layout(fig, 560), use_container_width=True)
    with c2:
        st.dataframe(geo.head(30), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("Hotspot Intelligence")
    geo = aggregate_geo(fdf, ["Negeri","Daerah"])
    hotspots = geo[geo["IKM_Score"] >= 70].copy()
    if hotspots.empty:
        st.success("Tiada daerah melebihi ambang hotspot dalam filter semasa.")
    else:
        selected = st.selectbox("Pilih hotspot/daerah", hotspots.apply(lambda r: f"{r['Daerah']} ({r['Negeri']}) - {r['IKM_Score']:.1f}", axis=1).tolist())
        idx = hotspots.apply(lambda r: f"{r['Daerah']} ({r['Negeri']}) - {r['IKM_Score']:.1f}", axis=1).tolist().index(selected)
        row = hotspots.iloc[idx]
        cls = "alert-red" if row["IKM_Score"] >= 80 else "alert-orange"
        st.markdown(f"""
        <div class="panel {cls}">
        <h3>{row['Daerah']}, {row['Negeri']} — {row['Status_Risiko']}</h3>
        <p><b>IKM Score:</b> {row['IKM_Score']:.1f} | <b>Responden:</b> {int(row['Responden']):,} | <b>Pain Point Dominan:</b> {row['Pain_Point_Label']}</p>
        </div>
        """, unsafe_allow_html=True)
        dim_values = pd.DataFrame({"Dimensi":[DIMENSIONS[d]["label"] for d in DIMENSIONS], "Skor":[row[d] if d != "D8_Ketahanan_Sosial" else 100-row[d] for d in DIMENSIONS]})
        fig = px.line_polar(dim_values, r="Skor", theta="Dimensi", line_close=True, title="Profil Risiko Hotspot")
        st.plotly_chart(plotly_layout(fig, 520), use_container_width=True)

with tab5:
    st.subheader("AI Intervention Recommendation Engine")
    geo = aggregate_geo(fdf, ["Negeri","Daerah"])
    geo = geo.sort_values("IKM_Score", ascending=False).head(15)
    for _, row in geo.iterrows():
        level, actions = intervention_for(row)
        alert = "alert-red" if row["IKM_Score"]>=80 else "alert-orange" if row["IKM_Score"]>=70 else "alert-green"
        st.markdown(f"""
        <div class="panel {alert}">
        <h3>{row['Daerah']}, {row['Negeri']} — {row['IKM_Score']:.1f}</h3>
        <p><b>Status:</b> {row['Status_Risiko']} | <b>Fokus:</b> {row['Pain_Point_Label']} | <b>Keutamaan:</b> {level}</p>
        <ol><li>{actions[0]}</li><li>{actions[1]}</li><li>{actions[2]}</li></ol>
        </div>
        """, unsafe_allow_html=True)

with tab6:
    st.subheader("Media & Public Issue Monitoring Module")
    st.info("Untuk prototype, upload Excel/CSV media. Kolum minimum: Tarikh, Sumber, Tajuk, Negeri, Daerah. Sistem akan kira keyword dan isu panas.")
    media_file = st.file_uploader("Upload media/news file", type=["xlsx","csv"], key="media")
    if media_file:
        mdf = pd.read_csv(media_file) if media_file.name.lower().endswith(".csv") else pd.read_excel(media_file)
    else:
        sample_titles = [
            "Kos sara hidup dan harga barang menjadi kebimbangan komuniti bandar",
            "Isu media sosial mencetuskan perdebatan berkaitan perpaduan",
            "Belia risau peluang pekerjaan dan kos rumah meningkat",
            "Ketegangan politik tempatan hangat dibincangkan di media",
            "Program komuniti bantu kukuhkan perpaduan masyarakat",
            "Aduan penduduk berkaitan perkhidmatan kerajaan meningkat",
        ]
        mdf = pd.DataFrame({
            "Tarikh": [datetime.today().date()-timedelta(days=int(x)) for x in np.random.default_rng(7).integers(0,30,200)],
            "Sumber": np.random.default_rng(8).choice(["Sinar Harian","Astro Awani","Bernama","Utusan","BH"], 200),
            "Tajuk": np.random.default_rng(9).choice(sample_titles, 200),
            "Negeri": np.random.default_rng(10).choice(list(NEGERI_DAERAH.keys()), 200),
            "Daerah": "-"
        })
    keywords = {
        "Ekonomi/Kos Sara Hidup":["kos", "harga", "barang", "ekonomi", "pekerjaan", "rumah"],
        "Digital/Media Sosial":["media sosial", "viral", "fitnah", "provokasi", "digital"],
        "Agama/Budaya":["agama", "budaya", "sensitif"],
        "Politik/Institusi":["politik", "kerajaan", "institusi", "aduan"],
        "Sosial/Perpaduan":["perpaduan", "komuniti", "kaum", "masyarakat"]
    }
    text = mdf["Tajuk"].astype(str).str.lower()
    issue_scores = []
    for issue, kws in keywords.items():
        count = sum(text.str.contains(k, regex=False).sum() for k in kws)
        issue_scores.append([issue, int(count), min(100, count/len(mdf)*100)])
    issue_df = pd.DataFrame(issue_scores, columns=["Isu", "Sebutan", "Hot_Issue_Score"]).sort_values("Hot_Issue_Score", ascending=False)
    c1,c2 = st.columns([1,1])
    with c1:
        fig = px.bar(issue_df.sort_values("Hot_Issue_Score"), x="Hot_Issue_Score", y="Isu", orientation="h", title="Hot Issue Score")
        st.plotly_chart(plotly_layout(fig, 420), use_container_width=True)
    with c2:
        st.dataframe(issue_df, use_container_width=True, hide_index=True)
    st.dataframe(mdf.head(50), use_container_width=True, hide_index=True)

with tab7:
    st.subheader("Data Explorer & Download")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.download_button("⬇️ Download filtered data CSV", fdf.to_csv(index=False).encode("utf-8"), "ikm_filtered_data.csv", "text/csv")
    with c2:
        st.download_button("⬇️ Download negeri summary CSV", aggregate_geo(fdf,["Negeri"]).to_csv(index=False).encode("utf-8"), "ikm_negeri_summary.csv", "text/csv")
    with c3:
        st.download_button("⬇️ Download daerah summary CSV", aggregate_geo(fdf,["Negeri","Daerah"]).to_csv(index=False).encode("utf-8"), "ikm_daerah_summary.csv", "text/csv")
    st.dataframe(fdf.head(1000), use_container_width=True, hide_index=True)

