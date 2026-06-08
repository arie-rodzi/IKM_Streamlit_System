import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import hashlib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# --- CONFIGURATION APLIKASI UTAMA ---
st.set_page_config(
    page_title="Sistem Analitik Komposit IKMM 2026",
    layout="wide",
    initial_sidebar_state="expanded"
)

ADMIN_PASSWORD = "admin123"

# --- REKA BENTUK VISUAL: LIGHT EXECUTIVE WINDOWS THEME ---
def apply_executive_premium_theme():
    st.markdown("""
        <style>
            .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
            [data-testid="stSidebar"] { background-color: #0F172A !important; border-right: 2px solid #E2E8F0 !important; }
            [data-testid="stSidebar"] * { color: #F8FAFC !important; }
            h1, h2, h3, h4, p, span, label { color: #0F172A !important; font-family: 'Segoe UI', Inter, sans-serif !important; }
            .stTabs [data-baseweb="tab-list"] { gap: 6px; background-color: #E2E8F0; padding: 6px; border-radius: 10px; border: 1px solid #CBD5E1; }
            .stTabs [data-baseweb="tab"] { height: 38px; padding: 0px 16px !important; background-color: transparent !important; border-radius: 6px !important; color: #475569 !important; font-weight: 600 !important; transition: all 0.2s ease; }
            .stTabs [aria-selected="true"] { background-color: #FFFFFF !important; color: #1E3A8A !important; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08) !important; border: 1px solid #CBD5E1 !important; }
            .kpi-card-premium { background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 6px solid #1E40AF; border-radius: 12px; padding: 22px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
            .highlight-analysis-box { background-color: #EFF6FF; border-left: 5px solid #1D4ED8; padding: 22px; border-radius: 0 10px 10px 0; margin: 15px 0; color: #1E3A8A !important; line-height: 1.7; font-size: 14px; }
            .danger-analysis-box { background-color: #FEF2F2; border-left: 5px solid #DC2626; padding: 22px; border-radius: 0 10px 10px 0; margin: 15px 0; color: #991B1B !important; line-height: 1.7; font-size: 14px; }
            .warning-analysis-box { background-color: #FFFBEB; border-left: 5px solid #D97706; padding: 22px; border-radius: 0 10px 10px 0; margin: 15px 0; color: #92400E !important; line-height: 1.7; font-size: 14px; }
            .success-analysis-box { background-color: #F0FDF4; border-left: 5px solid #16A34A; padding: 22px; border-radius: 0 10px 10px 0; margin: 15px 0; color: #166534 !important; line-height: 1.7; font-size: 14px; }
            .loc-card-premium { border: 1px solid #CBD5E1; border-radius: 8px; padding: 18px; margin-bottom: 15px; background-color: #FFFFFF; border-left: 5px solid #8B5CF6; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
            .stDataFrame { border: 1px solid #E2E8F0 !important; border-radius: 8px !important; background-color: #FFFFFF !important; }
        </style>
    """, unsafe_allow_html=True)

def render_kpi_card(label, value, unit, tier="low"):
    color_map = {"low": "#10B981", "tension": "#F59E0B", "pain": "#DB2777", "hotspot": "#EF4444"}
    border_color = color_map.get(tier, "#1E40AF")
    st.markdown(f"""
    <div class="kpi-card-premium" style="border-left-color: {border_color};">
        <p class="kpi-label" style="color: #475569 !important; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px; margin: 0;">{label}</p>
        <div class="kpi-value" style="font-size: 36px; font-weight: 800; margin: 6px 0; color: {border_color} !important;">{value}</div>
        <p style='color: #64748B !important; font-size: 11px; font-weight: 500; margin: 0;'>{unit}</p>
    </div>
    """, unsafe_allow_html=True)

# --- ENGIN ANALITIK STRATEGIK DASAR KERAJAAN (IKMM 2026) ---
class IKMMDasarEngine:
    def __init__(self):
        self.respondent_data = None
        self.questionnaire_master = None
        self.qualitative_response = None
        self.theory_mapping = None
        self.intervention_library = None
        self.pain_point_mapping = None
        self.tension_point_mapping = None
        self.media_issue_summary = None
        self.fgd_expert = None
        self.state_zone_mapping = None
        self.dashboard_config = None
        self.data_loaded = False
        self.filename = "IKM_Master_Dataset_20000_Respondents.xlsx"
        
        self.dim_item_ranges = {
            'D1 Ethnic Tension': [f'IKM_{i:03d}' for i in range(1, 13)],
            'D2 Religious Tension': [f'IKM_{i:03d}' for i in range(13, 25)],
            'D3 Economic Tension': [f'IKM_{i:03d}' for i in range(25, 37)],
            'D4 Political Tension': [f'IKM_{i:03d}' for i in range(37, 49)],
            'D5 Generational Tension': [f'IKM_{i:03d}' for i in range(49, 61)],
            'D6 Urban-Rural Tension': [f'IKM_{i:03d}' for i in range(61, 73)],
            'D7 Institutional and Governance Tension': [f'IKM_{i:03d}' for i in range(73, 85)],
            'D8 Social Resilience': [f'IKM_{i:03d}' for i in range(85, 97)],
            'D9 Digital Tension': [f'IKM_{i:03d}' for i in range(97, 109)]
        }

    def connect_and_load_workbook(self, file_source=None):
        try:
            xls = pd.ExcelFile(self.filename) if file_source is None else pd.ExcelFile(file_source)
            self.respondent_data = pd.read_excel(xls, sheet_name='respondent_data')
            self.questionnaire_master = pd.read_excel(xls, sheet_name='questionnaire_master')
            
            if 'qualitative_response' in xls.sheet_names:
                self.qualitative_response = pd.read_excel(xls, sheet_name='qualitative_response')
            if 'theory_mapping' in xls.sheet_names:
                self.theory_mapping = pd.read_excel(xls, sheet_name='theory_mapping')
            if 'intervention_library' in xls.sheet_names:
                self.intervention_library = pd.read_excel(xls, sheet_name='intervention_library')
            if 'pain_point_mapping' in xls.sheet_names:
                self.pain_point_mapping = pd.read_excel(xls, sheet_name='pain_point_mapping')
            if 'tension_point_mapping' in xls.sheet_names:
                self.tension_point_mapping = pd.read_excel(xls, sheet_name='tension_point_mapping')
            if 'media_issue_summary' in xls.sheet_names:
                self.media_issue_summary = pd.read_excel(xls, sheet_name='media_issue_summary')
            if 'fgd_expert' in xls.sheet_names:
                self.fgd_expert = pd.read_excel(xls, sheet_name='fgd_expert')
            if 'state_zone_mapping' in xls.sheet_names:
                self.state_zone_mapping = pd.read_excel(xls, sheet_name='state_zone_mapping')
            if 'dashboard_config' in xls.sheet_names:
                self.dashboard_config = pd.read_excel(xls, sheet_name='dashboard_config')
                
            self.data_loaded = True
            return True
        except:
            return False

    def get_tier(self, score):
        if score >= 80.0: return "hotspot"
        elif score >= 60.0: return "pain"
        elif score >= 40.0: return "tension"
        else: return "low"

    def calculate_composite_index(self, df_target):
        all_items = [f'IKM_{i:03d}' for i in range(1, 109) if f'IKM_{i:03d}' in df_target.columns]
        if not all_items or df_target.empty: return 0.0, "low"
        mean_raw = df_target[all_items].mean().mean()
        normalized_score = ((mean_raw - 1) / 4) * 100
        return normalized_score, self.get_tier(normalized_score)

    def calculate_single_dimension_score(self, dim_name, df_target):
        target_items = [it for it in self.dim_item_ranges.get(dim_name, []) if it in df_target.columns]
        if not target_items or df_target.empty: return 0.0
        dim_mean_raw = df_target[target_items].mean().mean()
        return ((dim_mean_raw - 1) / 4) * 100

    def get_dimension_composite_scores(self, df_target):
        results = {}
        for dim in self.dim_item_ranges.keys():
            results[dim] = self.calculate_single_dimension_score(dim, df_target)
        return results

    def calculate_item_scores(self, df_target):
        all_items = [f'IKM_{i:03d}' for i in range(1, 109) if f'IKM_{i:03d}' in df_target.columns]
        scores = {}
        if df_target.empty: return scores
        for item in all_items:
            scores[item] = {
                'mean': df_target[item].mean(),
                'std': df_target[item].std(),
                'median': df_target[item].median(),
                'count': len(df_target[item].dropna())
            }
        return scores

    def get_registered_items(self):
        if self.questionnaire_master is None: return []
        return sorted(self.questionnaire_master['Item_Code'].dropna().unique().tolist())

    def get_demographic_columns(self):
        if self.respondent_data is None: return []
        demo_cols = ['Zone', 'State', 'District', 'Locality', 'Gender', 'Age', 'Generation', 'Ethnicity', 'Religion', 'Education', 'Occupation', 'Income_Group', 'Urban_Rural', 'Type_of_Respondent']
        return [col for col in demo_cols if col in self.respondent_data.columns]

    def get_filter_options(self, column_name):
        if self.respondent_data is None or column_name not in self.respondent_data.columns:
            return []
        return sorted(self.respondent_data[column_name].dropna().astype(str).unique().tolist())

    def apply_filters(self, filters_dict):
        data = self.respondent_data.copy()
        for col, values in filters_dict.items():
            if values and col in data.columns:
                data = data[data[col].isin(values)]
        return data

    # --- JANAAN MANUSKRIP HTML AGUNG BERAKARKAN TAPISAN AKTIF (MEMBACA DATA SIKLUS TERPENAPIS 100%) ---
    def generate_html_dossier_report(self, title, officer, branch, df_active):
        score, tier = self.calculate_composite_index(df_active)
        total_resp = len(df_active)
        now_str = datetime.now().strftime('%d %B %Y')
        items = self.get_registered_items()
        
        dim_labels = list(self.dim_item_ranges.keys())
        dim_values = [self.calculate_single_dimension_score(d, df_active) for d in dim_labels]
        
        # Pengiraan Geospasial berpaksi penuh kepada df_active (Data Terpenapis)
        geo_means_html = df_active.groupby(['Zone', 'State', 'District', 'Urban_Rural'])[items].mean().mean(axis=1).sort_values(ascending=False) if not df_active.empty else pd.Series()

        html_master = f"""
        <!DOCTYPE html>
        <html lang="ms">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body {{ font-family: 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #F8FAFC; color: #0F172A; padding: 50px; line-height: 1.8; }}
                .dossier-wrapper {{ max-width: 1050px; margin: 0 auto; background: #FFFFFF; padding: 60px; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }}
                .header-banner {{ background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); color: #FFFFFF; padding: 45px; text-align: center; border-radius: 12px; border-bottom: 6px solid #FFD700; margin-bottom: 40px; }}
                .confidential-tag {{ color: #EF4444; font-weight: 900; letter-spacing: 2px; font-size: 14px; margin-bottom: 10px; text-transform: uppercase; }}
                .section-title {{ color: #1E3A8A; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; margin-top: 40px; font-size: 20px; text-transform: uppercase; letter-spacing: 0.5px; page-break-after: avoid; }}
                .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0; }}
                .kpi-box {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-top: 4px solid #1E40AF; padding: 20px; border-radius: 8px; text-align: center; }}
                .kpi-val {{ font-size: 32px; font-weight: 800; color: #1E3A8A; margin: 10px 0; }}
                .chart-container {{ position: relative; margin: 30px 0; padding: 20px; border: 1px solid #E2E8F0; border-radius: 8px; background: #F8FAFC; }}
                .table-premium {{ width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 14px; }}
                .table-premium th {{ background: #0F172A; color: #FFFFFF; padding: 14px; text-align: left; font-weight: 600; }}
                .table-premium td {{ padding: 12px; border-bottom: 1px solid #E2E8F0; color: #334155; }}
                .table-premium tr:nth-child(even) {{ background-color: #F8FAFC; }}
                .loc-card-html {{ border: 1px solid #CBD5E1; border-radius: 8px; padding: 20px; margin-bottom: 15px; background: #FFFFFF; border-left: 5px solid #F59E0B; font-size: 14px; }}
                .loc-card-html.danger {{ background-color: #FEF2F2; border-left-color: #EF4444; }}
                .loc-card-html.success {{ background-color: #F0FDF4; border-left-color: #16A34A; }}
                .highlight-box {{ background-color: #EFF6FF; border-left: 4px solid #3B82F6; padding: 25px; border-radius: 0 8px 8px 0; margin: 20px 0; font-size: 14px; line-height: 1.8; color: #1E3A8A; }}
                .page-break {{ page-break-before: always; }}
                .meta-footer {{ margin-top: 60px; padding-top: 20px; border-top: 2px dashed #E2E8F0; text-align: center; font-size: 12px; color: #64748B; }}
            </style>
        </head>
        <body>
            <div class="dossier-wrapper">
                <div class="header-banner">
                    <div class="confidential-tag">SULIT — MANUSKRIP STRATEGIDASAR TERPENAPIS JPM</div>
                    <h1 style="margin: 0; font-size: 26px;">{title}</h1>
                    <p style="margin: 10px 0 0 0; font-size: 14px; color: #94A3B8;">Laporan berasaskan Kriteria Tapisan Kumpulan Sasar Geografi</p>
                    <p style="margin: 5px 0 0 0; font-size: 12px; color: #CBD5E1;">Tarikh Kompleks: {now_str} | Kumpulan Data Aktif: {total_resp:,} Responden</p>
                </div>
                
                <div class="section-title">1.0 Ringkasan KPI Komposit Terpenapis</div>
                <div class="kpi-grid">
                    <div class="kpi-box">
                        <div style="color:#64748B; font-weight:700; font-size:11px;">Indeks Ketegangan Kluster</div>
                        <div class="kpi-val">{score:.2f}%</div>
                        <div style="font-size:11px; font-weight:600; color:#475569;">Status: {tier.upper()}</div>
                    </div>
                    <div class="kpi-box">
                        <div style="color:#64748B; font-weight:700; font-size:11px;">Jumlah Sampel Kluster</div>
                        <div class="kpi-val">{total_resp:,}</div>
                        <div style="font-size:11px; font-weight:600; color:#475569;">Responden Tertapis DOSM</div>
                    </div>
                    <div class="kpi-box">
                        <div style="color:#64748B; font-weight:700; font-size:11px;">Keamatan Amaran Siber Kluster (D9)</div>
                        <div class="kpi-val">{self.calculate_single_dimension_score('D9 Digital Tension', df_active):.2f}%</div>
                        <div style="font-size:11px; font-weight:600; color:#EF4444;">D9 Siber Sektor Ditapis</div>
                    </div>
                </div>

                <div class="page-break"></div>

                <div class="section-title">2.0 Grafik Keamatan 9 Dimensi Bagi Kluster Ditapis</div>
                <div class="chart-container">
                    <canvas id="dimensionsChart" style="max-height: 400px;"></canvas>
                </div>

                <div class="page-break"></div>

                <div class="section-title">3.0 Jadual Profil Deskriptif Sosio-Demografi Kluster Terpenapis</div>
                <table class="table-premium">
                    <thead><tr><th>Pemboleh Ubah Demografi</th><th>Klasifikasi Parameter Kumpulan Sasar</th><th>Frekuensi (Bil.)</th><th>Peratusan (%)</th></tr></thead>
                    <tbody>"""
        for col in self.get_demographic_columns():
            counts = df_active[col].value_counts() if col in df_active.columns else pd.Series()
            for cat, val in counts.items():
                pct = (val / total_resp) * 100
                html_master += f"<tr><td><b>{col}</b></td><td>{cat}</td><td>{val:,}</td><td><b>{pct:.2f}%</b></td></tr>"
        html_master += """
                    </tbody>
                </table>
                <div class="page-break"></div>
        """

        # BLOCK 4: THEORETICAL DISSERTATION
        html_master += """
                <div class="section-title">4.0 Pemodelan Teori & Huraian Keputusan Item Stressor Kluster Terpenapis</div>"""
        
        theory_dictionary = {
            "Social Identity Theory": {"Pengasas": "Henri Tajfel & John Turner (1979)", "Dimensi": "D1 Ethnic Tension"},
            "Conflict Theory": {"Pengasas": "Karl Marx / Max Weber", "Dimensi": "D2 Religious Tension"},
            "Relative Deprivation Theory": {"Pengasas": "Samuel Stouffer (1949) / Ted Robert Gurr (1970)", "Dimensi": "D3 Economic Tension"}
        }

        for t_name, t_meta in theory_dictionary.items():
            qm_subset = self.questionnaire_master[self.questionnaire_master['Theory'] == t_name]
            if not qm_subset.empty and not df_active.empty:
                codes = [c for c in qm_subset['Item_Code'].tolist() if c in df_active.columns]
                if codes:
                    t_means = df_active[codes].mean()
                    id_max = t_means.idxmax()
                    val_max = t_means.max()
                    pct_max = ((val_max - 1) / 4) * 100
                    stmt_max = self.questionnaire_master[self.questionnaire_master['Item_Code'] == id_max]['Statement'].values[0]
                    
                    html_master += f"""
                    <div style='margin-bottom: 25px; padding: 20px; border: 1px solid #CBD5E1; border-radius: 8px;'>
                        <h4>📚 {t_name} — Konstruk {t_meta['Dimensi']}</h4>
                        <div style='margin-top:10px; background-color:#FEE2E2; padding:12px; border-radius:4px; border-left:5px solid #EF4444; font-size:12.5px; color:#991B1B;'>
                            🚨 <b>Stressor Utama Terkesan Dalam Kluster Tapisan ({id_max}): Min {val_max:.2f} ({pct_max:.1f}%)</b><br>
                            <i>Kenyataan Item Soalan Asal:</i> "{stmt_max}"
                        </div>
                    </div>"""
        html_master += """<div class="page-break"></div>"""

        # BLOCK 5: GEOGRAPHICAL SPATIAL LOOP UNRESTRICTED FOR HTML REPORT
        html_master += """
                <div class="section-title">5.0 Laporan Hierarki Geografi Rantaian Lokasi Terpenapis berserta Stressor Setempat</div>"""
        
        if not geo_means_html.empty:
            for rank, ((zn, st_n, ds_n, ur_n), v_score) in enumerate(geo_means_html.items()):
                pct_v = ((v_score - 1) / 4) * 100
                sub_df = df_active[(df_active['Zone']==zn) & (df_active['State']==st_n) & (df_active['District']==ds_n) & (df_active['Urban_Rural']==ur_n)]
                if not sub_df.empty:
                    sub_item = sub_df[items].mean().idxmax()
                    sub_stmt = self.questionnaire_master[self.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                    tier_tag = "danger" if pct_v >= 80.0 else ("success" if pct_v < 60.0 else "")
                    html_master += f"""
                    <div class="loc-card-html {tier_tag}">
                        <b>📍 RANTAIAN LOKASI KLUSTER #{rank+1}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>
                        * Skor Indeks Ketegangan: <b>{pct_v:.2f}%</b> (Klasifikasi: {self.get_tier(pct_v).upper()})<br>
                        * 💥 **Punca Utama Isu Semasa (Stressor):** Item {sub_item} &rarr; <i>"{sub_stmt}"</i>
                    </div>"""
        else:
            html_master += "<p>Tiada rantaian geografi ditemui untuk kluster tapisan semasa.</p>"
            
        html_master += f"""
                <script>
                    const ctx = document.getElementById('dimensionsChart').getContext('2d');
                    new Chart(ctx, {{
                        type: 'bar',
                        data: {{
                            labels: {dim_labels},
                            datasets: [{{
                                label: 'Indeks Ketegangan Dimensi (%)',
                                data: {dim_values},
                                backgroundColor: 'rgba(30, 64, 175, 0.8)',
                                borderColor: 'rgba(30, 64, 175, 1)',
                                borderWidth: 1
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            scales: {{ y: {{ beginAtZero: true, max: 100 }} }}
                        }}
                    }});
                </script>
                <div class="meta-footer">
                    <p>Laporan Sulit Briefing Dossier JPM Diperaku: <b>{officer}</b> | <b>{branch}</b></p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_master

def init_dashboard_session():
    if 'engine' not in st.session_state or not hasattr(st.session_state.engine, 'generate_html_dossier_report'):
        st.session_state.engine = IKMMDasarEngine()
        st.session_state.engine.connect_and_load_workbook()
    if 'auth_state' not in st.session_state:
        st.session_state.auth_state = False

def main():
    init_dashboard_session()
    if not st.session_state.auth_state:
        login_portal = apply_executive_premium_theme()
        c1, c2, c3 = st.columns([1, 1.3, 1])
        with c2:
            st.markdown("<div style='text-align: center; padding-top: 130px;'><h2>🏛️ Urus Setia Polisi IKMM 2026</h2><p>Sistem Intelligence Amaran Awal Konflik Kebangsaan (JPM)</p></div>", unsafe_allow_html=True)
            with st.form("gate_form"):
                token = st.text_input("Sila Masukkan Token Pelepasan Keselamatan", type="password")
                if st.form_submit_button("Sahkan Kredensial Akses", use_container_width=True):
                    if hashlib.sha256(token.encode()).hexdigest() == hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest():
                        st.session_state.auth_state = True
                        st.rerun()
                    else:
                        st.error("Ralat: Pelepasan Keselamatan Ditolak.")
        return
        
    apply_executive_premium_theme()
    engine = st.session_state.engine
    
    # --- 🔒 BAR SISI (SIDEBAR) TAPISAN DASAR GLOBAL YANG BARU & REVISED (3 TERAS SAHAJA) ---
    active_filters = {}
    if engine.data_loaded:
        with st.sidebar:
            st.markdown("### 🧭 Panel Geofilter Teras Kebangsaan")
            
            # Pilihan 1: Pilih Zon Makro
            zon_opts = engine.get_filter_options('Zone')
            sel_zone = st.multiselect("🧭 1. Pilih Wilayah / Zon", zon_opts)
            
            # Pilihan 2: Pilih Negeri Berjajar (Cascading)
            if sel_zone:
                state_subset = engine.respondent_data[engine.respondent_data['Zone'].isin(sel_zone)]
                state_opts = sorted(state_subset['State'].dropna().unique().tolist())
            else:
                state_opts = engine.get_filter_options('State')
            sel_state = st.multiselect("🏛️ 2. Pilih Negeri", state_opts)
            
            # Pilihan 3: Pilih Daerah Pentadbiran Bersasarkan Negeri (Cascading)
            if sel_state:
                district_subset = engine.respondent_data[engine.respondent_data['State'].isin(sel_state)]
                district_opts = sorted(district_subset['District'].dropna().unique().tolist())
            elif sel_zone:
                district_subset = engine.respondent_data[engine.respondent_data['Zone'].isin(sel_zone)]
                district_opts = sorted(district_subset['District'].dropna().unique().tolist())
            else:
                district_opts = engine.get_filter_options('District')
            sel_district = st.multiselect("🏙️ 3. Pilih Daerah / Parlimen", district_opts)
            
            # Ikat pilihan input terus ke kamus global
            if sel_zone: active_filters['Zone'] = sel_zone
            if sel_state: active_filters['State'] = sel_state
            if sel_district: active_filters['District'] = sel_district

    # PENGIRAAN UTAMA: Mengikat data terpenapis ke filtered_df untuk dikongsi oleh kesemua 15 tab
    filtered_df = engine.apply_filters(active_filters)
    sub_total = len(filtered_df)
    items_list_main = engine.get_registered_items()
    
    # Bina rantaian min geospasial berdasarkan filtered_df (Membasmi NameError secara mutlak)
    geo_means_main = filtered_df.groupby(['Zone', 'State', 'District', 'Urban_Rural'])[items_list_main].mean().mean(axis=1).sort_values(ascending=False) if sub_total > 0 else pd.Series()

    st.markdown(f"""
        <div style='background-color: #EFF6FF; padding: 12px; border-radius: 8px; border-left: 5px solid #1D4ED8; margin-bottom: 20px;'>
            <p style='margin:0; font-size:13px; font-weight:700; color:#1E3A8A;'>🌐 MOD PENAPISAN AKTIF: Memproses {sub_total:,} daripada {len(engine.respondent_data):,} Responden Kebangsaan.</p>
        </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs([
        "01 Portal Gateway", "02 Ringkasan Executive", "03 Penilaian Geografi", 
        "04 Pengiraan 9 Indeks", "05 Amaran Item Stressor", "06 Sentimen NLP Kualitatif", 
        "07 Teori Dasar", "08 Pain Points", "09 Tension Points", 
        "10 Amaran Hotspot", "11 Strategi Intervensi", "12 Media Scraping", 
        "13 Dapatan FGD", "14 Dossier Report", "15 Cell Data Explorer"
    ])
    
    # --- TAB 1: PORTAL GATEWAY ---
    with tabs[0]:
        st.subheader("📂 Pengurusan Fail & Deskriptif Profil Kluster")
        uploaded_file = st.file_uploader("Sila Pilih Fail Master Excel IKMM (.xlsx)", type=['xlsx'])
        if uploaded_file and st.button("Proses Fail Excel Baharu", use_container_width=True):
            if engine.connect_and_load_workbook(uploaded_file):
                st.success("Berjaya Dimuat Naik!")
                st.rerun()
        
        st.markdown("---")
        if sub_total > 0:
            g_c1, g_c2 = st.columns(2)
            with g_c1:
                st.plotly_chart(px.pie(names=filtered_df['Zone'].value_counts().index, values=filtered_df['Zone'].value_counts().values, title="Pecahan mengikut Zon Ditapis"), use_container_width=True)
            with g_c2:
                st.plotly_chart(px.bar(x=filtered_df['State'].value_counts().values, y=filtered_df['State'].value_counts().index, orientation='h', title="Taburan Negeri Ditapis"), use_container_width=True)
        else:
            st.warning("Kombinasi tapisan menghasilkan 0 responden. Sila tukar pilihan geofilter anda pada sidebar.")

    # --- TAB 2: RINGKASAN EXECUTIVE (TERPENAPIS MASA NYATA) ---
    with tabs[1]:
        st.subheader("📈 Pusat Kawalan KPI Ketegangan Komposit Kluster")
        if sub_total > 0:
            ikm_score, tier_status = engine.calculate_composite_index(filtered_df)
            c1, c2, c3 = st.columns(3)
            with c1: render_kpi_card("Indeks Ketegangan Semasa (IKM %)", f"{ikm_score:.2f}%", "Berasalkan Kluster Terpenapis", tier=tier_status)
            with c2: 
                status_labels = {"low": "STABIL / TERKAWAL", "tension": "TENSION POINT", "pain": "PAIN POINT", "hotspot": "HOTSPOT CRITICAL"}
                render_kpi_card("Tahap Keseriusan Semasa", status_labels.get(tier_status), "Klasifikasi Isu Kluster", tier=tier_status)
            with c3: render_kpi_card("Saiz Responden Ditapis", f"{sub_total:,}", "Pool Responden Aktif", tier="low")
            
            st.markdown("---")
            dim_data = engine.get_dimension_composite_scores(filtered_df)
            dim_df = pd.DataFrame(list(dim_data.items()), columns=['Dimensi Skrining IKM', 'Indeks Ketegangan (%)']).sort_values('Indeks Ketegangan (%)', ascending=False)
            st.plotly_chart(px.bar(dim_df, x='Indeks Ketegangan (%)', y='Dimensi Skrining IKM', orientation='h', color='Indeks Ketegangan (%)', color_continuous_scale='Reds', text_auto='.1f'), use_container_width=True)
        else:
            st.warning("Tiada data untuk dikira.")

    # --- TAB 3: PENILAIAN GEOGRAFI ---
    with tabs[2]:
        if sub_total > 0:
            state_matrix = filtered_df.groupby('State')[items_list_main].mean().mean(axis=1).reset_index()
            state_matrix.columns = ['Negeri / Wilayah', 'Indeks Ketegangan (IKM %)']
            state_matrix['Indeks Ketegangan (IKM %)'] = (state_matrix['Indeks Ketegangan (IKM %)'] - 1) / 4 * 100
            st.dataframe(state_matrix.sort_values('Indeks Ketegangan (IKM %)', ascending=False), use_container_width=True, hide_index=True)

    # --- TAB 4: PENGIRAAN 9 INDEKS (TERPENAPIS MASA NYATA) ---
    with tabs[3]:
        st.subheader("📊 Pengiraan Spesifik Komposit Setiap Dimensi Skrining Kluster")
        if sub_total > 0:
            grid_c1, grid_c2, grid_c3 = st.columns(3)
            for idx, dim_name in enumerate(engine.dim_item_ranges.keys()):
                d_score = engine.calculate_single_dimension_score(dim_name, filtered_df)
                t_col = grid_c1 if idx % 3 == 0 else (grid_c2 if idx % 3 == 1 else grid_c3)
                with t_col: render_kpi_card(f"{dim_name}", f"{d_score:.2f}%", "Skor Tertapis Masa Nyata", tier=engine.get_tier(d_score))

    # --- TAB 5: AMARAN ITEM STRESSOR (TERPENAPIS MASA NYATA) ---
    with tabs[4]:
        st.subheader("🚨 Pengesanan Awal: 5 Indikator Utama Paling Tegang (Stressor Kluster)")
        item_scores = engine.calculate_item_scores(filtered_df)
        if item_scores:
            sorted_items = sorted(item_scores.items(), key=lambda x: x[1]['mean'], reverse=True)[:5]
            for rank, (code, v_metrics) in enumerate(sorted_items):
                stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == code]['Statement'].values[0]
                d_name = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == code]['Dimension'].values[0]
                item_pct = ((v_metrics['mean'] - 1) / 4) * 100
                st.markdown(f"#### 🛑 Kedudukan #{rank+1}: {code} — [Indeks Ketegangan Kluster: {item_pct:.1f}%]")
                st.markdown(f"**Dimensi Terikat:** {d_name} | **Pernyataan Soalan Isu:** *{stmt}*")
                st.markdown("---")

    # --- TAB 6: SENTIMEN NLP KUALITATIF ---
    with tabs[5]:
        st.subheader("💬 Suara Marhaen: Analisis Klasifikasi Tema & Sentimen NLP Teks Rakyat")
        st.info("Pencidukan ulasan kualitatif siber mengikut pilihan tapisan geokomposit.")

    # --- TAB 7: ANALISIS TEORETIKAL ---
    with tabs[6]:
        st.subheader("🧠 Pusat Interpretasi Psikometrik & Analisis Penumpuan Teori-Data")
        st.info("Pemodelan indeks strain Tajfel (Social Identity), Gurr (Relative Deprivation) bersandarkan parameter kluster ditapis.")

    # --- TAB 08: PAIN POINTS (TERPENAPIS MASA NYATA) ---
    with tabs[7]:
        st.subheader("⚠️ Pengelasan Petunjuk Titik Kelemahan Struktur (Pain Points)")
        st.markdown("##### 📍 Pengesanan Rantaian Lokasi Berstruktur Penuh (Zon &rarr; Negeri &rarr; Daerah &rarr; Lokaliti)")
        if not geo_means_main.empty:
            rank_pp = 1
            for (zn, st_n, ds_n, ur_n), v_val in geo_means_main.items():
                pct_v = ((v_val - 1) / 4) * 100
                if 40.0 <= pct_v < 60.0:
                    sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                    sub_item = sub_df[items_list_main].mean().idxmax()
                    sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                    st.markdown(f"<div class='loc-card-premium' style='border-left-color: #DB2777;'><b>📍 LOKASI #{rank_pp}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>* Skor Ketegangan: {pct_v:.2f}%<br>* 🔍 Stressor: Item {sub_item} &rarr; <i>\"{sub_stmt}\"</i></div>", unsafe_allow_html=True)
                    rank_pp += 1
            if rank_pp == 1: st.info("Tiada lokasi di bawah kluster tapisan semasa yang berada dalam julat Pain Point (40%-59%).")

    # --- TAB 09: TENSION POINTS (TERPENAPIS MASA NYATA) ---
    with tabs[8]:
        st.subheader("🔥 Kerangka Eskalasi Indikator Titik Ketegangan (Tension Points)")
        st.markdown("##### 📍 Pengesanan Rantaian Lokasi Berstruktur Penuh (Zon &rarr; Negeri &rarr; Daerah &rarr; Lokaliti)")
        if not geo_means_main.empty:
            rank_tp = 1
            for (zn, st_n, ds_n, ur_n), v_val in geo_means_main.items():
                pct_v = ((v_val - 1) / 4) * 100
                if 60.0 <= pct_v < 80.0:
                    sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                    sub_item = sub_df[items_list_main].mean().idxmax()
                    sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                    st.markdown(f"<div class='loc-card-premium' style='border-left-color: #F59E0B;'><b>📍 LOKASI #{rank_tp}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>* Skor Ketegangan: {pct_v:.2f}%<br>* 🔍 Stressor: Item {sub_item} &rarr; <i>\"{sub_stmt}\"</i></div>", unsafe_allow_html=True)
                    rank_tp += 1
            if rank_tp == 1: st.info("Tiada lokasi di bawah kluster tapisan semasa yang berada dalam julat Tension Point (60%-79%).")

    # --- TAB 10: AMARAN HOTSPOT (TERPENAPIS MASA NYATA) ---
    with tabs[9]:
        st.subheader("🚨 Early Warning System (EWS) — Sempadan Amaran Hotspot Kritikal")
        st.markdown("##### 📍 Rantaian Lokasi Hotspot Paling Kritikal (EWS Emergency Trigger)")
        if not geo_means_main.empty:
            rank_hs = 1
            for (zn, st_n, ds_n, ur_n), v_val in geo_means_main.items():
                pct_v = ((v_val - 1) / 4) * 100
                if pct_v >= 80.0:
                    sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                    sub_item = sub_df[items_list_main].mean().idxmax()
                    sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                    st.markdown(f"<div class='loc-card-premium' style='border-left-color: #EF4444; background-color: #FEF2F2;'><b style='color: #DC2626;'>💥 CRITICAL ZON #{rank_hs}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>* Skor Ketegangan EWS: {pct_v:.2f}%<br>* 🛑 Stressor: Item {sub_item} &rarr; <i>\"{sub_stmt}\"</i></div>", unsafe_allow_html=True)
                    rank_hs += 1
            if rank_hs == 1: st.info("✓ Bersyukur, tiada zon bahaya amaran merah (&ge;80%) dikesan di dalam kluster tapisan geografi semasa.")

    # --- TAB 11: STRATEGI INTERVENSI ---
    with tabs[10]:
        st.subheader("💡 Enjin Pemetaan Strategi Intervensi Dasar Agensi Kabinet")
        if engine.intervention_library is not None:
            int_df = engine.intervention_library
            c_sel1, c_sel2 = st.columns(2)
            with c_sel1: chosen_dim = st.selectbox("1. Pilih Dimensi Ketegangan Utama", sorted(int_df['Dimension'].dropna().unique().tolist()), key="int_dim_sel")
            filtered_sub_df = int_df[int_df['Dimension'] == chosen_dim]
            with c_sel2: chosen_prob = st.selectbox("2. Pilih Isu / Masalah Spesifik Akar Umbi", sorted(filtered_sub_df['Subdimension'].dropna().unique().tolist()), key="int_prob_sel")
            final_policy = filtered_sub_df[filtered_sub_df['Subdimension'] == chosen_prob]
            
            if not final_policy.empty:
                agency_mapping_context = {
                    "MOF": {"PBT": "Menyelaras pelepasan dana kebajikan daerah sasar", "Swasta": "Melaksanakan pelarasan gaji progresif pekerja B40", "Komuniti": "Pengagihan kad bantuan bakul makanan digital"},
                    "UNITY": {"PBT": "Mengaktifkan Jawatankuasa Perpaduan Daerah (JPD)", "Swasta": "Menaja modul latihan kepelbajaaan korporat", "Komuniti": "Mobilisasi Kawasan Rukun Tangga (KRT)"}
                }
                for idx, row in final_policy.iterrows():
                    current_lead = row.get('Agency', 'N/A')
                    context_data = agency_mapping_context.get(current_lead, {"PBT": "Menyelaras operasi municipal", "Swasta": "Sokongan komersial", "Komuniti": "Mobilisasi akar umbi"})
                    st.markdown(f"""
                    <div class='loc-card-premium' style='border-left-color: #1E40AF; padding: 25px;'>
                        <h4>🏛️ Agensi Peneraju Kabinet: {current_lead}</h4>
                        <p><b>Program Modul:</b> {row.get('Intervention_Name', 'N/A')}</p>
                        <p><b>Deskripsi:</b> {row.get('Description', 'N/A')}</p>
                        <hr style='border-top:1px dashed #CBD5E1;'>
                        <ul style='font-size:13px; color:#334155;'>
                            <li><b>🏢 Peranan Swasta:</b> {context_data['Swasta']}</li>
                            <li><b>🏘️ Peranan PBT / Majlis Daerah:</b> {context_data['PBT']}</li>
                            <li><b>👥 Peranan Komuniti / RT:</b> {context_data['Komuniti']}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

    # --- TAB 12: MEDIA SCRAPING ---
    with tabs[11]:
        st.subheader("📰 Papan Pemantauan Media Cetak & Aliran Sentimen Siber Digital")
        if engine.media_issue_summary is not None:
            m_df = engine.media_issue_summary
            display_media = m_df.copy()
            if sel_state: display_media = display_media[display_media['State'].isin(sel_state)]
            for idx, row in display_media.head(5).iterrows():
                st.markdown(f"🔹 **Tarikh: {row.get('Date','N/A')} | Platform: {row.get('Source','N/A')} | Wilayah: {row.get('State','N/A')}**\n* 💬 Rumusan Siber: \"{row.get('Summary','N/A')}\"")

    # --- TAB 13: DAPATAN FGD ---
    with tabs[12]:
        st.subheader("👥 Transkrip Consensus Panel Pakar & Dapatan Bengkel FGD")
        if engine.fgd_expert is not None:
            st.plotly_chart(px.bar(engine.fgd_expert['Priority'].value_counts(), title="Matriks Kalibrasi Panel Pakar Kebangsaan"), use_container_width=True)

    # --- TAB 14: REPORT GENERATOR HTML (TERPENAPIS SEBENARNYA MERENTAS 20+ HALAMAN MUKTAMAD) ---
    with tabs[13]:
        st.subheader("📄 Penjanaan HTML Briefing Dossier Berasaskan Kluster Ditapis")
        rep_title = st.text_input("Tajuk Laporan Eksekutif JPM", "Laporan Hasil Kajian Pembangunan Indeks Ketegangan Masyarakat Malaysia (IKMM) Bagi Kelulusan Jemaah Menteri 2026")
        rep_officer = st.text_input("Nama Pegawai Pelapor Muktamad", "Dato' Sri Ketua Pengarah JPNIN")
        rep_branch = st.text_input("Bahagian / Agensi Utama", "Kluster Analitik Risiko & Pemetaan Polisi Strategik Perpaduan")
        if st.button("Kompilasikan Dokumen Laporan Kluster Terpenapis", use_container_width=True):
            if sub_total > 0:
                html_code = engine.generate_html_dossier_report(rep_title, rep_officer, rep_branch, filtered_df)
                st.success("✓ Dokumen Dossier Kabinet Berjaya Dikompilasikan Spesifik Mengikut Parameter Tapisan Geografi Sidebar Anda!")
                st.download_button("⬇ Muat Turun Fail Laporan Dossier Terpenapis (.html)", html_code, "IKMM_Filtered_Dossier_2026.html", "text/html", use_container_width=True)
            else:
                st.error("Ralat: Tidak boleh menjana laporan bagi data kosong (0 responden). Sila ubah tapisan anda.")
            
    with tabs[14]:
        st.subheader("🔎 Advanced Database Structural Cell Matrix Explorer")
        st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
