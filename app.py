
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
import base64
import re

# =========================================================
# NATIONAL IKM INTELLIGENCE COMMAND CENTRE
# app.py
# Username: admin / viewer
# Password: jpnin2026 / ikm2026
# =========================================================

st.set_page_config(
    page_title="IKM Intelligence Command Centre",
    page_icon="🇲🇾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LOGIN CONFIG
# =========================================================
USERS = {
    "admin": {"password": "jpnin2026", "role": "Administrator"},
    "viewer": {"password": "ikm2026", "role": "Viewer"}
}

# =========================================================
# PREMIUM CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family:'Inter',sans-serif;}
header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"],#MainMenu,footer{visibility:hidden;display:none;}
.block-container{padding-top:0.2rem!important;max-width:1600px;padding-bottom:3rem;}
.stApp{
 background:
 radial-gradient(circle at 8% 2%,rgba(245,158,11,.25),transparent 27%),
 radial-gradient(circle at 92% 4%,rgba(59,130,246,.22),transparent 30%),
 radial-gradient(circle at 50% 100%,rgba(16,185,129,.16),transparent 36%),
 linear-gradient(135deg,#020617 0%,#061326 42%,#0b2545 76%,#102a43 100%);
 color:#F8FAFC;
}
.hero{
 padding:32px 40px 28px;border-radius:0 0 34px 34px;
 background:linear-gradient(135deg,rgba(255,255,255,.18),rgba(255,255,255,.06));
 border:1px solid rgba(255,255,255,.20);
 box-shadow:0 28px 80px rgba(0,0,0,.45);margin-bottom:18px;
}
.hero h1{margin:0;color:#FDE68A!important;font-size:42px;line-height:1.08;font-weight:950;letter-spacing:-1px;}
.hero p{color:#DDEBFF;font-size:15.8px;font-weight:650;max-width:1280px;margin-top:10px;line-height:1.7;}
.badge{display:inline-block;padding:8px 13px;border-radius:999px;background:rgba(15,23,42,.60);border:1px solid rgba(253,230,138,.42);color:#FDE68A;font-size:12px;font-weight:900;margin:12px 7px 0 0;}
.kpi{min-height:145px;padding:19px 20px;border-radius:25px;background:linear-gradient(145deg,rgba(255,255,255,.19),rgba(255,255,255,.055)),radial-gradient(circle at top right,rgba(253,230,138,.18),transparent 45%);border:1px solid rgba(255,255,255,.22);box-shadow:0 22px 55px rgba(0,0,0,.35);}
.kpi .label{color:#CFFAFE;font-size:11.5px;font-weight:900;text-transform:uppercase;letter-spacing:.52px;}
.kpi .value{color:#FDE68A;font-size:31px;font-weight:950;line-height:1;margin-top:9px;}
.kpi .note{color:#BBF7D0;font-size:12.2px;font-weight:750;margin-top:11px;}
.panel{padding:20px 22px;border-radius:26px;background:rgba(255,255,255,.095);border:1px solid rgba(255,255,255,.18);box-shadow:0 18px 46px rgba(0,0,0,.30);margin-bottom:16px;}
.red{border-left:7px solid #EF4444;background:linear-gradient(135deg,rgba(239,68,68,.22),rgba(255,255,255,.07));}
.orange{border-left:7px solid #F59E0B;background:linear-gradient(135deg,rgba(245,158,11,.22),rgba(255,255,255,.07));}
.green{border-left:7px solid #22C55E;background:linear-gradient(135deg,rgba(34,197,94,.18),rgba(255,255,255,.07));}
.blue{border-left:7px solid #38BDF8;background:linear-gradient(135deg,rgba(56,189,248,.18),rgba(255,255,255,.07));}
.gold{border-left:7px solid #FDE68A;background:linear-gradient(135deg,rgba(253,230,138,.18),rgba(255,255,255,.07));}
h1,h2,h3{color:#FDE68A!important;font-weight:950!important;}
.stTabs [data-baseweb="tab-list"]{gap:8px;flex-wrap:wrap;}
.stTabs [data-baseweb="tab"]{border-radius:999px;padding:10px 16px;background:rgba(255,255,255,.08);color:#E0F2FE;border:1px solid rgba(255,255,255,.14);font-weight:850;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#FDE68A,#F59E0B)!important;color:#111827!important;font-weight:950;}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{background-color:rgba(255,255,255,.94);border-radius:15px;min-height:48px;color:#111827;}
.stDataFrame{border-radius:18px;overflow:hidden;}
.small{font-size:12px;color:#CBD5E1;}
.loginbox{max-width:520px;margin:90px auto;padding:35px;border-radius:30px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);box-shadow:0 30px 90px rgba(0,0,0,.45);}
hr{border:0;border-top:1px solid rgba(255,255,255,.16);margin:18px 0;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGIN SCREEN
# =========================================================
def login_screen():
    st.markdown("""
    <div class="loginbox">
    <h1>🇲🇾 IKM Command Centre</h1>
    <p><b>National Societal Tension Intelligence Dashboard</b></p>
    <p class="small">Sila log masuk untuk mengakses sistem analitik IKM.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1.3,1])
    with c2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Log Masuk", use_container_width=True):
            if username in USERS and password == USERS[username]["password"]:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["role"] = USERS[username]["role"]
                st.rerun()
            else:
                st.error("Username atau password tidak betul.")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_screen()
    st.stop()

# =========================================================
# MASTER CONFIG
# =========================================================
ZONE_MAP = {
    "Johor":"Selatan", "Melaka":"Selatan", "Negeri Sembilan":"Selatan",
    "Selangor":"Tengah", "Kuala Lumpur":"Tengah", "Putrajaya":"Tengah",
    "Perak":"Utara", "Pulau Pinang":"Utara", "Kedah":"Utara", "Perlis":"Utara",
    "Kelantan":"Pantai Timur", "Terengganu":"Pantai Timur", "Pahang":"Pantai Timur",
    "Sabah":"Sabah", "Sarawak":"Sarawak", "Labuan":"Sabah"
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

DIMENSIONS = {
    "D1_Etnik": {"label":"D1 Indeks Ketegangan Etnik", "theory":"Social Identity Theory", "weight":0.12},
    "D2_Agama": {"label":"D2 Indeks Ketegangan Agama", "theory":"Social Identity Theory + Intergroup Threat", "weight":0.12},
    "D3_Ekonomi": {"label":"D3 Indeks Ketegangan Ekonomi", "theory":"Relative Deprivation Theory", "weight":0.16},
    "D4_Politik": {"label":"D4 Indeks Ketegangan Politik", "theory":"Conflict Theory", "weight":0.10},
    "D5_Generasi": {"label":"D5 Indeks Ketegangan Generasi", "theory":"General Strain Theory", "weight":0.08},
    "D6_Bandar_LuarBandar": {"label":"D6 Indeks Bandar-Luar Bandar", "theory":"Social Disorganization Theory", "weight":0.08},
    "D7_Institusi": {"label":"D7 Indeks Institusi & Governans", "theory":"Institutional Trust Theory", "weight":0.10},
    "D8_Ketahanan_Sosial": {"label":"D8 Indeks Ketahanan Sosial", "theory":"Social Cohesion Theory", "weight":0.12},
    "D9_Digital": {"label":"D9 Indeks Ketegangan Digital", "theory":"Media Ecology Theory", "weight":0.12},
}

ITEM_BANK = {
    "D1_Etnik": {
        "Etnik_1":"Kepercayaan terhadap kumpulan etnik lain rendah",
        "Etnik_2":"Keselesaan bergaul rentas etnik rendah",
        "Etnik_3":"Prasangka antara kumpulan etnik meningkat",
        "Etnik_4":"Rasa tidak diterima dalam komuniti etnik lain",
        "Etnik_5":"Persepsi diskriminasi etnik meningkat",
    },
    "D2_Agama": {
        "Agama_1":"Isu agama dianggap semakin sensitif",
        "Agama_2":"Pertikaian berkaitan rumah ibadat memerlukan perhatian",
        "Agama_3":"Naratif masjid/kuil/gereja mudah mencetus ketegangan",
        "Agama_4":"Tahap hormat amalan agama lain rendah",
        "Agama_5":"Fitnah atau salah faham agama meningkat",
    },
    "D3_Ekonomi": {
        "Ekonomi_1":"Tekanan kos sara hidup",
        "Ekonomi_2":"Peluang pekerjaan tidak mencukupi",
        "Ekonomi_3":"Rasa ketidaksamaan ekonomi",
        "Ekonomi_4":"Tekanan perumahan dan sewa",
        "Ekonomi_5":"Persepsi bantuan tidak adil",
    },
    "D4_Politik": {
        "Politik_1":"Polarisasi politik menjejaskan hubungan komuniti",
        "Politik_2":"Isu kepimpinan mencetus ketidakpuasan",
        "Politik_3":"Perbezaan parti menjarakkan komuniti",
        "Politik_4":"Retorik sensitif dalam politik",
        "Politik_5":"Keyakinan terhadap dasar awam rendah",
    },
    "D5_Generasi": {
        "Generasi_1":"Tekanan belia terhadap masa depan",
        "Generasi_2":"Jurang pandangan antara generasi",
        "Generasi_3":"Pekerjaan belia sebagai punca tekanan",
        "Generasi_4":"Kesukaran belia memiliki rumah",
        "Generasi_5":"Suara belia kurang didengar",
    },
    "D6_Bandar_LuarBandar": {
        "BLB_1":"Jurang akses kemudahan awam",
        "BLB_2":"Jurang pembangunan wilayah",
        "BLB_3":"Ketidakseimbangan infrastruktur",
        "BLB_4":"Akses pendidikan/kesihatan tidak seimbang",
        "BLB_5":"Peluang ekonomi tidak sekata antara kawasan",
    },
    "D7_Institusi": {
        "Institusi_1":"Kepercayaan terhadap institusi rendah",
        "Institusi_2":"Aduan komuniti tidak ditangani",
        "Institusi_3":"Persepsi perkhidmatan tidak adil",
        "Institusi_4":"Komunikasi kerajaan tidak jelas",
        "Institusi_5":"Respons agensi lambat",
    },
    "D8_Ketahanan_Sosial": {
        "Ketahanan_1":"Semangat kejiranan kuat",
        "Ketahanan_2":"Penyertaan aktiviti komuniti tinggi",
        "Ketahanan_3":"Patriotisme dan rasa kekitaan tinggi",
        "Ketahanan_4":"Pemimpin/mediator komuniti dipercayai",
        "Ketahanan_5":"Komuniti mampu meredakan konflik",
    },
    "D9_Digital": {
        "Digital_1":"Berita palsu berkaitan isu sensitif",
        "Digital_2":"Provokasi viral di media sosial",
        "Digital_3":"Komen kebencian antara kumpulan",
        "Digital_4":"Naratif influencer memanaskan isu",
        "Digital_5":"Salah faham online merebak ke komuniti",
    },
}

ITEM_TO_DIM = {item: dim for dim, items in ITEM_BANK.items() for item in items}
ITEM_LABELS = {item: label for dim, items in ITEM_BANK.items() for item, label in items.items()}

THEORY_MAP = {
    "Social Identity Theory": {
        "dims":["D1_Etnik","D2_Agama"],
        "story":"Teori ini menerangkan bagaimana identiti kumpulan seperti etnik dan agama boleh membentuk persepsi in-group dan out-group. Skor tinggi menunjukkan jarak sosial, prasangka atau sensitiviti identiti semakin ketara.",
        "intervention":"Dialog rentas identiti, engagement pemimpin komuniti, komunikasi risiko isu sensitif."
    },
    "Relative Deprivation Theory": {
        "dims":["D3_Ekonomi"],
        "story":"Teori ini menjelaskan bahawa ketegangan boleh muncul apabila masyarakat merasakan mereka kurang bernasib baik berbanding kumpulan lain dari segi pendapatan, bantuan, peluang pekerjaan dan kos hidup.",
        "intervention":"Program ekonomi komuniti, pemetaan bantuan, townhall kos sara hidup."
    },
    "Conflict Theory": {
        "dims":["D4_Politik","D7_Institusi"],
        "story":"Teori konflik melihat ketegangan sebagai hasil persaingan kuasa, sumber dan legitimasi institusi. Skor tinggi menunjukkan persepsi konflik politik atau kelemahan kepercayaan institusi.",
        "intervention":"Libat urus institusi, penerangan dasar, kaunter aduan bergerak dan pemantauan isu politik sensitif."
    },
    "General Strain Theory": {
        "dims":["D5_Generasi"],
        "story":"Teori ini melihat tekanan hidup, kegagalan mencapai aspirasi dan ketidakpuasan sebagai punca ketegangan. Dalam IKM, ia sesuai untuk memahami tekanan belia dan jurang generasi.",
        "intervention":"Program belia, mentoring komuniti, peluang pekerjaan dan dialog generasi."
    },
    "Social Disorganization Theory": {
        "dims":["D6_Bandar_LuarBandar"],
        "story":"Teori ini menerangkan bagaimana ketidakseimbangan kawasan, akses kemudahan dan struktur komuniti boleh melemahkan keteraturan sosial dan meningkatkan risiko ketegangan.",
        "intervention":"Pemetaan akses kemudahan, kolaborasi PBT/agensi, program pembangunan lokaliti."
    },
    "Social Cohesion Theory": {
        "dims":["D8_Ketahanan_Sosial"],
        "story":"Teori ini menekankan kepercayaan, rasa kekitaan, penyertaan komuniti dan modal sosial sebagai faktor pelindung. Skor rendah menunjukkan komuniti kurang daya tahan terhadap konflik.",
        "intervention":"Pengukuhan Rukun Tetangga, aktiviti sukarelawan, latihan mediator komuniti."
    },
    "Media Ecology Theory": {
        "dims":["D9_Digital"],
        "story":"Teori ini menjelaskan bagaimana media dan platform digital membentuk persepsi, mempercepat viraliti isu dan boleh meningkatkan polarisasi dalam talian.",
        "intervention":"Literasi media, counter-narrative, fact-checking dan pemantauan isu viral."
    }
}

SPECIAL_INTERVENTIONS = {
    "Agama_2": ["Aktifkan meja rundingan rumah ibadat", "Libat urus ketua agama + PBT + JPNIN daerah", "Sediakan skrip komunikasi risiko untuk elak salah faham"],
    "Agama_3": ["Rapid response naratif masjid/kuil/gereja", "Dialog tertutup pemimpin agama setempat", "Pemantauan digital kata kunci rumah ibadat"],
    "Agama_5": ["Fact-checking isu agama", "Counter-narrative hormat agama", "Hebahan rasmi bersama tokoh agama"],
    "Digital_2": ["Pasukan pantau viral 24-48 jam", "Amaran awal kepada pegawai daerah", "Kempen literasi media setempat"],
    "Digital_3": ["Moderasi komuniti digital", "Kerjasama platform/agensi berkaitan", "Latihan literasi digital komuniti"],
    "Ekonomi_1": ["Townhall kos sara hidup", "Pemetaan bantuan setempat", "Program ekonomi komuniti"],
    "Politik_1": ["Dialog sivik non-partisan", "Kod komunikasi isu sensitif", "Forum komuniti berfakta"],
    "Institusi_2": ["Kaunter aduan bergerak", "Dashboard SLA respons aduan", "Maklum balas awam berkala"],
}

DIM_INTERVENTION = {
    "D1_Etnik": ["Dialog rentas etnik", "Program kejiranan harmoni", "Mediator komuniti"],
    "D2_Agama": ["Libat urus pemimpin agama", "Protokol isu rumah ibadat", "Kempen hormat agama/budaya"],
    "D3_Ekonomi": ["Program ekonomi komuniti", "Pemetaan bantuan sosial", "Townhall kos sara hidup"],
    "D4_Politik": ["Forum literasi sivik", "Pemantauan naratif politik", "Dialog kepercayaan komuniti"],
    "D5_Generasi": ["Program belia", "Mentor komuniti belia", "Dialog belia-agensi"],
    "D6_Bandar_LuarBandar": ["Pemetaan akses kemudahan", "Kolaborasi PBT", "Program pembangunan lokaliti"],
    "D7_Institusi": ["Kaunter aduan bergerak", "Audit respons aduan", "Penerangan perkhidmatan kerajaan"],
    "D8_Ketahanan_Sosial": ["Aktiviti sukarelawan", "Pengukuhan Rukun Tetangga", "Latihan mediator komuniti"],
    "D9_Digital": ["Literasi media", "Counter-narrative", "Pemantauan isu viral"],
}

THEME_KEYWORDS = {
    "Kos Sara Hidup":["kos","harga","barang","makanan","sewa","mahal","inflasi","pendapatan"],
    "Pekerjaan & Belia":["kerja","pekerjaan","belia","gaji","graduan","masa depan"],
    "Agama & Rumah Ibadat":["agama","masjid","kuil","gereja","tokong","rumah ibadat","fitnah agama"],
    "Kaum & Identiti":["kaum","etnik","bangsa","perkauman","diskriminasi"],
    "Politik & Kepimpinan":["politik","parti","pemimpin","kerajaan","dasar"],
    "Institusi & Aduan":["agensi","aduan","perkhidmatan","lambat","tidak adil"],
    "Digital & Media Sosial":["media sosial","viral","tular","fitnah","berita palsu","komen"],
    "Keselamatan Komuniti":["jenayah","keselamatan","gangguan","ancaman"],
    "Perpaduan Komuniti":["perpaduan","komuniti","jiran","gotong","harmoni"]
}

# =========================================================
# HELPERS
# =========================================================
def age_group(age):
    try:
        age = float(age)
    except:
        age = 30
    if age < 25: return "Belia"
    if age < 40: return "Dewasa Muda"
    if age < 60: return "Dewasa"
    return "Warga Emas"

def classify_score(score):
    if score < 50: return "Monitor"
    if score < 60: return "Pain Point"
    if score < 70: return "Tension Point"
    if score < 80: return "Hotspot"
    return "Kritikal"

def risk_class_css(score):
    if score >= 80: return "red"
    if score >= 70: return "orange"
    if score >= 60: return "gold"
    return "green"

def kpi(label,value,note=""):
    st.markdown(f"""<div class='kpi'><div class='label'>{label}</div><div class='value'>{value}</div><div class='note'>{note}</div></div>""", unsafe_allow_html=True)

def plotly_layout(fig, height=430):
    fig.update_layout(
        template="plotly_dark", height=height,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"), title_font=dict(size=21,color="#FDE68A"),
        margin=dict(l=20,r=20,t=62,b=35), legend=dict(orientation="h", y=-.18)
    )
    return fig

def action_for(item, dim, score):
    if item in SPECIAL_INTERVENTIONS:
        acts = SPECIAL_INTERVENTIONS[item]
    else:
        acts = DIM_INTERVENTION.get(dim, ["Pemantauan komuniti", "Libat urus pihak berkepentingan", "Laporan tindakan daerah"])
    priority = "TINDAKAN SEGERA" if score>=80 else "INTERVENSI SASARAN" if score>=70 else "PEMANTAUAN AKTIF" if score>=60 else "MONITOR"
    return priority, acts

def normalize_colnames(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df

def make_zone(df):
    df = df.copy()
    if "Zon" not in df.columns:
        df["Zon"] = df["Negeri"].map(ZONE_MAP).fillna("Lain-lain")
    return df

def compute_scores(df):
    df = normalize_colnames(df)
    df = df.copy()

    defaults = {
        "Respondent_ID": None, "Negeri":"Tidak Dinyatakan", "Daerah":"Tidak Dinyatakan",
        "Lokaliti":"Tidak Dinyatakan", "Umur":30, "Etnik":"Tidak Dinyatakan",
        "Agama":"Tidak Dinyatakan", "Jantina":"Tidak Dinyatakan", "Pendapatan":"Tidak Dinyatakan",
        "Bandar_LuarBandar":"Tidak Dinyatakan"
    }
    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = range(1, len(df)+1) if col == "Respondent_ID" else default

    df["Kumpulan_Umur"] = pd.to_numeric(df["Umur"], errors="coerce").fillna(30).apply(age_group)
    df = make_zone(df)

    # support old columns if any
    old_map = {
        "skor_ekonomi":"D3_Ekonomi",
        "skor_politik":"D4_Politik",
        "skor_sosial":"D1_Etnik",
        "skor_digital":"D9_Digital",
        "skor_defisit_kepercayaan":"D7_Institusi",
        "skor_risiko_perpaduan":"D8_Ketahanan_Sosial",
        "skor_IKM":"IKM_Score"
    }
    for old, new in old_map.items():
        if old in df.columns and new not in df.columns:
            df[new] = pd.to_numeric(df[old], errors="coerce")

    for dim, items in ITEM_BANK.items():
        for item in items:
            if item not in df.columns:
                if dim in df.columns:
                    df[item] = df[dim]
                else:
                    df[item] = 50
            df[item] = pd.to_numeric(df[item], errors="coerce").fillna(50).clip(0,100)

        if dim not in df.columns:
            df[dim] = df[list(items)].mean(axis=1)
        else:
            df[dim] = pd.to_numeric(df[dim], errors="coerce").fillna(df[list(items)].mean(axis=1)).clip(0,100)

    weights = {d:cfg["weight"] for d,cfg in DIMENSIONS.items()}
    risk_sum = sum(weights.values())
    df["IKM_Score"] = sum((100-df[d] if d=="D8_Ketahanan_Sosial" else df[d])*w for d,w in weights.items())/risk_sum
    df["IKM_Score"] = df["IKM_Score"].clip(0,100)

    # Conflict Risk Index: high IKM + low social resilience = high risk
    df["IRK_Score"] = (0.70*df["IKM_Score"] + 0.30*(100-df["D8_Ketahanan_Sosial"])).clip(0,100)

    df["Status_Risiko"] = df["IKM_Score"].apply(classify_score)
    df["Alert_Level"] = df["IRK_Score"].apply(classify_score)

    risk_items = [i for i in ITEM_LABELS if ITEM_TO_DIM[i] != "D8_Ketahanan_Sosial"]
    temp = df[risk_items].copy()
    for item in ITEM_BANK["D8_Ketahanan_Sosial"]:
        temp[item] = 100 - df[item]
    df["Item_Kritikal"] = temp.idxmax(axis=1)
    df["Item_Kritikal_Label"] = df["Item_Kritikal"].map(ITEM_LABELS)
    df["Dimensi_Dominan"] = df["Item_Kritikal"].map(ITEM_TO_DIM)
    df["Dimensi_Dominan_Label"] = df["Dimensi_Dominan"].map(lambda x: DIMENSIONS.get(x,{}).get("label",x))
    return df

@st.cache_data(show_spinner=False)
def generate_data(n=20000, seed=2026):
    rng = np.random.default_rng(seed)
    negeri_list = list(NEGERI_DAERAH.keys())
    p = np.array([.10,.05,.04,.03,.04,.05,.05,.07,.01,.09,.09,.14,.04,.10,.05,.01])
    p = p/p.sum()
    hot_states = {"Selangor":7,"Kuala Lumpur":8,"Johor":5,"Pulau Pinang":4,"Sabah":3,"Sarawak":2,"Perak":2,"Negeri Sembilan":2}
    rows=[]
    for i in range(n):
        negeri = rng.choice(negeri_list, p=p)
        daerah = rng.choice(NEGERI_DAERAH[negeri])
        lokaliti = f"Lokaliti {rng.integers(1,31):02d}"
        umur = int(np.clip(rng.normal(38,15),15,80))
        etnik = rng.choice(["Melayu","Cina","India","Bumiputera Sabah/Sarawak","Lain-lain"], p=[.58,.22,.07,.10,.03])
        agama = rng.choice(["Islam","Buddha","Kristian","Hindu","Lain-lain"], p=[.62,.19,.10,.06,.03])
        jantina = rng.choice(["Lelaki","Perempuan"], p=[.49,.51])
        pendapatan = rng.choice(["B40","M40","T20"], p=[.55,.36,.09])
        bandar = rng.choice(["Bandar","Luar Bandar"], p=[.68,.32])
        shock = hot_states.get(negeri,0) + rng.normal(0,3)
        sensitive = 0
        if negeri in ["Selangor","Kuala Lumpur","Johor","Pulau Pinang"] and rng.random()<.42:
            sensitive += rng.normal(8,4)
        if daerah in ["Klang","Gombak","Petaling","Johor Bahru","Cheras","Bukit Bintang"]:
            sensitive += rng.normal(5,3)

        item_vals={}
        for dim, items in ITEM_BANK.items():
            for item in items:
                base = 50 + shock
                if dim == "D3_Ekonomi": base += 10 if pendapatan=="B40" else 3 if pendapatan=="M40" else -5
                if dim == "D9_Digital": base += 8 if umur<35 else 1
                if dim == "D5_Generasi": base += 9 if umur<30 else 2 if umur<45 else -4
                if dim == "D2_Agama": base += sensitive
                if item in ["Agama_2","Agama_3","Agama_5"]: base += sensitive*.65
                if dim == "D8_Ketahanan_Sosial":
                    base = 68 - shock*.45 + rng.normal(0,7)
                else:
                    base = base + rng.normal(0,9)
                item_vals[item] = float(np.clip(base,0,100))

        row = {
            "Respondent_ID":i+1,"Negeri":negeri,"Daerah":daerah,"Lokaliti":lokaliti,
            "Umur":umur,"Kumpulan_Umur":age_group(umur),"Etnik":etnik,"Agama":agama,
            "Jantina":jantina,"Pendapatan":pendapatan,"Bandar_LuarBandar":bandar
        }
        row.update(item_vals)
        rows.append(row)
    return compute_scores(pd.DataFrame(rows))

def read_excel_all(file):
    if file is None:
        return {}
    if file.name.lower().endswith(".csv"):
        return {"respondent_data": pd.read_csv(file)}
    try:
        return pd.read_excel(file, sheet_name=None)
    except Exception:
        return {"respondent_data": pd.read_excel(file)}

def first_existing_sheet(sheets, names):
    lower_map = {k.lower():k for k in sheets}
    for name in names:
        if name.lower() in lower_map:
            return sheets[lower_map[name.lower()]]
    return None

@st.cache_data(show_spinner=False)
def load_uploaded(file_bytes, file_name):
    bio = BytesIO(file_bytes)
    if file_name.lower().endswith(".csv"):
        df = pd.read_csv(bio)
        return compute_scores(df), {}
    sheets = pd.read_excel(bio, sheet_name=None)
    resp = first_existing_sheet(sheets, ["respondent_data","index_scores","survey","data","Sheet1"])
    if resp is None:
        resp = list(sheets.values())[0]
    return compute_scores(resp), sheets

def aggregate(df, group_cols):
    named = {
        "Responden":("Respondent_ID","count"),
        "IKM_Score":("IKM_Score","mean"),
        "IRK_Score":("IRK_Score","mean"),
    }
    for d in DIMENSIONS:
        named[d] = (d,"mean")
    agg = df.groupby(group_cols, as_index=False).agg(**named)
    agg["Status_Risiko"] = agg["IKM_Score"].apply(classify_score)
    agg["Alert_Level"] = agg["IRK_Score"].apply(classify_score)

    item_means = df.groupby(group_cols)[list(ITEM_LABELS)].mean().reset_index()
    merged = agg.merge(item_means, on=group_cols, how="left")
    risk_items = [i for i in ITEM_LABELS if ITEM_TO_DIM[i] != "D8_Ketahanan_Sosial"]
    temp = merged[risk_items].copy()
    for item in ITEM_BANK["D8_Ketahanan_Sosial"]:
        temp[item] = 100 - merged[item]
    merged["Item_Kritikal"] = temp.idxmax(axis=1)
    merged["Item_Kritikal_Label"] = merged["Item_Kritikal"].map(ITEM_LABELS)
    merged["Dimensi_Dominan"] = merged["Item_Kritikal"].map(ITEM_TO_DIM)
    merged["Dimensi_Dominan_Label"] = merged["Dimensi_Dominan"].map(lambda x: DIMENSIONS[x]["label"])
    return merged.sort_values("IKM_Score", ascending=False)

def item_intelligence(df):
    means = df[list(ITEM_LABELS)].mean().reset_index()
    means.columns=["Item","Skor"]
    means["Label"] = means["Item"].map(ITEM_LABELS)
    means["Dimensi"] = means["Item"].map(ITEM_TO_DIM).map(lambda x: DIMENSIONS[x]["label"])
    means["Tindakan"] = pd.cut(means["Skor"], bins=[-1,59.99,69.99,79.99,101], labels=["Monitor","Pantau Aktif","Tindakan Sasaran","Tindakan Segera"])
    return means.sort_values("Skor", ascending=False)

def get_qualitative_df(sheets):
    qdf = first_existing_sheet(sheets, ["qualitative_response","qualitative","open_ended","suara_rakyat"])
    if qdf is None:
        qdf = simulate_qualitative()
    qdf = normalize_colnames(qdf)
    # flexible column mapping
    if "jawapan" not in qdf.columns:
        possible = [c for c in qdf.columns if c.lower() in ["answer","response","komen","comment","text","ulasan"]]
        if possible:
            qdf["jawapan"] = qdf[possible[0]]
        else:
            text_cols = qdf.select_dtypes(include="object").columns.tolist()
            qdf["jawapan"] = qdf[text_cols[-1]] if text_cols else ""
    for col in ["negeri","daerah","soalan"]:
        if col not in qdf.columns:
            cap = col.capitalize()
            if cap in qdf.columns:
                qdf[col] = qdf[cap]
            else:
                qdf[col] = "Tidak Dinyatakan"
    qdf["jawapan"] = qdf["jawapan"].fillna("").astype(str)
    qdf["negeri"] = qdf["negeri"].fillna("Tidak Dinyatakan").astype(str)
    qdf["daerah"] = qdf["daerah"].fillna("Tidak Dinyatakan").astype(str)
    qdf["Zon"] = qdf["negeri"].map(ZONE_MAP).fillna("Lain-lain")
    return qdf

def simulate_qualitative(n=350, seed=7):
    rng = np.random.default_rng(seed)
    comments = [
        "Kos sara hidup semakin membebankan keluarga terutama harga makanan dan sewa rumah.",
        "Media sosial banyak menimbulkan salah faham antara kaum dan agama.",
        "Peluang pekerjaan belia masih terhad dan gaji tidak mencukupi.",
        "Isu rumah ibadat perlu ditangani dengan berhati-hati supaya tidak jadi provokasi.",
        "Aduan penduduk lambat ditangani oleh agensi berkaitan.",
        "Program komuniti dan gotong royong boleh mengeratkan hubungan masyarakat.",
        "Perbezaan politik menyebabkan jiran kurang bertegur sapa.",
        "Berita palsu berkaitan agama mudah tular dan perlu disemak segera.",
        "Kemudahan di kawasan luar bandar masih tidak seimbang.",
        "Belia mahu suara mereka didengar dalam program komuniti."
    ]
    negeri = list(NEGERI_DAERAH.keys())
    rows=[]
    for i in range(n):
        ngeri = rng.choice(negeri)
        rows.append({
            "id":i+1,
            "negeri":ngeri,
            "daerah":rng.choice(NEGERI_DAERAH[ngeri]),
            "soalan":rng.choice(["Q1 isu utama","Q2 punca","Q3 cadangan","Q4 pengalaman"]),
            "jawapan":rng.choice(comments)
        })
    return pd.DataFrame(rows)

def detect_themes(text_series):
    text = " ".join(text_series.dropna().astype(str).str.lower().tolist())
    rows=[]
    for theme, kws in THEME_KEYWORDS.items():
        score = sum(text.count(k.lower()) for k in kws)
        rows.append({"Tema":theme, "Sebutan":int(score)})
    out = pd.DataFrame(rows).sort_values("Sebutan", ascending=False)
    total = out["Sebutan"].sum()
    out["Peratus"] = np.where(total>0, out["Sebutan"]/total*100, 0)
    return out

def extract_quotes(qdf, top_themes, max_quotes=8):
    quotes=[]
    for _, r in top_themes.head(4).iterrows():
        theme = r["Tema"]
        kws = THEME_KEYWORDS[theme]
        mask = qdf["jawapan"].str.lower().apply(lambda x: any(k in x for k in kws))
        subset = qdf[mask]
        if len(subset)>0:
            row = subset.sample(1, random_state=42).iloc[0]
            quotes.append({"Tema":theme, "Negeri":row.get("negeri",""), "Daerah":row.get("daerah",""), "Petikan":row["jawapan"]})
    return pd.DataFrame(quotes).head(max_quotes)

def qualitative_story(qdf, scope_text):
    themes = detect_themes(qdf["jawapan"])
    top = themes.iloc[0]["Tema"] if len(themes) else "Tiada tema dominan"
    second = themes.iloc[1]["Tema"] if len(themes)>1 else "tema sokongan"
    third = themes.iloc[2]["Tema"] if len(themes)>2 else "tema lain"
    return f"""
    Berdasarkan analisis kualitatif bagi {scope_text}, tema paling dominan ialah **{top}**, diikuti oleh **{second}** dan **{third}**.
    Dapatan ini menunjukkan bahawa suara responden tidak hanya menggambarkan skor numerik, tetapi turut memberi konteks sebenar kepada punca ketegangan.
    Tema dominan ini wajar dijadikan asas kepada pain point, tension point dan cadangan intervensi setempat.
    """

def executive_story(df, qdf, scope_text):
    score = df["IKM_Score"].mean()
    irk = df["IRK_Score"].mean()
    status = classify_score(score)
    top_dim = pd.DataFrame({
        "dim":list(DIMENSIONS.keys()),
        "label":[DIMENSIONS[d]["label"] for d in DIMENSIONS],
        "score":[(100-df[d].mean()) if d=="D8_Ketahanan_Sosial" else df[d].mean() for d in DIMENSIONS]
    }).sort_values("score", ascending=False).iloc[0]
    item = item_intelligence(df).iloc[0]
    themes = detect_themes(qdf["jawapan"])
    top_theme = themes.iloc[0]["Tema"] if len(themes) else "tiada tema dominan"
    return f"""
    Bagi {scope_text}, skor IKM ialah **{score:.1f}** dan berada pada tahap **{status}**. 
    Skor Indeks Risiko Konflik (IRK) pula ialah **{irk:.1f}**, menunjukkan tahap amaran berdasarkan gabungan ketegangan semasa dan ketahanan sosial.
    Dimensi paling dominan ialah **{top_dim['label']}** dengan skor risiko **{top_dim['score']:.1f}**.
    Item paling kritikal ialah **{item['Label']}** dengan skor **{item['Skor']:.1f}**.
    Analisis kualitatif menunjukkan tema utama suara rakyat ialah **{top_theme}**.
    Oleh itu, tindakan susulan perlu memfokuskan kepada intervensi bersasar berdasarkan dimensi dominan, isu lapangan dan lokasi berisiko.
    """

def make_html_report(df, qdf, scope_text):
    story = executive_story(df, qdf, scope_text)
    item = item_intelligence(df).head(10)
    themes = detect_themes(qdf["jawapan"]).head(10)
    html = f"""
    <html><head><meta charset='utf-8'>
    <style>
    body{{font-family:Arial;padding:35px;color:#111827;}}
    h1{{color:#001845}} h2{{color:#0b2545}}
    .box{{padding:18px;border-radius:14px;background:#f3f4f6;margin:12px 0;}}
    table{{border-collapse:collapse;width:100%;font-size:12px;}}
    th,td{{border:1px solid #ddd;padding:8px;text-align:left;}}
    th{{background:#001845;color:white;}}
    </style></head><body>
    <h1>Laporan Analitik IKM</h1>
    <h2>{scope_text}</h2>
    <div class='box'>{story}</div>
    <h2>Top Item Kritikal</h2>
    {item.to_html(index=False)}
    <h2>Tema Kualitatif</h2>
    {themes.to_html(index=False)}
    <p><i>Dijana pada {datetime.now().strftime('%d/%m/%Y %H:%M')}</i></p>
    </body></html>
    """
    return html

def make_pdf_bytes(df, qdf, scope_text):
    # Lightweight PDF using reportlab if available
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        story.append(Paragraph("Laporan Analitik IKM", styles["Title"]))
        story.append(Paragraph(scope_text, styles["Heading2"]))
        story.append(Spacer(1,12))
        story.append(Paragraph(executive_story(df, qdf, scope_text).replace("**",""), styles["BodyText"]))
        story.append(Spacer(1,12))
        item = item_intelligence(df).head(8)[["Item","Label","Skor","Tindakan"]]
        data = [item.columns.tolist()] + item.round(2).astype(str).values.tolist()
        table = Table(data)
        table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#001845")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.5,colors.grey),("FONT",(0,0),(-1,-1),"Helvetica",7)]))
        story.append(Paragraph("Top Item Kritikal", styles["Heading2"]))
        story.append(table)
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception:
        return None

# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
<h1>🇲🇾 Sistem Indeks Ketegangan Masyarakat (IKM) Malaysia</h1>
<p><b>National IKM Intelligence Command Centre</b> ialah sistem analitik bersepadu untuk memantau skor IKM, IRK, hotspot, pain point, tension point, suara rakyat, teori, media issue dan cadangan intervensi mengikut peringkat nasional, zon, negeri, daerah dan lokaliti.</p>
<span class="badge">📊 IKM & IRK</span>
<span class="badge">🗺️ Zon / Negeri / Daerah / Lokaliti</span>
<span class="badge">🎯 Pain Point</span>
<span class="badge">🔥 Tension Point</span>
<span class="badge">🧠 Theory Intelligence</span>
<span class="badge">💬 Qualitative Intelligence</span>
<span class="badge">📄 HTML/PDF Report</span>
</div>
""", unsafe_allow_html=True)

topbar = st.columns([1,1,1,1,1])
with topbar[0]:
    st.markdown(f"**User:** {st.session_state.get('username','')}")
with topbar[1]:
    st.markdown(f"**Role:** {st.session_state.get('role','')}")
with topbar[4]:
    if st.button("Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

# =========================================================
# UPLOAD
# =========================================================
with st.expander("📤 Upload Excel/CSV atau guna data simulasi", expanded=False):
    st.write("""
    Format terbaik Excel:
    `respondent_data`, `qualitative_response`, `fgd_expert`, `media_issue_summary`, `intervention_library`, 
    `pain_point_mapping`, `tension_point_mapping`, `theory_mapping`, `state_zone_mapping`.
    Jika sheet tiada, sistem akan guna simulasi/default.
    """)
    upload = st.file_uploader("Upload fail Excel/CSV", type=["xlsx","csv"])
    st.info("Login demo: admin / jpnin2026 atau viewer / ikm2026")

if upload is not None:
    bytes_data = upload.getvalue()
    df, sheets = load_uploaded(bytes_data, upload.name)
    data_label = f"Data upload: {upload.name}"
else:
    df = generate_data(20000)
    sheets = {}
    data_label = "Data simulasi 20,000 responden"

qdf_all = get_qualitative_df(sheets)

# =========================================================
# FILTERS
# =========================================================
fc = st.columns([1,1,1,1,1,1])
with fc[0]:
    zone_filter = st.selectbox("Zon", ["Semua"]+sorted(df["Zon"].dropna().unique().tolist()))
with fc[1]:
    tmp1 = df if zone_filter=="Semua" else df[df["Zon"]==zone_filter]
    negeri_filter = st.selectbox("Negeri", ["Semua"]+sorted(tmp1["Negeri"].dropna().unique().tolist()))
with fc[2]:
    tmp2 = tmp1 if negeri_filter=="Semua" else tmp1[tmp1["Negeri"]==negeri_filter]
    daerah_filter = st.selectbox("Daerah", ["Semua"]+sorted(tmp2["Daerah"].dropna().unique().tolist()))
with fc[3]:
    tmp3 = tmp2 if daerah_filter=="Semua" else tmp2[tmp2["Daerah"]==daerah_filter]
    lokaliti_filter = st.selectbox("Lokaliti", ["Semua"]+sorted(tmp3["Lokaliti"].dropna().unique().tolist())[:200])
with fc[4]:
    umur_filter = st.selectbox("Umur", ["Semua"]+sorted(df["Kumpulan_Umur"].dropna().unique().tolist()))
with fc[5]:
    etnik_filter = st.selectbox("Etnik", ["Semua"]+sorted(df["Etnik"].dropna().unique().tolist()))

fdf = df.copy()
if zone_filter != "Semua": fdf = fdf[fdf["Zon"]==zone_filter]
if negeri_filter != "Semua": fdf = fdf[fdf["Negeri"]==negeri_filter]
if daerah_filter != "Semua": fdf = fdf[fdf["Daerah"]==daerah_filter]
if lokaliti_filter != "Semua": fdf = fdf[fdf["Lokaliti"]==lokaliti_filter]
if umur_filter != "Semua": fdf = fdf[fdf["Kumpulan_Umur"]==umur_filter]
if etnik_filter != "Semua": fdf = fdf[fdf["Etnik"]==etnik_filter]

fqdf = qdf_all.copy()
if zone_filter != "Semua": fqdf = fqdf[fqdf["Zon"]==zone_filter]
if negeri_filter != "Semua": fqdf = fqdf[fqdf["negeri"]==negeri_filter]
if daerah_filter != "Semua": fqdf = fqdf[fqdf["daerah"]==daerah_filter]

scope_parts = []
if zone_filter!="Semua": scope_parts.append(f"Zon {zone_filter}")
if negeri_filter!="Semua": scope_parts.append(f"Negeri {negeri_filter}")
if daerah_filter!="Semua": scope_parts.append(f"Daerah {daerah_filter}")
if lokaliti_filter!="Semua": scope_parts.append(f"Lokaliti {lokaliti_filter}")
scope_text = ", ".join(scope_parts) if scope_parts else "Peringkat Nasional"

if len(fdf) == 0:
    st.error("Tiada data untuk filter ini.")
    st.stop()

# =========================================================
# TABS
# =========================================================
tabs = st.tabs([
    "01 Executive KPI",
    "02 Sub-Indeks & Item",
    "03 Negeri/Zon/Daerah",
    "04 Qualitative Intelligence",
    "05 Theory Intelligence",
    "06 Pain/Tension/Hotspot",
    "07 Intervention Engine",
    "08 Media & FGD",
    "09 Report HTML/PDF",
    "10 Data"
])

with tabs[0]:
    st.subheader("Executive KPI — IKM Intelligence")
    st.caption(data_label)

    geo_daerah = aggregate(fdf, ["Negeri","Daerah"])
    geo_lokal = aggregate(fdf, ["Negeri","Daerah","Lokaliti"])
    item_top = item_intelligence(fdf).iloc[0]
    themes = detect_themes(fqdf["jawapan"])
    top_theme = themes.iloc[0]["Tema"] if len(themes) else "Tiada"

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: kpi("IKM", f"{fdf['IKM_Score'].mean():.1f}", classify_score(fdf['IKM_Score'].mean()))
    with c2: kpi("IRK", f"{fdf['IRK_Score'].mean():.1f}", "Indeks Risiko Konflik")
    with c3: kpi("Responden", f"{len(fdf):,}", "Data aktif")
    with c4: kpi("Daerah Hotspot", f"{(geo_daerah['IKM_Score']>=70).sum()}", "IKM ≥ 70")
    with c5: kpi("Lokaliti Tindakan", f"{(geo_lokal['IKM_Score']>=70).sum()}", "Hotspot lokaliti")
    with c6: kpi("Tema Utama", top_theme, "Kualitatif")

    st.markdown(f"<div class='panel {risk_class_css(fdf['IKM_Score'].mean())}'><h3>Executive AI Summary</h3><p>{executive_story(fdf, fqdf, scope_text)}</p></div>", unsafe_allow_html=True)

    a,b = st.columns([1.25,1])
    with a:
        dim_df = pd.DataFrame({
            "Dimensi":[DIMENSIONS[d]["label"] for d in DIMENSIONS],
            "Skor Risiko":[(100-fdf[d].mean()) if d=="D8_Ketahanan_Sosial" else fdf[d].mean() for d in DIMENSIONS]
        }).sort_values("Skor Risiko")
        fig = px.bar(dim_df, x="Skor Risiko", y="Dimensi", orientation="h", text="Skor Risiko", title="Skor Risiko Mengikut 9 Sub-Indeks")
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        st.plotly_chart(plotly_layout(fig, 540), use_container_width=True)
    with b:
        status = geo_daerah["Status_Risiko"].value_counts().reset_index()
        status.columns=["Status","Bilangan"]
        fig = px.pie(status, values="Bilangan", names="Status", title="Status Daerah")
        st.plotly_chart(plotly_layout(fig, 330), use_container_width=True)

        st.markdown(f"""
        <div class='panel orange'>
        <h3>Where to Take Action?</h3>
        <p><b>Item kritikal:</b> {item_top['Label']} ({item_top['Skor']:.1f})</p>
        <p><b>Daerah tertinggi:</b> {geo_daerah.iloc[0]['Daerah']}, {geo_daerah.iloc[0]['Negeri']} ({geo_daerah.iloc[0]['IKM_Score']:.1f})</p>
        <p><b>Lokaliti tertinggi:</b> {geo_lokal.iloc[0]['Lokaliti']}, {geo_lokal.iloc[0]['Daerah']} ({geo_lokal.iloc[0]['IKM_Score']:.1f})</p>
        </div>
        """, unsafe_allow_html=True)

with tabs[1]:
    st.subheader("9 Sub-Indeks, Sub-Dimensi dan Item-Level Intelligence")
    dim_select = st.selectbox("Pilih indeks", ["Semua"]+[DIMENSIONS[d]["label"] for d in DIMENSIONS])
    item_df = item_intelligence(fdf)
    if dim_select != "Semua":
        item_df = item_df[item_df["Dimensi"]==dim_select]

    c1,c2 = st.columns([1.2,1])
    with c1:
        top20 = item_df.head(20).sort_values("Skor")
        fig = px.bar(top20, x="Skor", y="Label", color="Dimensi", orientation="h", title="Top Item Kritikal", text="Skor")
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        st.plotly_chart(plotly_layout(fig, 650), use_container_width=True)
    with c2:
        st.dataframe(item_df[["Item","Label","Dimensi","Skor","Tindakan"]].head(30), use_container_width=True, hide_index=True)
        st.markdown("<div class='panel blue'><h3>Penceritaan Item</h3><p>Item-level intelligence menjawab soalan: skor tinggi ini datang daripada item apa, berada di bawah indeks mana, dan apakah tindakan awal yang sesuai.</p></div>", unsafe_allow_html=True)

with tabs[2]:
    st.subheader("Analisis Mengikut Zon, Negeri, Daerah dan Lokaliti")
    level = st.radio("Tahap analisis", ["Zon","Negeri","Daerah","Lokaliti"], horizontal=True)
    group = ["Zon"] if level=="Zon" else ["Negeri"] if level=="Negeri" else ["Negeri","Daerah"] if level=="Daerah" else ["Negeri","Daerah","Lokaliti"]
    geo = aggregate(fdf, group)

    a,b = st.columns([1.25,1])
    with a:
        ycol = group[-1]
        fig = px.bar(geo.head(30).sort_values("IKM_Score"), x="IKM_Score", y=ycol, color="Status_Risiko", orientation="h", text="IKM_Score", title=f"Top Risiko Mengikut {level}")
        fig.update_traces(texttemplate="%{text:.1f}")
        st.plotly_chart(plotly_layout(fig, 650), use_container_width=True)
    with b:
        selected = st.selectbox("Pilih lokasi untuk profil", geo.apply(lambda r: " | ".join([str(r[g]) for g in group])+f" — {r['IKM_Score']:.1f}", axis=1).tolist())
        ix = geo.apply(lambda r: " | ".join([str(r[g]) for g in group])+f" — {r['IKM_Score']:.1f}", axis=1).tolist().index(selected)
        row = geo.iloc[ix]
        dim_values = pd.DataFrame({"Dimensi":[DIMENSIONS[d]["label"] for d in DIMENSIONS], "Skor":[(100-row[d]) if d=="D8_Ketahanan_Sosial" else row[d] for d in DIMENSIONS]})
        fig = px.line_polar(dim_values, r="Skor", theta="Dimensi", line_close=True, title="Profil Risiko Lokasi")
        st.plotly_chart(plotly_layout(fig, 440), use_container_width=True)
        priority, acts = action_for(row["Item_Kritikal"], row["Dimensi_Dominan"], row["IKM_Score"])
        st.markdown(f"""
        <div class='panel {risk_class_css(row["IKM_Score"])}'>
        <h3>{priority}</h3>
        <p><b>Status:</b> {row['Status_Risiko']}</p>
        <p><b>Item:</b> {row['Item_Kritikal_Label']}</p>
        <ol><li>{acts[0]}</li><li>{acts[1]}</li><li>{acts[2]}</li></ol>
        </div>
        """, unsafe_allow_html=True)
    st.dataframe(geo.head(80)[group+["Responden","IKM_Score","IRK_Score","Status_Risiko","Alert_Level","Item_Kritikal_Label","Dimensi_Dominan_Label"]], use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("Qualitative Intelligence — Suara Rakyat")
    st.markdown(f"<div class='panel blue'><h3>Rumusan Kualitatif</h3><p>{qualitative_story(fqdf, scope_text)}</p></div>", unsafe_allow_html=True)

    themes = detect_themes(fqdf["jawapan"])
    quotes = extract_quotes(fqdf, themes)

    c1,c2 = st.columns([1.1,1])
    with c1:
        fig = px.bar(themes.sort_values("Sebutan"), x="Sebutan", y="Tema", orientation="h", text="Sebutan", title="Tema Utama Jawapan Terbuka")
        st.plotly_chart(plotly_layout(fig, 520), use_container_width=True)
    with c2:
        st.markdown("### Petikan Responden")
        if len(quotes):
            for _, r in quotes.iterrows():
                st.markdown(f"""
                <div class='panel gold'>
                <b>{r['Tema']}</b><br>
                <span class='small'>{r['Negeri']} | {r['Daerah']}</span>
                <p>"{r['Petikan']}"</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Tiada petikan ditemui.")

    st.markdown("### Data Kualitatif")
    st.dataframe(fqdf.head(300), use_container_width=True, hide_index=True)

with tabs[4]:
    st.subheader("Theory Intelligence — Teori → Result → Huraian → Intervensi")
    rows=[]
    for theory, info in THEORY_MAP.items():
        scores=[]
        for d in info["dims"]:
            scores.append((100-fdf[d].mean()) if d=="D8_Ketahanan_Sosial" else fdf[d].mean())
        rows.append({"Teori":theory, "Skor":np.mean(scores), "Konstruk":", ".join([DIMENSIONS[d]["label"] for d in info["dims"]])})
    tdf = pd.DataFrame(rows).sort_values("Skor", ascending=False)

    c1,c2 = st.columns([1.1,1])
    with c1:
        fig = px.bar(tdf.sort_values("Skor"), x="Skor", y="Teori", orientation="h", text="Skor", title="Skor Risiko Mengikut Teori")
        fig.update_traces(texttemplate="%{text:.1f}")
        st.plotly_chart(plotly_layout(fig, 520), use_container_width=True)
    with c2:
        st.dataframe(tdf, use_container_width=True, hide_index=True)

    for _, r in tdf.iterrows():
        info = THEORY_MAP[r["Teori"]]
        st.markdown(f"""
        <div class='panel {risk_class_css(r["Skor"])}'>
        <h3>{r["Teori"]} — {r["Skor"]:.1f}</h3>
        <p><b>Konstruk berkaitan:</b> {r["Konstruk"]}</p>
        <p><b>Huraian:</b> {info["story"]}</p>
        <p><b>Cadangan tindakan:</b> {info["intervention"]}</p>
        </div>
        """, unsafe_allow_html=True)

with tabs[5]:
    st.subheader("Pain Point, Tension Point dan Hotspot Intelligence")
    geo = aggregate(fdf, ["Negeri","Daerah","Lokaliti"])
    geo["Kategori_Operasi"] = np.select(
        [
            geo["IKM_Score"]>=80,
            geo["IKM_Score"]>=70,
            geo["IKM_Score"]>=60,
            geo["IKM_Score"]>=50
        ],
        ["Critical Hotspot","Hotspot","Tension Point","Pain Point"],
        default="Monitor"
    )

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Pain Point", f"{(geo['Kategori_Operasi']=='Pain Point').sum()}", "50 ≤ IKM < 60")
    with c2: kpi("Tension Point", f"{(geo['Kategori_Operasi']=='Tension Point').sum()}", "60 ≤ IKM < 70")
    with c3: kpi("Hotspot", f"{(geo['Kategori_Operasi']=='Hotspot').sum()}", "70 ≤ IKM < 80")
    with c4: kpi("Critical", f"{(geo['Kategori_Operasi']=='Critical Hotspot').sum()}", "IKM ≥ 80")

    fig = px.scatter(
        geo.head(300),
        x="IKM_Score", y="IRK_Score",
        size="Responden", color="Kategori_Operasi",
        hover_data=["Negeri","Daerah","Lokaliti","Item_Kritikal_Label"],
        title="Matriks IKM vs IRK"
    )
    st.plotly_chart(plotly_layout(fig, 560), use_container_width=True)

    st.dataframe(geo.head(100)[["Negeri","Daerah","Lokaliti","Responden","IKM_Score","IRK_Score","Kategori_Operasi","Item_Kritikal_Label","Dimensi_Dominan_Label"]], use_container_width=True, hide_index=True)

with tabs[6]:
    st.subheader("Intervention Recommendation Engine")
    geo = aggregate(fdf, ["Negeri","Daerah","Lokaliti"]).head(30)
    for _, row in geo.iterrows():
        priority, acts = action_for(row["Item_Kritikal"], row["Dimensi_Dominan"], row["IKM_Score"])
        st.markdown(f"""
        <div class='panel {risk_class_css(row["IKM_Score"])}'>
        <h3>{row['Lokaliti']}, {row['Daerah']}, {row['Negeri']} — IKM {row['IKM_Score']:.1f} | IRK {row['IRK_Score']:.1f}</h3>
        <p><b>Status:</b> {row['Status_Risiko']} | <b>Alert:</b> {row['Alert_Level']} | <b>Item kritikal:</b> {row['Item_Kritikal_Label']} | <b>Priority:</b> {priority}</p>
        <ol><li>{acts[0]}</li><li>{acts[1]}</li><li>{acts[2]}</li></ol>
        </div>
        """, unsafe_allow_html=True)

with tabs[7]:
    st.subheader("Media Monitoring & FGD Expert Validation")

    mdf = first_existing_sheet(sheets, ["media_issue_summary","media","news"])
    if mdf is None:
        mdf = pd.DataFrame({
            "Tarikh":[datetime.today().date()]*8,
            "Sumber":["Sinar","Awani","Bernama","BH","Utusan","Portal","X","Facebook"],
            "Isu":["Kos sara hidup","Rumah ibadat","Berita palsu","Politik","Aduan agensi","Belia","Kaum","Perpaduan"],
            "Ringkasan":[
                "Harga barang menjadi kebimbangan utama.",
                "Isu rumah ibadat perlu dipantau.",
                "Berita palsu berkaitan agama tular.",
                "Polarisasi politik meningkat.",
                "Aduan perkhidmatan lambat.",
                "Belia bimbang pekerjaan.",
                "Naratif kaum sensitif meningkat.",
                "Program komuniti membantu perpaduan."
            ],
            "Negeri":["Selangor","Selangor","Johor","KL","Sabah","Perak","Penang","Sarawak"]
        })
    fgd = first_existing_sheet(sheets, ["fgd_expert","expert_validation","fgd"])
    if fgd is None:
        fgd = pd.DataFrame({
            "Pakar":["Pakar Sosial","Pakar Statistik","Pakar Dasar","Pakar Komuniti"],
            "Tema":["Validasi Indeks","SEM","Intervensi","Lapangan"],
            "Dapatan":["Indeks sesuai tetapi perlu item-level.","EFA/CFA/PLS-SEM dikekalkan.","Intervensi perlu ikut dimensi dominan.","Data kualitatif penting untuk konteks."]
        })

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("### Media Issue Summary")
        st.dataframe(mdf.head(100), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("### FGD Expert Validation")
        st.dataframe(fgd.head(100), use_container_width=True, hide_index=True)

with tabs[8]:
    st.subheader("Report Generator — HTML dan PDF")

    html = make_html_report(fdf, fqdf, scope_text)
    st.download_button(
        "⬇️ Download HTML Report",
        html.encode("utf-8"),
        file_name=f"IKM_Report_{scope_text.replace(' ','_').replace(',','')}.html",
        mime="text/html",
        use_container_width=True
    )

    pdf_bytes = make_pdf_bytes(fdf, fqdf, scope_text)
    if pdf_bytes:
        st.download_button(
            "⬇️ Download PDF Report",
            pdf_bytes,
            file_name=f"IKM_Report_{scope_text.replace(' ','_').replace(',','')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.warning("PDF memerlukan package reportlab. Tambah `reportlab` dalam requirements.txt.")

    st.markdown("### Preview Executive Report")
    st.components.v1.html(html, height=720, scrolling=True)

with tabs[9]:
    st.subheader("Data Explorer & Download")

    c1,c2,c3 = st.columns(3)
    with c1:
        st.download_button("⬇️ Filtered Respondent CSV", fdf.to_csv(index=False).encode("utf-8"), "ikm_filtered_respondent_data.csv", "text/csv", use_container_width=True)
    with c2:
        st.download_button("⬇️ Daerah Summary CSV", aggregate(fdf,["Negeri","Daerah"]).to_csv(index=False).encode("utf-8"), "ikm_daerah_summary.csv", "text/csv", use_container_width=True)
    with c3:
        st.download_button("⬇️ Item Intelligence CSV", item_intelligence(fdf).to_csv(index=False).encode("utf-8"), "ikm_item_intelligence.csv", "text/csv", use_container_width=True)

    st.markdown("### Format Kolum Disyorkan")
    format_df = pd.DataFrame({
        "Sheet":["respondent_data"]*7 + ["respondent_data"]*len(ITEM_LABELS) + ["qualitative_response"]*5,
        "Kolum":["Respondent_ID","Negeri","Daerah","Lokaliti","Umur","Etnik","Agama"] + list(ITEM_LABELS.keys()) + ["id","negeri","daerah","soalan","jawapan"],
        "Maksud":["ID responden","Negeri","Daerah","Lokaliti","Umur","Etnik","Agama"] + list(ITEM_LABELS.values()) + ["ID","Negeri","Daerah","Kod/teks soalan","Jawapan terbuka responden"]
    })
    st.dataframe(format_df, use_container_width=True, hide_index=True)

    st.markdown("### Data Semasa")
    st.dataframe(fdf.head(1000), use_container_width=True, hide_index=True)
