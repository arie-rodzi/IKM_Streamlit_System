import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =========================================================
# NATIONAL IKM INTELLIGENCE COMMAND CENTRE v2
# Fokus: item-level detection, isu agama/rumah ibadat, hotspot, intervention
# =========================================================

st.set_page_config(
    page_title="IKM Command Centre v2",
    page_icon="🇲🇾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family:'Inter',sans-serif;}
header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"],#MainMenu,footer{visibility:hidden;display:none;}
.block-container{padding-top:0.2rem!important;max-width:1580px;padding-bottom:3rem;}
.stApp{
 background:
 radial-gradient(circle at 10% 5%,rgba(245,158,11,.22),transparent 27%),
 radial-gradient(circle at 90% 5%,rgba(59,130,246,.20),transparent 30%),
 radial-gradient(circle at 50% 100%,rgba(16,185,129,.16),transparent 36%),
 linear-gradient(135deg,#020617 0%,#061326 42%,#0b2545 76%,#102a43 100%);
 color:#F8FAFC;
}
.hero{padding:30px 38px 26px;border-radius:0 0 34px 34px;background:linear-gradient(135deg,rgba(255,255,255,.18),rgba(255,255,255,.06));border:1px solid rgba(255,255,255,.20);box-shadow:0 28px 80px rgba(0,0,0,.45);margin-bottom:18px;}
.hero h1{margin:0;color:#FDE68A!important;font-size:39px;line-height:1.08;font-weight:950;letter-spacing:-1px;}
.hero p{color:#DDEBFF;font-size:15.5px;font-weight:650;max-width:1200px;margin-top:10px;}
.badge{display:inline-block;padding:8px 13px;border-radius:999px;background:rgba(15,23,42,.60);border:1px solid rgba(253,230,138,.42);color:#FDE68A;font-size:12px;font-weight:900;margin:12px 7px 0 0;}
.kpi{min-height:145px;padding:19px 20px;border-radius:25px;background:linear-gradient(145deg,rgba(255,255,255,.19),rgba(255,255,255,.055)),radial-gradient(circle at top right,rgba(253,230,138,.18),transparent 45%);border:1px solid rgba(255,255,255,.22);box-shadow:0 22px 55px rgba(0,0,0,.35);}
.kpi .label{color:#CFFAFE;font-size:11.5px;font-weight:900;text-transform:uppercase;letter-spacing:.52px;}
.kpi .value{color:#FDE68A;font-size:32px;font-weight:950;line-height:1;margin-top:9px;}
.kpi .note{color:#BBF7D0;font-size:12.2px;font-weight:750;margin-top:11px;}
.panel{padding:20px 22px;border-radius:26px;background:rgba(255,255,255,.095);border:1px solid rgba(255,255,255,.18);box-shadow:0 18px 46px rgba(0,0,0,.30);margin-bottom:16px;}
.red{border-left:7px solid #EF4444;background:linear-gradient(135deg,rgba(239,68,68,.22),rgba(255,255,255,.07));}
.orange{border-left:7px solid #F59E0B;background:linear-gradient(135deg,rgba(245,158,11,.22),rgba(255,255,255,.07));}
.green{border-left:7px solid #22C55E;background:linear-gradient(135deg,rgba(34,197,94,.18),rgba(255,255,255,.07));}
.blue{border-left:7px solid #38BDF8;background:linear-gradient(135deg,rgba(56,189,248,.18),rgba(255,255,255,.07));}
h1,h2,h3{color:#FDE68A!important;font-weight:950!important;}
.stTabs [data-baseweb="tab-list"]{gap:8px;flex-wrap:wrap;}
.stTabs [data-baseweb="tab"]{border-radius:999px;padding:10px 16px;background:rgba(255,255,255,.08);color:#E0F2FE;border:1px solid rgba(255,255,255,.14);font-weight:850;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#FDE68A,#F59E0B)!important;color:#111827!important;font-weight:950;}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{background-color:rgba(255,255,255,.94);border-radius:15px;min-height:48px;}
.stDataFrame{border-radius:18px;overflow:hidden;}
.small{font-size:12px;color:#CBD5E1;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MASTER CONFIG
# =========================================================
DIMENSIONS = {
    "D1_Sosial_Identiti": {"label":"D1 Sosial & Identiti", "theory":"Social Identity Theory", "weight":0.13},
    "D2_Agama_Budaya": {"label":"D2 Agama, Budaya & Rumah Ibadat", "theory":"Social Identity Theory + Intergroup Threat", "weight":0.14},
    "D3_Ekonomi": {"label":"D3 Ekonomi & Sara Hidup", "theory":"Relative Deprivation Theory", "weight":0.16},
    "D4_Politik_Kuasa": {"label":"D4 Politik, Kuasa & Kepimpinan", "theory":"Conflict Theory", "weight":0.11},
    "D5_Generasi": {"label":"D5 Generasi & Belia", "theory":"General Strain Theory", "weight":0.09},
    "D6_Digital_Media": {"label":"D6 Digital, Viral & Provokasi", "theory":"Media Ecology Theory", "weight":0.15},
    "D7_Institusi_Governans": {"label":"D7 Institusi & Governans", "theory":"Institutional Trust Theory", "weight":0.10},
    "D8_Ketahanan_Sosial": {"label":"D8 Ketahanan Sosial", "theory":"Social Cohesion Theory", "weight":0.12},
}

ITEM_BANK = {
    "D1_Sosial_Identiti": {
        "S1_Percaya_Kaum_Lain":"Kepercayaan terhadap kaum/etnik lain rendah",
        "S2_Selesa_Bergaul":"Keselesaan bergaul rentas kumpulan rendah",
        "S3_Prasaangka_Kumpulan":"Prasangka terhadap kumpulan lain meningkat",
        "S4_Rasa_Tidak_Diterima":"Rasa tidak diterima dalam komuniti",
        "S5_Jurang_Bandar_LuarBandar":"Jurang bandar-luar bandar menimbulkan ketegangan",
    },
    "D2_Agama_Budaya": {
        "A1_Sensitiviti_Agama":"Isu agama dianggap semakin sensitif",
        "A2_Rumah_Ibadat":"Pertikaian berkaitan rumah ibadat perlu perhatian",
        "A3_Masjid_Kuil_Gereja":"Naratif masjid/kuil/gereja mudah mencetus ketegangan",
        "A4_Hormat_Amalan_Agama":"Tahap hormat amalan agama lain rendah",
        "A5_Fitnah_Agama":"Fitnah atau salah faham agama meningkat",
    },
    "D3_Ekonomi": {
        "E1_Kos_Sara_Hidup":"Tekanan kos sara hidup",
        "E2_Peluang_Pekerjaan":"Peluang pekerjaan tidak mencukupi",
        "E3_Ketidaksamaan_Ekonomi":"Rasa ketidaksamaan ekonomi",
        "E4_Perumahan":"Tekanan perumahan/sewa",
        "E5_Bantuan_Tidak_Adil":"Persepsi bantuan tidak adil",
    },
    "D4_Politik_Kuasa": {
        "P1_Polarisasi_Politik":"Polarisasi politik menjejaskan hubungan komuniti",
        "P2_Isu_Kepimpinan":"Isu kepimpinan mencetus ketidakpuasan",
        "P3_Partizan_Komuniti":"Perbezaan parti menjarakkan komuniti",
        "P4_Retoric_Sensitif":"Retorik sensitif dalam politik",
        "P5_Keyakinan_Dasar":"Keyakinan terhadap dasar awam rendah",
    },
    "D5_Generasi": {
        "G1_Tekanan_Belia":"Tekanan belia terhadap masa depan",
        "G2_Jurang_Generasi":"Jurang pandangan antara generasi",
        "G3_Pekerjaan_Belia":"Pekerjaan belia sebagai punca tekanan",
        "G4_Rumah_Belia":"Kesukaran memiliki rumah",
        "G5_Suara_Belia":"Suara belia kurang didengar",
    },
    "D6_Digital_Media": {
        "M1_Berita_Palsu":"Berita palsu berkaitan isu sensitif",
        "M2_Provokasi_Viral":"Provokasi viral di media sosial",
        "M3_Komen_Kebencian":"Komen kebencian antara kumpulan",
        "M4_Influencer_Naratif":"Naratif influencer memanaskan isu",
        "M5_Salah_Faham_Online":"Salah faham online merebak ke komuniti",
    },
    "D7_Institusi_Governans": {
        "I1_Percaya_Institusi":"Kepercayaan terhadap institusi rendah",
        "I2_Aduan_Tidak_Ditangani":"Aduan komuniti tidak ditangani",
        "I3_Keadilan_Perkhidmatan":"Persepsi perkhidmatan tidak adil",
        "I4_Komunikasi_Kerajaan":"Komunikasi kerajaan tidak jelas",
        "I5_Respons_Agensi":"Respons agensi lambat",
    },
    "D8_Ketahanan_Sosial": {
        "K1_Semangat_Kejiranan":"Semangat kejiranan kuat",
        "K2_Penyertaan_Komuniti":"Penyertaan aktiviti komuniti tinggi",
        "K3_Patriotisme":"Patriotisme dan rasa kekitaan tinggi",
        "K4_Mediator_Komuniti":"Pemimpin/mediator komuniti dipercayai",
        "K5_Daya_Tahan_Komuniti":"Komuniti mampu meredakan konflik",
    },
}
ITEM_TO_DIM = {item: dim for dim, items in ITEM_BANK.items() for item in items}
ITEM_LABELS = {item: label for dim, items in ITEM_BANK.items() for item, label in items.items()}

SPECIAL_INTERVENTIONS = {
    "A2_Rumah_Ibadat": ["Aktifkan meja rundingan rumah ibadat", "Libat urus ketua agama + PBT + JPNIN daerah", "Sediakan skrip komunikasi risiko untuk elak salah faham"],
    "A3_Masjid_Kuil_Gereja": ["Rapid response naratif masjid/kuil/gereja", "Dialog tertutup pemimpin agama setempat", "Pemantauan digital kata kunci rumah ibadat"],
    "A5_Fitnah_Agama": ["Fact-checking isu agama", "Counter-narrative hormat agama", "Hebahan rasmi bersama tokoh agama"],
    "M2_Provokasi_Viral": ["Pasukan pantau viral 24-48 jam", "Amaran awal kepada pegawai daerah", "Kempen literasi media setempat"],
    "M3_Komen_Kebencian": ["Moderasi komuniti digital", "Kerjasama platform/agensi berkaitan", "Latihan literasi digital komuniti"],
    "E1_Kos_Sara_Hidup": ["Townhall kos sara hidup", "Pemetaan bantuan setempat", "Program ekonomi komuniti"],
    "P1_Polarisasi_Politik": ["Dialog sivik non-partisan", "Kod komunikasi isu sensitif", "Forum komuniti berfakta"],
    "I2_Aduan_Tidak_Ditangani": ["Kaunter aduan bergerak", "Dashboard SLA respons aduan", "Maklum balas awam berkala"],
}

DIM_INTERVENTION = {
    "D1_Sosial_Identiti": ["Dialog rentas etnik", "Program kejiranan harmoni", "Mediator komuniti"],
    "D2_Agama_Budaya": ["Libat urus pemimpin agama", "Protokol isu rumah ibadat", "Kempen hormat agama/budaya"],
    "D3_Ekonomi": ["Program ekonomi komuniti", "Pemetaan bantuan sosial", "Townhall kos sara hidup"],
    "D4_Politik_Kuasa": ["Forum literasi sivik", "Pemantauan naratif politik", "Dialog kepercayaan komuniti"],
    "D5_Generasi": ["Program belia", "Mentor komuniti belia", "Dialog belia-agency"],
    "D6_Digital_Media": ["Literasi media", "Counter-narrative", "Pemantauan isu viral"],
    "D7_Institusi_Governans": ["Kaunter aduan bergerak", "Audit respons aduan", "Penerangan perkhidmatan kerajaan"],
    "D8_Ketahanan_Sosial": ["Aktiviti sukarelawan", "Pengukuhan rukun tetangga", "Latihan mediator komuniti"],
}

NEGERI_DAERAH = {
    "Johor":["Johor Bahru","Batu Pahat","Muar","Kluang","Segamat"], "Kedah":["Kota Setar","Kuala Muda","Kulim","Langkawi","Baling"],
    "Kelantan":["Kota Bharu","Pasir Mas","Tumpat","Bachok","Gua Musang"], "Melaka":["Melaka Tengah","Alor Gajah","Jasin"],
    "Negeri Sembilan":["Seremban","Port Dickson","Rembau","Jempol","Tampin"], "Pahang":["Kuantan","Temerloh","Bentong","Pekan","Raub"],
    "Pulau Pinang":["Timur Laut","Barat Daya","Seberang Perai Utara","Seberang Perai Tengah"], "Perak":["Kinta","Larut Matang Selama","Manjung","Hilir Perak","Kerian"],
    "Perlis":["Kangar","Arau","Padang Besar"], "Sabah":["Kota Kinabalu","Sandakan","Tawau","Lahad Datu","Keningau"],
    "Sarawak":["Kuching","Miri","Sibu","Bintulu","Sri Aman"], "Selangor":["Petaling","Klang","Gombak","Hulu Langat","Sepang"],
    "Terengganu":["Kuala Terengganu","Kemaman","Dungun","Besut"], "Kuala Lumpur":["Bukit Bintang","Titiwangsa","Cheras","Setiawangsa"],
    "Putrajaya":["Putrajaya"], "Labuan":["Labuan"]
}

def age_group(age):
    if age < 25: return "Belia"
    if age < 40: return "Dewasa Muda"
    if age < 60: return "Dewasa"
    return "Warga Emas"

# =========================================================
# DATA GENERATION + SCORING
# =========================================================
@st.cache_data(show_spinner=False)
def generate_data(n=20000, seed=2026):
    rng = np.random.default_rng(seed)
    negeri_list = list(NEGERI_DAERAH.keys())
    p = np.array([.10,.05,.04,.03,.04,.05,.05,.07,.01,.09,.09,.14,.04,.10,.05,.01]); p=p/p.sum()
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
        # event shock: isu rumah ibadat/digital lebih tinggi di beberapa kawasan simulasi
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
                if dim == "D6_Digital_Media": base += 8 if umur<35 else 1
                if dim == "D5_Generasi": base += 9 if umur<30 else 2 if umur<45 else -4
                if dim == "D2_Agama_Budaya": base += sensitive
                if item in ["A2_Rumah_Ibadat","A3_Masjid_Kuil_Gereja","A5_Fitnah_Agama"]: base += sensitive*.65
                if dim == "D8_Ketahanan_Sosial": base = 68 - shock*.45 + rng.normal(0,7) # protective high = good
                else: base = base + rng.normal(0,9)
                item_vals[item] = float(np.clip(base,0,100))
        row = {"Respondent_ID":i+1,"Negeri":negeri,"Daerah":daerah,"Lokaliti":lokaliti,"Umur":umur,"Kumpulan_Umur":age_group(umur),"Etnik":etnik,"Agama":agama,"Jantina":jantina,"Pendapatan":pendapatan,"Bandar_LuarBandar":bandar}
        row.update(item_vals)
        rows.append(row)
    return compute_scores(pd.DataFrame(rows))

def compute_scores(df):
    df=df.copy()
    # ensure demographic columns
    for col, default in [("Respondent_ID", None),("Negeri","Tidak Dinyatakan"),("Daerah","Tidak Dinyatakan"),("Lokaliti","Tidak Dinyatakan"),("Umur",30),("Etnik","Tidak Dinyatakan"),("Agama","Tidak Dinyatakan"),("Jantina","Tidak Dinyatakan"),("Pendapatan","Tidak Dinyatakan"),("Bandar_LuarBandar","Tidak Dinyatakan")]:
        if col not in df.columns:
            df[col] = range(1,len(df)+1) if col=="Respondent_ID" else default
    if "Kumpulan_Umur" not in df.columns:
        df["Kumpulan_Umur"] = pd.to_numeric(df["Umur"], errors="coerce").fillna(30).apply(age_group)
    # If user upload dimension-only data, generate blank item scores from dimension cols
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
    df["Status_Risiko"] = pd.cut(df["IKM_Score"], bins=[-1,49.99,59.99,69.99,79.99,101], labels=["Monitor","Pain Point","Tension Point","Hotspot","Kritikal"])
    # top item and dimension for each respondent
    risk_items = [i for i in ITEM_LABELS if ITEM_TO_DIM[i] != "D8_Ketahanan_Sosial"]
    protective_risk = 100 - df[list(ITEM_BANK["D8_Ketahanan_Sosial"].keys())]
    temp = pd.concat([df[risk_items], protective_risk.rename(columns={c:c+"_Rendah" for c in protective_risk.columns})], axis=1)
    df["Item_Kritikal"] = temp.idxmax(axis=1).str.replace("_Rendah", "", regex=False)
    df["Item_Kritikal_Label"] = df["Item_Kritikal"].map(ITEM_LABELS)
    df["Dimensi_Dominan"] = df["Item_Kritikal"].map(ITEM_TO_DIM)
    df["Dimensi_Dominan_Label"] = df["Dimensi_Dominan"].map(lambda x: DIMENSIONS[x]["label"])
    return df

@st.cache_data(show_spinner=False)
def load_file(file):
    if file is None: return None
    if file.name.lower().endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    return compute_scores(df)

def kpi(label,value,note=""):
    st.markdown(f"""<div class='kpi'><div class='label'>{label}</div><div class='value'>{value}</div><div class='note'>{note}</div></div>""", unsafe_allow_html=True)

def plotly_layout(fig, height=430):
    fig.update_layout(template="plotly_dark", height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"), title_font=dict(size=21,color="#FDE68A"), margin=dict(l=20,r=20,t=62,b=30), legend=dict(orientation="h", y=-.20))
    return fig

def aggregate(df, group_cols):
    agg = df.groupby(group_cols, as_index=False).agg(Responden=("Respondent_ID","count"), IKM_Score=("IKM_Score","mean"), **{d:(d,"mean") for d in DIMENSIONS})
    agg["Status_Risiko"] = pd.cut(agg["IKM_Score"], bins=[-1,49.99,59.99,69.99,79.99,101], labels=["Monitor","Pain Point","Tension Point","Hotspot","Kritikal"])
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

def item_intelligence(df, group_cols=None):
    if group_cols is None:
        means = df[list(ITEM_LABELS)].mean().reset_index()
        means.columns=["Item","Skor"]
    else:
        means = df.groupby(group_cols)[list(ITEM_LABELS)].mean().reset_index().melt(id_vars=group_cols, var_name="Item", value_name="Skor")
    means["Label"] = means["Item"].map(ITEM_LABELS)
    means["Dimensi"] = means["Item"].map(ITEM_TO_DIM).map(lambda x: DIMENSIONS[x]["label"])
    means["Tindakan"] = pd.cut(means["Skor"], bins=[-1,59.99,69.99,79.99,101], labels=["Monitor","Pantau Aktif","Tindakan Sasaran","Tindakan Segera"])
    return means.sort_values("Skor", ascending=False)

def action_for(item, dim, score):
    if item in SPECIAL_INTERVENTIONS:
        acts = SPECIAL_INTERVENTIONS[item]
    else:
        acts = DIM_INTERVENTION.get(dim, ["Pemantauan komuniti", "Libat urus pihak berkepentingan", "Laporan tindakan daerah"])
    priority = "TINDAKAN SEGERA" if score>=80 else "INTERVENSI SASARAN" if score>=70 else "PEMANTAUAN AKTIF" if score>=60 else "MONITOR"
    return priority, acts

# =========================================================
# HERO + UPLOAD + FILTER
# =========================================================
st.markdown("""
<div class="hero">
<h1>🇲🇾 Sistem Indeks Ketegangan Masyarakat (IKM) Malaysia</h1>

<p style="font-size:18px; line-height:1.8;">
Sistem Indeks Ketegangan Masyarakat (IKM) Malaysia merupakan platform analitik bersepadu yang dibangunkan bagi membantu Jabatan Perpaduan Negara dan Integrasi Nasional (JPNIN) memantau, mengukur dan menilai tahap ketegangan masyarakat secara sistematik di peringkat nasional, negeri, daerah dan lokaliti.
</p>

<p style="font-size:17px; line-height:1.8;">
Sistem ini mengintegrasikan data kaji selidik nasional, data pentadbiran, maklumat lapangan serta dapatan analisis isu semasa bagi mengenal pasti kawasan berisiko, mengesan pola ketegangan masyarakat, menentukan faktor penyumbang utama dan menyokong pelaksanaan intervensi yang lebih tepat, cepat dan berkesan.
</p>

<p style="font-size:17px; line-height:1.8;">
Melalui pendekatan berasaskan data, sistem ini membolehkan pengguna mengenal pasti <b>Hotspot</b>, <b>Tension Point</b> dan <b>Pain Point</b>, memantau perubahan skor indeks mengikut lokasi dan tempoh masa, serta menilai keberkesanan program intervensi yang dilaksanakan bagi memperkukuh perpaduan dan keharmonian masyarakat Malaysia.
</p>

<span class="badge">📊 Pemantauan Nasional</span>
<span class="badge">🗺️ Analisis Negeri, Daerah & Lokaliti</span>
<span class="badge">🔥 Hotspot & Tension Point</span>
<span class="badge">🎯 Pain Point Analysis</span>
<span class="badge">🤝 Cadangan Intervensi</span>
<span class="badge">📈 Sistem Amaran Awal</span>

</div>
""", unsafe_allow_html=True)

with st.expander("📤 Upload Excel/CSV survey 20,000 responden atau guna data simulasi", expanded=False):
    st.write("Upload boleh guna kolum item seperti `A2_Rumah_Ibadat`, `A3_Masjid_Kuil_Gereja`, `M2_Provokasi_Viral`, atau sekurang-kurangnya kolum dimensi D1-D8.")
    upload = st.file_uploader("Upload survey Excel/CSV", type=["xlsx","csv"])

udf = load_file(upload) if 'upload' in locals() else None
df = udf if udf is not None else generate_data(20000)
data_label = f"Data upload: {upload.name}" if udf is not None else "Data simulasi 20,000 responden"

fc = st.columns([1.15,1.15,1.15,1.15,1.15])
with fc[0]: negeri_filter = st.selectbox("Negeri", ["Semua"]+sorted(df["Negeri"].dropna().unique().tolist()))
with fc[1]:
    tmp = df if negeri_filter=="Semua" else df[df["Negeri"]==negeri_filter]
    daerah_filter = st.selectbox("Daerah", ["Semua"]+sorted(tmp["Daerah"].dropna().unique().tolist()))
with fc[2]: umur_filter = st.selectbox("Umur", ["Semua"]+sorted(df["Kumpulan_Umur"].dropna().unique().tolist()))
with fc[3]: etnik_filter = st.selectbox("Etnik", ["Semua"]+sorted(df["Etnik"].dropna().unique().tolist()))
with fc[4]: isu_filter = st.selectbox("Fokus isu", ["Semua Dimensi"]+[DIMENSIONS[d]["label"] for d in DIMENSIONS])

fdf = df.copy()
if negeri_filter != "Semua": fdf = fdf[fdf["Negeri"]==negeri_filter]
if daerah_filter != "Semua": fdf = fdf[fdf["Daerah"]==daerah_filter]
if umur_filter != "Semua": fdf = fdf[fdf["Kumpulan_Umur"]==umur_filter]
if etnik_filter != "Semua": fdf = fdf[fdf["Etnik"]==etnik_filter]
if isu_filter != "Semua Dimensi":
    dim_selected = [d for d,cfg in DIMENSIONS.items() if cfg["label"]==isu_filter][0]
else:
    dim_selected = None

# =========================================================
# TABS
# =========================================================
tabs = st.tabs(["01 Executive KPI", "02 Item Action Intelligence", "03 Hotspot & Lokaliti", "04 SEM & Teori", "05 Media Issue", "06 Intervensi", "07 Data"])

with tabs[0]:
    st.subheader("Executive KPI — Indeks Ketegangan Masyarakat Malaysia")
    st.caption(data_label)
    geo_daerah = aggregate(fdf, ["Negeri","Daerah"])
    geo_lokal = aggregate(fdf, ["Negeri","Daerah","Lokaliti"])
    item_top = item_intelligence(fdf).iloc[0]
    house_score = fdf[["A2_Rumah_Ibadat","A3_Masjid_Kuil_Gereja","A5_Fitnah_Agama"]].mean().mean()
    action_locs = geo_lokal[geo_lokal["IKM_Score"]>=70]
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: kpi("IKM Nasional", f"{fdf['IKM_Score'].mean():.1f}", "Skor risiko komposit")
    with c2: kpi("Responden", f"{len(fdf):,}", "Survey aktif")
    with c3: kpi("Daerah Hotspot", f"{(geo_daerah['IKM_Score']>=70).sum()}", "IKM ≥ 70")
    with c4: kpi("Lokaliti Tindakan", f"{len(action_locs)}", "Hotspot lokaliti")
    with c5: kpi("Isu Rumah Ibadat", f"{house_score:.1f}", "Masjid/kuil/gereja")
    with c6: kpi("Item Kritikal", item_top["Item"], item_top["Label"])

    a,b = st.columns([1.25,1])
    with a:
        dim_df = pd.DataFrame({"Dimensi":[DIMENSIONS[d]["label"] for d in DIMENSIONS], "Skor Risiko":[(100-fdf[d].mean()) if d=="D8_Ketahanan_Sosial" else fdf[d].mean() for d in DIMENSIONS]})
        fig = px.bar(dim_df.sort_values("Skor Risiko"), x="Skor Risiko", y="Dimensi", orientation="h", text="Skor Risiko", title="Skor Risiko Mengikut Dimensi IKM")
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        st.plotly_chart(plotly_layout(fig, 500), use_container_width=True)
    with b:
        st.markdown(f"""
        <div class='panel red'>
        <h3>Where to Take Action?</h3>
        <p><b>Item paling kritikal:</b> {item_top['Label']} ({item_top['Skor']:.1f})</p>
        <p><b>Daerah tertinggi:</b> {geo_daerah.iloc[0]['Daerah']}, {geo_daerah.iloc[0]['Negeri']} ({geo_daerah.iloc[0]['IKM_Score']:.1f})</p>
        <p><b>Lokaliti tertinggi:</b> {geo_lokal.iloc[0]['Lokaliti']}, {geo_lokal.iloc[0]['Daerah']} ({geo_lokal.iloc[0]['IKM_Score']:.1f})</p>
        <p>Sistem ini bukan hanya kata skor tinggi; ia tunjuk <b>item apa</b>, <b>lokasi mana</b>, dan <b>tindakan apa</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        status = geo_daerah["Status_Risiko"].value_counts().reset_index(); status.columns=["Status","Bilangan"]
        fig = px.pie(status, values="Bilangan", names="Status", title="Status Daerah")
        st.plotly_chart(plotly_layout(fig, 330), use_container_width=True)

with tabs[1]:
    st.subheader("Item-Level Action Intelligence")
    st.write("Bahagian ini jawab soalan panel: *item mana yang menyebabkan skor tinggi dan kawasan mana perlu tindakan?*")
    item_df = item_intelligence(fdf)
    if dim_selected:
        item_df = item_df[item_df["Dimensi"]==DIMENSIONS[dim_selected]["label"]]
    c1,c2 = st.columns([1.2,1])
    with c1:
        top20 = item_df.head(20).sort_values("Skor")
        fig = px.bar(top20, x="Skor", y="Label", color="Dimensi", orientation="h", title="Top Item Kritikal Nasional / Filter Semasa", text="Skor")
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        st.plotly_chart(plotly_layout(fig, 650), use_container_width=True)
    with c2:
        st.dataframe(item_df[["Item","Label","Dimensi","Skor","Tindakan"]].head(25), use_container_width=True, hide_index=True)
    st.markdown("### Item kritikal mengikut daerah")
    geo = aggregate(fdf,["Negeri","Daerah"])
    view = geo[["Negeri","Daerah","Responden","IKM_Score","Status_Risiko","Item_Kritikal","Item_Kritikal_Label","Dimensi_Dominan_Label"]].head(30)
    st.dataframe(view, use_container_width=True, hide_index=True)

with tabs[2]:
    st.subheader("Hotspot, Tension Point dan Lokaliti Tindakan")
    level = st.radio("Tahap analisis", ["Negeri","Daerah","Lokaliti"], horizontal=True)
    group = ["Negeri"] if level=="Negeri" else ["Negeri","Daerah"] if level=="Daerah" else ["Negeri","Daerah","Lokaliti"]
    geo = aggregate(fdf, group)
    a,b = st.columns([1.2,1])
    with a:
        ycol = level
        fig = px.bar(geo.head(25).sort_values("IKM_Score"), x="IKM_Score", y=ycol, color="Status_Risiko", orientation="h", text="IKM_Score", title=f"Top 25 Risiko Mengikut {level}")
        fig.update_traces(texttemplate="%{text:.1f}")
        st.plotly_chart(plotly_layout(fig, 640), use_container_width=True)
    with b:
        selected = st.selectbox("Pilih lokasi untuk profil", geo.apply(lambda r: " | ".join([str(r[g]) for g in group])+f" — {r['IKM_Score']:.1f}", axis=1).tolist())
        ix = geo.apply(lambda r: " | ".join([str(r[g]) for g in group])+f" — {r['IKM_Score']:.1f}", axis=1).tolist().index(selected)
        row = geo.iloc[ix]
        dim_values = pd.DataFrame({"Dimensi":[DIMENSIONS[d]["label"] for d in DIMENSIONS], "Skor":[(100-row[d]) if d=="D8_Ketahanan_Sosial" else row[d] for d in DIMENSIONS]})
        fig = px.line_polar(dim_values, r="Skor", theta="Dimensi", line_close=True, title="Profil Risiko Lokasi")
        st.plotly_chart(plotly_layout(fig, 430), use_container_width=True)
        priority, acts = action_for(row["Item_Kritikal"], row["Dimensi_Dominan"], row["IKM_Score"])
        st.markdown(f"""
        <div class='panel orange'>
        <h3>{priority}</h3>
        <p><b>Item:</b> {row['Item_Kritikal_Label']}</p>
        <ol><li>{acts[0]}</li><li>{acts[1]}</li><li>{acts[2]}</li></ol>
        </div>
        """, unsafe_allow_html=True)
    st.dataframe(geo.head(50)[group+["Responden","IKM_Score","Status_Risiko","Item_Kritikal_Label","Dimensi_Dominan_Label"]], use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("SEM & Teori: Soalan → Konstruk → Indeks")
    sem = []
    for dim, cfg in DIMENSIONS.items():
        sem.append([cfg["theory"], cfg["label"], dim, len(ITEM_BANK[dim]), cfg["weight"], fdf[dim].mean()])
    semdf = pd.DataFrame(sem, columns=["Teori", "Konstruk SEM", "Kod", "Bil. Item", "Berat Indeks", "Purata Skor"])
    st.dataframe(semdf, use_container_width=True, hide_index=True)
    c1,c2 = st.columns([1,1])
    with c1:
        fig = px.bar(semdf, x="Konstruk SEM", y="Purata Skor", color="Teori", title="Skor Konstruk SEM")
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(plotly_layout(fig, 480), use_container_width=True)
    with c2:
        st.markdown("""
        <div class='panel blue'>
        <h3>Model SEM yang dicadangkan</h3>
        <p><b>Ekonomi, konflik, digital, agama dan institusi</b> bertindak sebagai pendorong ketegangan.</p>
        <p><b>Ketahanan sosial</b> bertindak sebagai faktor pelindung; sebab itu dalam indeks risiko ia dikira sebagai 100 - D8.</p>
        <p>SEM boleh uji laluan seperti: Ekonomi → Konflik → IKM; Digital → Agama/Budaya → IKM; Institusi → Ketegangan Sosial → IKM.</p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"IKM_i=\sum_{j=1}^{7}w_jD_{ij}+w_8(100-D_{i8})")

with tabs[4]:
    st.subheader("Media & Public Issue Monitor")
    st.write("Modul ini embed isu viral seperti masjid, kuil, rumah ibadat, agama, kaum, kos sara hidup, politik dan provokasi digital.")
    media_file = st.file_uploader("Upload media/news Excel/CSV", type=["xlsx","csv"], key="media")
    if media_file:
        mdf = pd.read_csv(media_file) if media_file.name.lower().endswith(".csv") else pd.read_excel(media_file)
    else:
        rng = np.random.default_rng(11)
        sample = [
            "Isu rumah ibadat menjadi perhatian penduduk setempat",
            "Naratif masjid dan kuil tular di media sosial",
            "Kos sara hidup dan harga barang menekan komuniti bandar",
            "Komen kebencian berkaitan agama mencetus kebimbangan",
            "Perbezaan politik memanaskan perbincangan komuniti",
            "Program perpaduan bantu redakan salah faham masyarakat",
            "Aduan penduduk terhadap respons agensi meningkat",
            "Berita palsu berkaitan kaum tersebar secara viral",
        ]
        mdf = pd.DataFrame({
            "Tarikh":[datetime.today().date()-timedelta(days=int(x)) for x in rng.integers(0,30,350)],
            "Sumber":rng.choice(["Sinar Harian","Astro Awani","Bernama","Utusan","BH","Portal Awam"],350),
            "Tajuk":rng.choice(sample,350),
            "Negeri":rng.choice(list(NEGERI_DAERAH.keys()),350),
            "Daerah":"-"
        })
    if "Tajuk" not in mdf.columns: mdf["Tajuk"] = ""
    text = mdf["Tajuk"].astype(str).str.lower()
    issue_keywords = {
        "Agama/Rumah Ibadat":["agama","rumah ibadat","masjid","kuil","gereja","tokong"],
        "Kaum/Identiti":["kaum","etnik","bangsa","perkauman"],
        "Ekonomi/Kos Sara Hidup":["kos sara hidup","harga","barang","ekonomi","pekerjaan","sewa"],
        "Digital/Viral":["viral","media sosial","fitnah","berita palsu","tular"],
        "Politik/Kepimpinan":["politik","kepimpinan","parti","kerajaan"],
        "Institusi/Aduan":["aduan","agensi","institusi","perkhidmatan"],
    }
    rows=[]
    for issue,kws in issue_keywords.items():
        count = sum(text.str.contains(k, regex=False).sum() for k in kws)
        rows.append([issue, int(count), min(100, count/max(len(mdf),1)*100)])
    idf = pd.DataFrame(rows, columns=["Isu","Sebutan","Hot_Issue_Score"]).sort_values("Hot_Issue_Score", ascending=False)
    c1,c2=st.columns([1.15,1])
    with c1:
        fig = px.bar(idf.sort_values("Hot_Issue_Score"), x="Hot_Issue_Score", y="Isu", orientation="h", text="Hot_Issue_Score", title="Hot Issue Score Media")
        fig.update_traces(texttemplate="%{text:.1f}")
        st.plotly_chart(plotly_layout(fig, 450), use_container_width=True)
    with c2:
        st.dataframe(idf, use_container_width=True, hide_index=True)
        top_issue = idf.iloc[0]
        st.markdown(f"""<div class='panel red'><h3>Emerging Issue</h3><p><b>{top_issue['Isu']}</b> sedang dominan dalam data media semasa.</p><p>Gunakan ini sebagai <b>early warning layer</b>, bukan skor utama IKM.</p></div>""", unsafe_allow_html=True)
    st.dataframe(mdf.head(80), use_container_width=True, hide_index=True)

with tabs[5]:
    st.subheader("Intervention Recommendation Engine")
    geo = aggregate(fdf, ["Negeri","Daerah","Lokaliti"]).head(20)
    for _, row in geo.iterrows():
        priority, acts = action_for(row["Item_Kritikal"], row["Dimensi_Dominan"], row["IKM_Score"])
        klass = "red" if row["IKM_Score"]>=80 else "orange" if row["IKM_Score"]>=70 else "green"
        st.markdown(f"""
        <div class='panel {klass}'>
        <h3>{row['Lokaliti']}, {row['Daerah']}, {row['Negeri']} — {row['IKM_Score']:.1f}</h3>
        <p><b>Status:</b> {row['Status_Risiko']} | <b>Item kritikal:</b> {row['Item_Kritikal_Label']} | <b>Priority:</b> {priority}</p>
        <ol><li>{acts[0]}</li><li>{acts[1]}</li><li>{acts[2]}</li></ol>
        </div>
        """, unsafe_allow_html=True)

with tabs[6]:
    st.subheader("Data Explorer & Download")
    s1,s2,s3 = st.columns(3)
    with s1: st.download_button("⬇️ Download filtered respondent data", fdf.to_csv(index=False).encode("utf-8"), "ikm_filtered_respondent_data.csv", "text/csv")
    with s2: st.download_button("⬇️ Download daerah action summary", aggregate(fdf,["Negeri","Daerah"]).to_csv(index=False).encode("utf-8"), "ikm_daerah_action_summary.csv", "text/csv")
    with s3: st.download_button("⬇️ Download item intelligence", item_intelligence(fdf).to_csv(index=False).encode("utf-8"), "ikm_item_intelligence.csv", "text/csv")
    st.markdown("### Format kolum penting untuk Excel survey")
    st.dataframe(pd.DataFrame({"Kolum": ["Respondent_ID","Negeri","Daerah","Lokaliti","Umur","Etnik","Agama"]+list(ITEM_LABELS.keys()), "Maksud": ["ID responden","Negeri","Daerah","Lokaliti/kawasan","Umur","Etnik","Agama"]+list(ITEM_LABELS.values())}).head(60), use_container_width=True, hide_index=True)
    st.markdown("### Data semasa")
    st.dataframe(fdf.head(1000), use_container_width=True, hide_index=True)
