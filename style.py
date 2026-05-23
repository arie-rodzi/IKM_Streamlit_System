
import streamlit as st

def apply_premium_style():
    st.markdown("""
    <style>
    :root{
        --navy:#061A33; --navy2:#0B2E59; --blue:#106EBE; --cyan:#00A6D6;
        --gold:#D6A437; --green:#0F9D58; --red:#D93025; --orange:#F29900;
        --purple:#6F42C1; --ink:#102030; --muted:#5B6B7A; --bg:#F3F7FB;
    }
    .stApp{
        background:
          radial-gradient(circle at top left, rgba(0,166,214,.20), transparent 28%),
          radial-gradient(circle at top right, rgba(214,164,55,.18), transparent 26%),
          linear-gradient(180deg,#F7FAFE 0%,#EEF4FA 100%);
    }
    .block-container{padding-top:1.1rem; padding-bottom:2rem; max-width: 1500px;}

    section[data-testid="stSidebar"]{
        background: linear-gradient(180deg,#061A33 0%,#092747 100%) !important;
        border-right: 1px solid rgba(255,255,255,.10);
    }
    section[data-testid="stSidebar"] *{
        color:#FFFFFF !important;
    }
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span{
        color:#F4F8FF !important;
        font-weight:700 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div{
        background:#FFFFFF !important;
        color:#0B1F3A !important;
        border-radius:16px !important;
        border:1px solid rgba(255,255,255,.25) !important;
    }
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] input{
        color:#0B1F3A !important;
    }
    section[data-testid="stSidebar"] [role="radiogroup"] label span{
        color:#FFFFFF !important;
        font-size:15px !important;
    }

    .hero{
        border-radius:28px; padding:28px 32px; color:white;
        background:
        linear-gradient(120deg,rgba(6,26,51,.98),rgba(11,46,89,.96) 55%,rgba(214,164,55,.92));
        box-shadow:0 18px 50px rgba(6,26,51,.22);
        border:1px solid rgba(255,255,255,.25);
        margin-bottom:16px;
    }
    .hero h1{font-size:38px; margin:0; line-height:1.1; letter-spacing:-.7px;}
    .hero p{font-size:16px; opacity:.95; margin-top:10px; max-width:1100px;}
    .badge-row{display:flex; gap:8px; flex-wrap:wrap; margin-top:14px;}
    .badge{padding:7px 12px; border-radius:999px; background:rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.25); font-size:13px; font-weight:800;}

    .glass-card{
        background:rgba(255,255,255,.92); border:1px solid rgba(12,42,75,.10);
        box-shadow:0 14px 36px rgba(11,31,58,.10);
        border-radius:24px; padding:20px; margin-bottom:14px;
    }
    .dark-card{
        background:linear-gradient(135deg,#061A33,#0B2E59);
        color:white; border-radius:24px; padding:22px; box-shadow:0 14px 36px rgba(6,26,51,.22);
        border:1px solid rgba(255,255,255,.12); margin-bottom:14px;
    }
    .metric-card{
        min-height:120px; border-radius:24px; padding:18px;
        background:linear-gradient(180deg,#ffffff,#f6f9fd);
        box-shadow:0 12px 28px rgba(11,31,58,.09);
        border:1px solid rgba(11,31,58,.10);
    }
    .metric-title{font-size:13px; color:#5B6B7A; font-weight:900; text-transform:uppercase; letter-spacing:.4px;}
    .metric-value{font-size:32px; font-weight:950; color:#061A33; margin-top:7px; line-height:1.0;}
    .metric-sub{font-size:13px; color:#6B7C8F; margin-top:7px;}
    .risk-rendah{color:#0F9D58!important}.risk-sederhana{color:#D6A437!important}.risk-tinggi{color:#F29900!important}.risk-kritikal{color:#D93025!important}
    .section-title{
        font-size:24px; font-weight:950; color:#061A33; margin:8px 0 4px 0;
    }
    .section-subtitle{
        color:#5B6B7A; margin-bottom:14px; font-size:14px;
    }
    .objective-chip{
        display:inline-block; padding:7px 12px; border-radius:999px; color:white; background:#0B2E59;
        font-weight:900; margin-right:8px; font-size:13px;
    }
    .callout{
        background:linear-gradient(90deg,rgba(214,164,55,.18),rgba(0,166,214,.10));
        border-left:6px solid #D6A437; padding:14px 16px; border-radius:16px; color:#102030; margin-bottom:12px;
    }
    .mini-table th{background:#061A33!important;color:white!important;}
    div[data-testid="stDataFrame"]{border-radius:18px; overflow:hidden; border:1px solid rgba(11,31,58,.12);}
    .stTabs [data-baseweb="tab-list"]{gap:8px;}
    .stTabs [data-baseweb="tab"]{
        background:#FFFFFF; border-radius:14px 14px 0 0; padding:10px 16px;
        border:1px solid rgba(11,31,58,.10); font-weight:900;
    }
    .stTabs [aria-selected="true"]{
        background:linear-gradient(135deg,#061A33,#0B2E59)!important; color:white!important;
    }
    </style>
    """, unsafe_allow_html=True)

def hero():
    st.markdown("""
    <div class="hero">
        <h1>Sistem Pintar Indeks Ketegangan Masyarakat (IKM)</h1>
        <p>Prototaip nasional berasaskan Python + Streamlit untuk pengiraan indeks, perbandingan negeri/daerah, analisis demografi, analitik media sosial big data, model risiko dan cadangan intervensi lokasi.</p>
        <div class="badge-row">
            <div class="badge">Python Analytics</div>
            <div class="badge">IKM Model Engine</div>
            <div class="badge">Demographic Intelligence</div>
            <div class="badge">Big Data Media Sosial</div>
            <div class="badge">Intervensi Berasaskan Lokasi</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def metric_card(title, value, sub="", risk=None):
    cls = ""
    if risk:
        cls = f"risk-{risk.lower()}"
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value {cls}">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """
