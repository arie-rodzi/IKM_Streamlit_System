
import streamlit as st

NAVY = "#071B38"
BLUE = "#0B3D66"
CYAN = "#00B4D8"
GOLD = "#C9952B"
ORANGE = "#F77F00"
RED = "#C0392B"
GREEN = "#0B6B43"
PURPLE = "#7D3C98"
PINK = "#C2185B"
BG = "#061524"
CARD = "rgba(255,255,255,0.08)"

RISK_COLORS = {
    "Rendah": GREEN,
    "Sederhana": GOLD,
    "Tinggi": ORANGE,
    "Kritikal": RED,
}

PLOTLY_TEMPLATE = "plotly_dark"

COLORWAY = [CYAN, GOLD, ORANGE, PURPLE, PINK, GREEN, "#4CC9F0", "#F72585", "#B5179E", "#7209B7"]

def inject_css():
    st.markdown(f"""
    <style>
    .stApp {{
        background: radial-gradient(circle at top left, #123b66 0, #061524 32%, #030914 100%);
        color: #ffffff;
    }}
    .block-container {{
        padding-top: 0.85rem; padding-bottom: 1.2rem; max-width: 1500px;
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #071B38 0%, #061524 100%);
        border-right: 1px solid rgba(201,149,43,0.35);
    }}
    .hero {{
        background: linear-gradient(135deg, rgba(7,27,56,0.98), rgba(11,61,102,0.95), rgba(201,149,43,0.78));
        padding: 24px 28px; border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.14);
        box-shadow: 0 20px 45px rgba(0,0,0,0.35);
        margin: 0 0 14px 0;
    }}
    .hero h1 {{font-size: 38px; margin: 0; letter-spacing: -0.8px; color:white;}}
    .hero p {{font-size: 15.5px; margin: 8px 0 0 0; opacity:.92; max-width:1120px;}}
    .pill {{
        display:inline-block; padding:6px 12px; border-radius:999px;
        background: rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.18);
        color:#fff; margin-right:8px; font-weight:700; font-size:12px;
    }}
    .kpi {{
        background: linear-gradient(145deg, rgba(255,255,255,.12), rgba(255,255,255,.05));
        border: 1px solid rgba(255,255,255,.16); border-radius: 22px;
        padding: 16px 18px; min-height: 110px;
        box-shadow: 0 16px 36px rgba(0,0,0,.22);
        position: relative; overflow:hidden;
    }}
    .kpi:after {{content:""; position:absolute; right:-45px; top:-45px; width:120px; height:120px; border-radius:50%; background:rgba(201,149,43,.16);}}
    .kpi-title {{font-size:12px; text-transform:uppercase; color:#b7c8dc; font-weight:900; letter-spacing:.5px;}}
    .kpi-value {{font-size:30px; font-weight:1000; color:white; margin-top:6px;}}
    .kpi-sub {{font-size:12px; color:#d6e2f1; margin-top:2px;}}
    .glass {{
        background: rgba(255,255,255,.075); border:1px solid rgba(255,255,255,.14);
        border-radius:24px; padding:18px 18px 12px 18px; margin-bottom:14px;
        box-shadow: 0 12px 28px rgba(0,0,0,.18);
    }}
    .section-title {{font-size:21px; font-weight:1000; margin:0 0 8px 0; color:white;}}
    .section-sub {{font-size:13px; color:#b7c8dc; margin-bottom:10px;}}
    .insight {{
        background: linear-gradient(135deg, rgba(0,180,216,.16), rgba(201,149,43,.13));
        border:1px solid rgba(255,255,255,.14); border-radius:20px; padding:14px 16px;
        margin: 8px 0;
    }}
    .critical-box {{
        background: linear-gradient(135deg, rgba(192,57,43,.24), rgba(247,127,0,.16));
        border:1px solid rgba(255,120,80,.35); border-radius:20px; padding:16px;
    }}
    .ok-box {{
        background: linear-gradient(135deg, rgba(11,107,67,.22), rgba(0,180,216,.12));
        border:1px solid rgba(100,255,200,.25); border-radius:20px; padding:16px;
    }}
    div[data-testid="stMetric"] {{background: rgba(255,255,255,.08); padding: 12px; border-radius: 18px; border:1px solid rgba(255,255,255,.12);}}
    .stTabs [data-baseweb="tab-list"] {{gap: 8px;}}
    .stTabs [data-baseweb="tab"] {{
        background: rgba(255,255,255,.08); border-radius: 16px; padding: 10px 14px;
        border: 1px solid rgba(255,255,255,.12); color:#fff;
    }}
    .stTabs [aria-selected="true"] {{background: linear-gradient(135deg, #0B3D66, #C9952B) !important;}}
    .dataframe {{font-size: 12px;}}
    </style>
    """, unsafe_allow_html=True)

def hero():
    st.markdown("""
    <div class="hero">
        <span class="pill">RM2.7 Juta National Prototype</span><span class="pill">Python + Streamlit</span><span class="pill">Big Data Media Sosial</span><span class="pill">Early Warning</span>
        <h1>Sistem Pintar Indeks Ketegangan Masyarakat (IKM)</h1>
        <p>Platform analitik nasional untuk mengira IKM, membandingkan negeri dan daerah, menganalisis demografi, memantau isyarat media sosial, serta mencadangkan intervensi lokasi secara automatik.</p>
    </div>
    """, unsafe_allow_html=True)

def kpi_card(title, value, subtitle="", color="#FFFFFF"):
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value" style="color:{color};">{value}</div>
        <div class="kpi-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def glass_open(title, sub=""):
    st.markdown(f"<div class='glass'><div class='section-title'>{title}</div><div class='section-sub'>{sub}</div>", unsafe_allow_html=True)

def glass_close():
    st.markdown("</div>", unsafe_allow_html=True)
