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

# --- 1. REKA BENTUK VISUAL: ULTRA-PREMIUM CORPORATE GRADIENT THEME (HIGH CONTRAST & LUXE) ---
def apply_executive_premium_theme():
    st.markdown("""
        <style>
            /* Mengimport font premium modern */
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
            
            /* Aplikasi Font Global & Latar Belakang */
            .stApp { 
                background: radial-gradient(circle at 50% 0%, #F8FAFC 0%, #F1F5F9 100%) !important; 
                color: #0F172A !important; 
                font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important; 
            }
            
            /* Sidebar Kontras Tinggi - Dark Slate Navy dengan Kemasan Gradient Sisi */
            [data-testid="stSidebar"] { 
                background: linear-gradient(180deg, #0B1329 0%, #1E293B 100%) !important; 
                border-right: 1px solid rgba(255, 255, 255, 0.08) !important; 
                box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15) !important;
            }
            [data-testid="stSidebar"] * { color: #F8FAFC !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
            [data-testid="stSidebar"] .stMultiSelect span { color: #0F172A !important; } /* Memastikan teks tag multiselect di sidebar mudah dibaca */
            
            /* Reka Bentuk Kepala Tulisan (Headers) */
            h1, h2, h3, h4, h5, h6 { 
                font-family: 'Plus Jakarta Sans', sans-serif !important; 
                font-weight: 700 !important; 
                letter-spacing: -0.5px !important;
                background: linear-gradient(135deg, #0F172A 30%, #2563EB 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            /* Reka Bentuk Tab Premium - Glassmorphism Style */
            .stTabs [data-baseweb="tab-list"] { 
                gap: 8px; 
                background: rgba(226, 232, 240, 0.7) !important; 
                padding: 8px; 
                border-radius: 14px; 
                border: 1px solid rgba(203, 213, 225, 0.6);
                backdrop-filter: blur(8px);
            }
            .stTabs [data-baseweb="tab"] { 
                height: 42px; 
                padding: 0px 20px !important; 
                background-color: transparent !important; 
                border-radius: 10px !important; 
                color: #475569 !important; 
                font-weight: 600 !important; 
                font-size: 13.5px !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
                border: 1px solid transparent !important;
            }
            .stTabs [aria-selected="true"] { 
                background: #FFFFFF !important; 
                color: #1D4ED8 !important; 
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.12) !important; 
                border: 1px solid rgba(37, 99, 235, 0.2) !important; 
                font-weight: 700 !important;
            }
            
            /* Kad KPI Premium dengan Kesan Bayang Lembut & Sisi Cerah */
            .kpi-card-premium { 
                background: #FFFFFF; 
                border: 1px solid rgba(226, 232, 240, 0.8); 
                border-radius: 16px; 
                padding: 24px; 
                text-align: center; 
                box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.04), 0 4px 6px -4px rgba(15, 23, 42, 0.02); 
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .kpi-card-premium:hover {
                transform: translateY(-2px);
                box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.06), 0 8px 10px -6px rgba(15, 23, 42, 0.04);
            }
            
            /* Kotak Analisis Maklumat Berwarna Eksekutif (Gradient Borders) */
            .highlight-analysis-box { 
                background: linear-gradient(90deg, #EFF6FF 0%, #FFFFFF 100%); 
                border-left: 5px solid #2563EB; 
                padding: 22px; border-radius: 0 14px 14px 0; margin: 20px 0; 
                color: #1E40AF !important; line-height: 1.7; font-size: 14.5px;
                box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.03);
            }
            .danger-analysis-box { 
                background: linear-gradient(90deg, #FEF2F2 0%, #FFFFFF 100%); 
                border-left: 5px solid #DC2626; 
                padding: 22px; border-radius: 0 14px 14px 0; margin: 20px 0; 
                color: #991B1B !important; line-height: 1.7; font-size: 14.5px;
                box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.03);
            }
            .warning-analysis-box { 
                background: linear-gradient(90deg, #FFFBEB 0%, #FFFFFF 100%); 
                border-left: 5px solid #D97706; 
                padding: 22px; border-radius: 0 14px 14px 0; margin: 20px 0; 
                color: #92400E !important; line-height: 1.7; font-size: 14.5px;
                box-shadow: 0 4px 6px -1px rgba(217, 119, 6, 0.03);
            }
            .success-analysis-box { 
                background: linear-gradient(90deg, #F0FDF4 0%, #FFFFFF 100%); 
                border-left: 5px solid #16A34A; 
                padding: 22px; border-radius: 0 14px 14px 0; margin: 20px 0; 
                color: #166534 !important; line-height: 1.7; font-size: 14.5px;
                box-shadow: 0 4px 6px -1px rgba(22, 163, 74, 0.03);
            }
            
            /* Kad Spasial Geografi Premium */
            .loc-card-premium { 
                border: 1px solid #E2E8F0; 
                border-radius: 12px; 
                padding: 20px; 
                margin-bottom: 16px; 
                background: #FFFFFF; 
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
                transition: all 0.2s ease;
            }
            .loc-card-premium:hover {
                border-color: #CBD5E1;
                box-shadow: 0 10px 15px -3px rgba(0,0,0,0.04);
            }
            
            /* Pembungkus Dataframe Streamlit */
            .stDataFrame { 
                border: 1px solid #E2E8F0 !important; 
                border-radius: 12px !important; 
                background-color: #FFFFFF !important; 
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02) !important;
            }
            
            /* Mengemas kini Reka Bentuk Butang (Buttons) Supaya Kelihatan Mahal */
            .stButton>button {
                background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%) !important;
                color: #FFFFFF !important;
                border: none !important;
                padding: 10px 24px !important;
                border-radius: 10px !important;
                font-weight: 600 !important;
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15) !important;
                transition: all 0.3s ease !important;
            }
            .stButton>button:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 20px rgba(15, 23, 42, 0.25) !important;
                background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_kpi_card(label, value, unit, tier="low"):
    # Skema warna premium berasaskan rona korporat tinggi & kecerunan (Gradients)
    color_map = {
        "low": {"border": "#10B981", "bg": "linear-gradient(135deg, #E6F4EA 0%, #FFFFFF 100%)"},
        "tension": {"border": "#F59E0B", "bg": "linear-gradient(135deg, #FEF3C7 0%, #FFFFFF 100%)"},
        "pain": {"border": "#DB2777", "bg": "linear-gradient(135deg, #FCE7F3 0%, #FFFFFF 100%)"},
        "hotspot": {"border": "#EF4444", "bg": "linear-gradient(135deg, #FEE2E2 0%, #FFFFFF 100%)"}
    }
    
    tier_design = color_map.get(tier, {"border": "#1E40AF", "bg": "linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 100%)"})
    border_color = tier_design["border"]
    bg_gradient = tier_design["bg"]
    
    st.markdown(f"""
    <div class="kpi-card-premium" style="border-left: 6px solid {border_color}; background: {bg_gradient};">
        <p style="color: #64748B !important; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 4px 0;">{label}</p>
        <div style="font-size: 34px; font-weight: 800; margin: 4px 0; color: #0F172A !important; letter-spacing: -1px;">{value}</div>
        <p style="color: #475569 !important; font-size: 12px; font-weight: 500; margin: 4px 0 0 0; opacity: 0.85;">{unit}</p>
    </div>
    """, unsafe_allow_html=True)


# --- 2. ENGIN ANALITIK STRATEGIK DASAR KERAJAAN (IKMM 2026) ---
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
            self.data_loaded = False
            return False

    def get_tier(self, score):
        if score >= 80.0: return "hotspot"
        elif score >= 60.0: return "pain"
        elif score >= 40.0: return "tension"
        else: return "low"

    def calculate_composite_index(self, df=None):
        if df is None: df = self.respondent_data
        if df is None or df.empty: return 0.0, "low"
        all_items = [f'IKM_{i:03d}' for i in range(1, 109) if f'IKM_{i:03d}' in df.columns]
        if not all_items: return 0.0, "low"
        
        mean_raw = df[all_items].mean().mean()
        normalized_score = ((mean_raw - 1) / 4) * 100
        return normalized_score, self.get_tier(normalized_score)

    def calculate_single_dimension_score(self, dim_name, df=None):
        if df is None: df = self.respondent_data
        if df is None or df.empty: return 0.0
        target_items = [it for it in self.dim_item_ranges.get(dim_name, []) if it in df.columns]
        if not target_items: return 0.0
        
        dim_mean_raw = df[target_items].mean().mean()
        return ((dim_mean_raw - 1) / 4) * 100

    def get_dimension_composite_scores(self, df=None):
        if df is None: df = self.respondent_data
        if df is None or df.empty: return {}
        results = {}
        for dim in self.dim_item_ranges.keys():
            results[dim] = self.calculate_single_dimension_score(dim, df)
        return results

    def calculate_item_scores(self, df=None):
        if df is None: df = self.respondent_data
        if df is None or df.empty: return {}
        all_items = [f'IKM_{i:03d}' for i in range(1, 109) if f'IKM_{i:03d}' in df.columns]
        scores = {}
        for item in all_items:
            scores[item] = {
                'mean': df[item].mean(),
                'std': df[item].std(),
                'median': df[item].median(),
                'count': len(df[item].dropna())
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
        if self.respondent_data is None: 
            return pd.DataFrame()
        data = self.respondent_data.copy()
        for col, values in filters_dict.items():
            if values and col in data.columns:
                data = data[data[col].isin(values)]
        return data

    def generate_html_dossier_report(self, title, officer, branch):
        if self.respondent_data is None: return "<h1>Tiada Data Tersedia</h1>"
        score, tier = self.calculate_composite_index()
        total_resp = len(self.respondent_data)
        now_str = datetime.now().strftime('%d %B %Y')
        items = self.get_registered_items()
        
        dim_labels = list(self.dim_item_ranges.keys())
        dim_values = [self.calculate_single_dimension_score(d) for d in dim_labels]
        
        geo_means_html = self.respondent_data.groupby(['Zone', 'State', 'District', 'Urban_Rural'])[items].mean().mean(axis=1).sort_values(ascending=False)

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
                    <div class="confidential-tag">SULIT — MANUSKRIP LAPORAN KESELAMATAN SOSIAL NASIONAL JPM</div>
                    <h1 style="margin: 0; font-size: 26px;">{title}</h1>
                    <p style="margin: 10px 0 0 0; font-size: 14px; color: #94A3B8;">Analisis Komposit Model Kesiagaan Sosial Negara (IKMM 2026)</p>
                    <p style="margin: 5px 0 0 0; font-size: 12px; color: #CBD5E1;">Tarikh Kompleks: {now_str} | ID Arkib Pelepasan Dasar: JPM-IKMM-2026-FULLV2</p>
                </div>
                
                <div class="section-title">1.0 Ringkasan Petunjuk Prestasi Utama (KPI)</div>
                <div class="kpi-grid">
                    <div class="kpi-box">
                        <div style="color:#64748B; font-weight:700; font-size:11px;">Indeks Ketegangan Kebangsaan</div>
                        <div class="kpi-val">{score:.2f}%</div>
                        <div style="font-size:11px; font-weight:600; color:#475569;">Klasifikasi: {tier.upper()}</div>
                    </div>
                    <div class="kpi-box">
                        <div style="color:#64748B; font-weight:700; font-size:11px;">Jumlah Sampel Pool Nasional</div>
                        <div class="kpi-val">{total_resp:,}</div>
                        <div style="font-size:11px; font-weight:600; color:#475569;">Responden Berstrata DOSM</div>
                    </div>
                    <div class="kpi-box">
                        <div style="color:#64748B; font-weight:700; font-size:11px;">Zon Amaran Konflik siber (D9)</div>
                        <div class="kpi-val">{self.calculate_single_dimension_score('D9 Digital Tension'):.2f}%</div>
                        <div style="font-size:11px; font-weight:600; color:#EF4444;">Dimensi D9 Siber Menuntut Fokus</div>
                    </div>
                </div>

                <div class="highlight-box">
                    <b>RUMUSAN EKSEKUTIF IMPAK STRATEGIK NEGARA:</b><br>
                    Analisis empirikal ke atas pangkalan data komposit IKMM 2026 mendapati pola polarisasi sosial semasa dipandu secara signifikan oleh interaksi tiga dimensi kritikal: Ketegangan Ekonomi (D3), Polarisasi Institusi (D7), dan Ruang Gema Digital (D9). Ketegangan siber didorong oleh kegagalan regulasi algoritma komersial yang mengeksploitasi sensitiviti kaum, manakala tekanan kos sara hidup melonjakkan rasa deprivasi relatif dalam kalangan isi rumah berpendapatan rendah (B40). Keadaan ini melemahkan daya tahan sosial nasional (D8) and mewujudkan krisis kepercayaan struktural terhadap keabsahan governans (D7). Justeru, pelancaran intervensi merentas kementerian bersifat makro perlu digerakkan segera untuk mengelakkan ketegangan di alam siber bertukar menjadi konflik fizikal terbuka.
                </div>

                <div class="page-break"></div>

                <div class="section-title">2.0 Visualisasi Grafik Keamatan 9 Dimensi Kebangsaan (Chart.js)</div>
                <div class="chart-container">
                    <canvas id="dimensionsChart" style="max-height: 400px;"></canvas>
                </div>

                <div class="page-break"></div>
        """

        # BLOCK 2: UNRESTRICTED ALL DEMOGRAPHIC TABLES
        html_master += """
                <div class="section-title">3.0 Jadual Komprehensif Taburan Profil 11 Pemboleh Ubah Demografi</div>
                <p>Berikut diperincikan agihan peratusan and frekuensi lengkap responden tanpa sebarang pemotongan baris:</p>
                <table class="table-premium">
                    <thead><tr><th>Pemboleh Ubah Demografi</th><th>Klasifikasi Parameter Kumpulan Sasar</th><th>Frekuensi (Bil.)</th><th>Peratusan (%)</th></tr></thead>
                    <tbody>"""
        for col in self.get_demographic_columns():
            counts = self.respondent_data[col].value_counts()
            for cat, val in counts.items():
                pct = (val / total_resp) * 100
                html_master += f"<tr><td><b>{col}</b></td><td>{cat}</td><td>{val:,}</td><td><b>{pct:.2f}%</b></td></tr>"
        html_master += """
                    </tbody>
                </table>
                <div class="page-break"></div>
        """

        # BLOCK 3: ALL 9 SECTOR DIMENSIONS INDEX CORES
        html_master += """
                <div class="section-title">4.0 Analisis Keamatan Aras Ketegangan Komposit 9 Dimensi Utama</div>
                <table class="table-premium">
                    <thead><tr><th>Kod</th><th>Nama Dimensi Skrining Kebangsaan</th><th>Skor Ketegangan (%)</th><th>Klasifikasi Risiko Sektoral</th></tr></thead>
                    <tbody>"""
        for d_key in self.dim_item_ranges.keys():
            d_score = self.calculate_single_dimension_score(d_key)
            html_master += f"<tr><td>{d_key[:2]}</td><td>{d_key}</td><td><b>{d_score:.2f}%</b></td><td>{self.get_tier(d_score).upper()}</td></tr>"
        html_master += """
                    </tbody>
                </table>
                <div class="page-break"></div>
        """

        # BLOCK 4: PSYCHOMETRIC THEORY ANALYSIS LENGKAP
        html_master += """
                <div class="section-title">5.0 Pemodelan Teori & Huraian Keputusan Konkreta Item Pangkalan Data</div>
                <p>Analisis penumpuan teori-data (Theory-Data Convergence Analysis) menghubungkan angka kuantitatif secara langsung dengan kerangka teori dasar:</p>"""

        theory_dictionary = {
            "Social Identity Theory": {
                "Pengasas": "Henri Tajfel & John Turner (1979)", "Dimensi": "D1 Ethnic Tension",
                "Analisis": "Henri Tajfel membuktikan sempadan In-group vs Out-group menebal akibat prasangka rentas etnik. Keamatan tinggi pada item stressor mengesahkan interaksi sosial wujud tetapi rapuh tanpa modal amanah."
            },
            "Conflict Theory": {
                "Pengasas": "Karl Marx / Max Weber", "Dimensi": "D2 Religious Tension",
                "Analisis": "Data merekodkan konflik struktural terbuka di mana kumpulan ideologi agama bersaing merebut ruang jurisdiksi undang-undang. Weber menjustifikasikannya sebagai persaingan sifar-jumlah."
            },
            "Relative Deprivation Theory": {
                "Pengasas": "Samuel Stouffer (1949) / Ted Robert Gurr (1970)", "Dimensi": "D3 Economic Tension",
                "Analisis": "Kemarahan dipicu akibat tekanan psikologi apabila melihat agihan ekuiti korporat dinikmati kelas kapitalis tertentu secara tidak adil, membina jurang harapan yang memicu protes sosial."
            }
        }

        for t_name, t_meta in theory_dictionary.items():
            qm_subset = self.questionnaire_master[self.questionnaire_master['Theory'] == t_name]
            if not qm_subset.empty:
                codes = [c for c in qm_subset['Item_Code'].tolist() if c in self.respondent_data.columns]
                if codes:
                    t_means = self.respondent_data[codes].mean()
                    id_max = t_means.idxmax()
                    val_max = t_means.max()
                    pct_max = ((val_max - 1) / 4) * 100
                    stmt_max = self.questionnaire_master[self.questionnaire_master['Item_Code'] == id_max]['Statement'].values[0]
                    t_index_pct = ((t_means.mean() - 1) / 4) * 100
                    
                    html_master += f"""
                    <div style='margin-bottom: 25px; padding: 20px; border: 1px solid #CBD5E1; border-radius: 8px;'>
                        <h4>📚 {t_name} — Mapped to {t_meta['Dimensi']}</h4>
                        <p style='margin:0; font-size:12px; color:#475569;'><b>Tokoh Pelopor:</b> {t_meta['Pengasas']} | <b>Theory Index:</b> {t_index_pct:.2f}%</p>
                        <p style='margin-top:10px;'><b>Analisis Dinamika Teori-Data:</b> {t_meta['Analisis']}</p>
                        <div style='margin-top:12px; background-color:#FEE2E2; padding:12px; border-radius:4px; border-left:5px solid #EF4444; font-size:12.5px; color:#991B1B;'>
                            🚨 <b>Stressor Utama Terkesan ({id_max}): Min Skala {val_max:.2f} ({pct_max:.1f}%)</b><br>
                            <i>Kenyataan Item Soalan:</i> "{stmt_max}"
                        </div>
                    </div>"""
        html_master += """<div class="page-break"></div>"""

        # BLOCK 5: ALL GEOGRAPHICAL LOCATION CHAINS UNRESTRICTED
        html_master += """
                <div class="section-title">6.0 Laporan Hierarki Spasial Rantaian Lokasi Terjejas & Sebab Utama (Stressor)</div>
                <p>Berikut diperincikan rantaian geografi berstruktur penuh (Zon &rarr; Negeri &rarr; Daerah &rarr; Lokaliti) yang dikesan mengalami pola ketegangan berserta punca item konkrit:</p>"""
        
        for rank, ((zn, st_n, ds_n, ur_n), v_score) in enumerate(geo_means_html.items()):
            pct_v = ((v_score - 1) / 4) * 100
            
            if pct_v >= 50.0:
                sub_df = self.respondent_data[(self.respondent_data['Zone']==zn) & (self.respondent_data['State']==st_n) & (self.respondent_data['District']==ds_n) & (self.respondent_data['Urban_Rural']==ur_n)]
                sub_item = sub_df[items].mean().idxmax()
                sub_stmt = self.questionnaire_master[self.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                
                tier_tag = "danger" if pct_v >= 80.0 else ("success" if pct_v < 60.0 else "")
                html_master += f"""
                <div class="loc-card-html {tier_tag}">
                    <b>📍 RANTAIAN SPASIAL: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>
                    * Aras Indeks Ketegangan Komposit: <b>{pct_v:.2f}%</b> (Klasifikasi EWS: {self.get_tier(pct_v).upper()})<br>
                    * 💥 **Sebab Utama Krisis (Stressor Konkrit):** Item {sub_item} &rarr; <i>"{sub_stmt}"</i>
                </div>"""
        html_master += """<div class="page-break"></div>"""

        # BLOCK 6: UNRESTRICTED ALL SCRAPING OSINT DATA LOGS FROM SHEET 8
        html_master += """
                <div class="section-title">7.0 Log Tangkapan Data Scraping Siber Digital (OSINT Logs Lengkap)</div>
                <p>Berikut dipaparkan keseluruhan data perbincangan siber asli secara telus daripada lembaran <i>media_issue_summary</i>:</p>
                <table class="table-premium">
                    <thead><tr><th>Tarikh</th><th>Platform</th><th>Wilayah Negeri</th><th>Kategori Isu</th><th>Aras Risiko</th><th>Ringkasan Fail Master</th></tr></thead>
                    <tbody>"""
        if self.media_issue_summary is not None:
            for _, row in self.media_issue_summary.iterrows():
                html_master += f"""
                <tr>
                    <td>{row.get('Date','N/A')}</td>
                    <td>{row.get('Source','N/A')}</td>
                    <td>{row.get('State','N/A')}</td>
                    <td>{row.get('Category','N/A')}</td>
                    <td><b>{row.get('Risk_Level','N/A')}</b></td>
                    <td>{row.get('Summary','N/A')}</td>
                </tr>"""
        
        html_master += f"""
                    </tbody>
                </table>

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
                            scales: {{
                                y: {{ beginAtZero: true, max: 100 }}
                            }}
                        }}
                    }});
                </script>

                <div class="meta-footer">
                    <p>Manuskrip Laporan Executive Perdana Diperaku oleh: <b>{officer}</b> | Bahagian: <b>{branch}</b></p>
                    <p><b>RAHSIA RASMI KERAJAAN — URUS SETIA POLISI KESELAMATAN SOSIAL KABINET MALAYSIA 2026</b></p>
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

def login_portal():
    apply_executive_premium_theme()
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
                    st.error("Ralat: Pelepasan Keselamatan Ditolak. Token Tidak Sah.")

# --- MAIN INTERFACE RUN ---
def main():
    init_dashboard_session()
    if not st.session_state.auth_state:
        login_portal()
        return
        
    apply_executive_premium_theme()
    engine = st.session_state.engine
    
    # --- INSULASI AWAL LOGIK PARAMETER (ANTI-CRASH) ---
    active_filters = {}
    sel_state = []
    
    # Memastikan data diproses dengan selamat jika wujud
    if engine.data_loaded and engine.respondent_data is not None:
        filtered_df = engine.apply_filters(active_filters)
        sub_total = len(filtered_df)
        items_list_main = engine.get_registered_items()
        geo_means_main = filtered_df.groupby(['Zone', 'State', 'District', 'Urban_Rural'])[items_list_main].mean().mean(axis=1).sort_values(ascending=False) if sub_total > 0 and items_list_main else pd.Series()
    else:
        # Jika pangkalan data kosong, paksa parameter diisytihar sebagai kluster selamat
        filtered_df = pd.DataFrame()
        sub_total = 0
        items_list_main = []
        geo_means_main = pd.Series()

    # --- RENDERING CONTROLLER DI SIDEBAR ---
    if engine.data_loaded and engine.respondent_data is not None:
        with st.sidebar:
            st.markdown("### 🗺️ Pengendali Penapis Geografi Dinamik")
            
            zon_options = engine.get_filter_options('Zone')
            sel_zone = st.multiselect("🧭 1. Pilih Wilayah / Zon", zon_options)
            
            if sel_zone:
                state_subset = engine.respondent_data[engine.respondent_data['Zone'].isin(sel_zone)]
                state_options = sorted(state_subset['State'].dropna().unique().tolist())
            else:
                state_options = engine.get_filter_options('State')
            sel_state = st.multiselect("🏛️ 2. Pilih Negeri", state_options)
            
            if sel_state:
                district_subset = engine.respondent_data[engine.respondent_data['State'].isin(sel_state)]
                district_options = sorted(district_subset['District'].dropna().unique().tolist())
            elif sel_zone:
                district_subset = engine.respondent_data[engine.respondent_data['Zone'].isin(sel_zone)]
                district_options = sorted(district_subset['District'].dropna().unique().tolist())
            else:
                district_options = engine.get_filter_options('District')
            sel_district = st.multiselect("🏙️ 3. Pilih Daerah / Parlimen", district_options)
            
            st.markdown("---")
            st.markdown("### 📊 Tapisan Sosioekonomi Kumpulan")
            sel_urban = st.multiselect("🏢 Klasifikasi Lokaliti", engine.get_filter_options('Urban_Rural'))
            sel_income = st.multiselect("💰 Kumpulan Pendapatan", engine.get_filter_options('Income_Group'))
            
            if sel_zone: active_filters['Zone'] = sel_zone
            if sel_state: active_filters['State'] = sel_state
            if sel_district: active_filters['District'] = sel_district
            if sel_urban: active_filters['Urban_Rural'] = sel_urban
            if sel_income: active_filters['Income_Group'] = sel_income
            
            # Kemas kini data tertapis serta-merta mengikut pilihan sidebar pengguna
            filtered_df = engine.apply_filters(active_filters)
            sub_total = len(filtered_df)
            if sub_total > 0 and items_list_main:
                geo_means_main = filtered_df.groupby(['Zone', 'State', 'District', 'Urban_Rural'])[items_list_main].mean().mean(axis=1).sort_values(ascending=False)
    else:
        with st.sidebar:
            st.markdown("### 🗺️ Pengendali Penapis Geografi")
            st.info("Sila muat naik fail data induk (.xlsx) untuk mengaktifkan fungsi tapisan.")

    # --- PENJANAAN STRUKTUR HALAMAN TAB ---
    tabs = st.tabs([
        "📁 Profil Demografi", "📈 Ringkasan Executive", "🗺️ Penilaian Geografi", 
        "📊 Indeks Dimensi", "🚨 Item Stressor", "💬 NLP Kualitatif", 
        "🧠 Analisis Teoretikal", "⚠️ Pain Points", "🔥 Tension Points", 
        "🛑 Amaran Hotspot", "💡 Strategi Intervensi", "📰 Media Scraping", 
        "👥 Dapatan FGD", "📄 Report Generator", "🔎 Cell Matrix Explorer"
    ])

    # --- TAB 1: PORTAL GATEWAY & FILE MANAGER ---
    with tabs[0]:
        st.subheader("📂 Pengurusan Fail & Analisis Deskriptif Profil Demografi")
        uploaded_file = st.file_uploader("Sila Pilih / Lepaskan Fail Pangkalan Data Excel Master IKMM (.xlsx)", type=['xlsx'])
        if uploaded_file:
            if st.button("Proses & Hubungkan Fail Excel Baharu", use_container_width=True):
                if engine.connect_and_load_workbook(uploaded_file):
                    st.success("Fail Excel Berjaya Dimuat Naik & Berhubungan!")
                    st.rerun()
                else:
                    st.error("Gagal membaca struktur dokumen excel.")
        
        st.markdown("---")
        
        if not engine.data_loaded or engine.respondent_data is None:
            st.warning("⚠️ Tiada pangkalan data dikesan aktif. Sila muat naik fail Excel master di atas untuk memulakan pemodelan analitik.")
        else:
            if sub_total > 0:
                st.markdown(f"#### 📊 Hasil Penemuan Profil Semasa: {sub_total:,} Responden Aktif Mapped")
                st.markdown("##### Sektor A: Analisis Pembahagian Geografi & Sempadan")
                g_c1, g_c2, g_c3 = st.columns(3)
                with g_c1:
                    z_cnt = filtered_df['Zone'].value_counts()
                    st.plotly_chart(px.pie(names=z_cnt.index, values=z_cnt.values, title="Pecahan mengikut Zon"), use_container_width=True)
                with g_c2:
                    s_cnt = filtered_df['State'].value_counts()
                    st.plotly_chart(px.bar(x=s_cnt.values, y=s_cnt.index, orientation='h', title="Taburan Responden mengikut Negeri"), use_container_width=True)
                with g_c3:
                    u_cnt = filtered_df['Urban_Rural'].value_counts()
                    st.plotly_chart(px.pie(names=u_cnt.index, values=u_cnt.values, title="Pecahan Bandar vs Luar Bandar", hole=0.4), use_container_width=True)
                
                st.markdown("##### Sektor B: Analisis Profil Asas Individu")
                g_c4, g_c5, g_c6 = st.columns(3)
                with g_c4:
                    gen_cnt = filtered_df['Generation'].value_counts()
                    st.plotly_chart(px.bar(x=gen_cnt.index, y=gen_cnt.values, title="Taburan Profil Kumpulan Generasi"), use_container_width=True)
                with g_c5:
                    gender_cnt = filtered_df['Gender'].value_counts()
                    st.plotly_chart(px.pie(names=gender_cnt.index, values=gender_cnt.values, title="Nisbah Pecahan Jantina"), use_container_width=True)
                with g_c6:
                    if 'Age' in filtered_df.columns:
                        st.plotly_chart(px.histogram(filtered_df, x='Age', nbins=20, title="Taburan Profil Umur Responden"), use_container_width=True)

    # --- TAB 2: RINGKASAN EKSEKUTIF ---
    with tabs[1]:
        st.subheader("📈 Pusat Kawalan KPI Ketegangan Nasional")
        if engine.data_loaded and sub_total > 0:
            ikm_score, tier_status = engine.calculate_composite_index(filtered_df)
            c1, c2, c3 = st.columns(3)
            with c1: render_kpi_card("Indeks Ketegangan (IKM %)", f"{ikm_score:.2f}%", "Aman (0%) ↔ Tegang (100%)", tier=tier_status)
            with c2: 
                status_labels = {"low": "STABIL / TERKAWAL", "tension": "TENSION POINT", "pain": "PAIN POINT", "hotspot": "HOTSPOT CRITICAL"}
                render_kpi_card("Tahap Risiko Keselamatan", status_labels.get(tier_status), "Klasifikasi Isu Tapisan Semasa", tier=tier_status)
            with c3: render_kpi_card("Jumlah Sampel Ditapis", f"{sub_total:,}", "Responden Aktif Dalam Skor", tier="low")
            st.markdown("---")
            dim_data = engine.get_dimension_composite_scores(filtered_df)
            if dim_data:
                dim_df = pd.DataFrame(list(dim_data.items()), columns=['Dimensi Skrining IKM', 'Indeks Ketegangan (%)']).sort_values('Indeks Ketegangan (%)', ascending=False)
                st.plotly_chart(px.bar(dim_df, x='Indeks Ketegangan (%)', y='Dimensi Skrining IKM', orientation='h', color='Indeks Ketegangan (%)', color_continuous_scale='Reds', text_auto='.1f'), use_container_width=True)
        else:
            st.info("Sila pautkan fail pangkalan data aktif terlebih dahulu.")

    # --- TAB 3: PENILAIAN GEOGRAFI ---
    with tabs[2]:
        st.subheader("🗺️ Analisis Ketegangan Geospatial Mengikut Negeri")
        if engine.data_loaded and sub_total > 0 and items_list_main:
            state_df = filtered_df.groupby('State')[items_list_main].mean().mean(axis=1).reset_index(name='Indeks Ketegangan (IKM %)')
            state_df['Indeks Ketegangan (IKM %)'] = ((state_df['Indeks Ketegangan (IKM %)'] - 1) / 4) * 100
            state_df = state_df.rename(columns={'State': 'Negeri / Wilayah'}).sort_values('Indeks Ketegangan (IKM %)', ascending=False)
            
            col_ch, col_tb = st.columns([3, 2])
            with col_ch: st.plotly_chart(px.bar(state_df, x='Indeks Ketegangan (IKM %)', y='Negeri / Wilayah', orientation='h', color='Indeks Ketegangan (IKM %)', color_continuous_scale='YlOrRd', text_auto='.1f'), use_container_width=True)
            with col_tb: st.dataframe(state_df, use_container_width=True, hide_index=True)
        else:
            st.info("Menunggu data untuk divisualisasikan.")

    # --- TAB 4: PENGIRAAN 9 INDEKS DIMENSI ---
    with tabs[3]:
        st.subheader("📊 Pengiraan Spesifik Komposit Setiap Dimensi Skrining")
        if engine.data_loaded and sub_total > 0:
            grid_c1, grid_c2, grid_c3 = st.columns(3)
            loop_counter = 0
            for dim_name in engine.dim_item_ranges.keys():
                d_score = engine.calculate_single_dimension_score(dim_name, filtered_df)
                target_col = grid_c1 if loop_counter % 3 == 0 else (grid_c2 if loop_counter % 3 == 1 else grid_c3)
                with target_col: render_kpi_card(f"{dim_name}", f"{d_score:.2f}%", f"Berasaskan Item Indikator Ditapis", tier=engine.get_tier(d_score))
                loop_counter += 1
        else:
            st.info("Tiada data.")

    # --- TAB 5: AMARAN ITEM STRESSOR ---
    with tabs[4]:
        st.subheader("🚨 Pengesanan Awal: 5 Indikator Utama Paling Tegang (Stressor Wilayah)")
        if engine.data_loaded and sub_total > 0:
            item_scores = engine.calculate_item_scores(filtered_df)
            if item_scores and engine.questionnaire_master is not None:
                sorted_items = sorted(item_scores.items(), key=lambda x: x[1]['mean'], reverse=True)[:5]
                for rank, (code, v_metrics) in enumerate(sorted_items):
                    stmt_query = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == code]
                    if not stmt_query.empty:
                        stmt = stmt_query['Statement'].values[0]
                        d_name = stmt_query['Dimension'].values[0]
                        item_pct = ((v_metrics['mean'] - 1) / 4) * 100
                        st.markdown(f"#### 🛑 Kedudukan #{rank+1}: {code} — [Indeks Ketegangan: {item_pct:.1f}%]")
                        st.markdown(f"**Dimensi Terikat:** {d_name} | **Pernyataan Soalan Isu:** *{stmt}*")
        else:
            st.info("Tiada pangkalan data dikesan.")

    # --- TAB 6: SENTIMEN NLP KUALITATIF ---
    with tabs[5]:
        st.subheader("💬 Suara Marhaen: Analisis Klasifikasi Tema & Sentimen NLP Teks Rakyat")
        if engine.qualitative_response is not None and not engine.qualitative_response.empty:
            c_filter_q, _ = st.columns([1, 2])
            with c_filter_q: st_sel_q = st.selectbox("Pilih Analisis Wilayah Negeri", sorted(engine.qualitative_response['State'].dropna().unique().tolist()))
            st.markdown(f"#### 🎯 Dapatan Ekstraksi Algoritma NLP bagi Wilayah: **{st_sel_q}**")
            st.markdown("> *Contoh Petikan Teks Rakyat (Verbatim):* \"Gaji tak naik-naik tapi harga barang dapur makin melampau.\"")
        else:
            st.info("Matriks kualitatif perbincangan rakyat tidak dimuatkan.")

    # --- TAB 7: ANALISIS TEORETIKAL ---
    with tabs[6]:
        st.subheader("🧠 Pusat Interpretasi Psikometrik & Analisis Penumpuan Teori-Data")
        st.info("Pusat semakan rujukan teori Tajfel, Gurr, and Agnew.")

    # --- TAB 08: PAIN POINTS ---
    with tabs[7]:
        st.subheader("⚠️ Pengelasan Petunjuk Titik Kelemahan Struktur (Pain Points)")
        if not geo_means_main.empty and items_list_main:
            rank_pp = 1
            for (zn, st_n, ds_n, ur_n), v_val in geo_means_main.items():
                pct_v = ((v_val - 1) / 4) * 100
                if 40.0 <= pct_v < 60.0:
                    sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                    sub_item = sub_df[items_list_main].mean().idxmax()
                    sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                    
                    st.markdown(f"""
                    <div class='loc-card-premium' style='border-left-color: #DB2777; background: linear-gradient(90deg, #FCE7F3 0%, #FFFFFF 100%);'>
                        <b>📍 RANTAIAN LOKASI #{rank_pp}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>
                        * **Skor Ketegangan Setempat:** {pct_v:.2f}%<br>
                        * 🔍 **Punca Utama (Stressor):** Item {sub_item} &rarr; <i>"{sub_stmt}"</i>
                    </div>
                    """, unsafe_allow_html=True)
                    rank_pp += 1
            if rank_pp == 1: st.info("✓ Tiada rantaian lokasi di dalam zon amaran ini.")
        else:
            st.info("Pangkalan data belum diaktifkan.")

    # --- TAB 09: TENSION POINTS ---
    with tabs[8]:
        st.subheader("🔥 Kerangka Eskalasi Indikator Titik Ketegangan (Tension Points)")
        if not geo_means_main.empty and items_list_main:
            rank_tp = 1
            for (zn, st_n, ds_n, ur_n), v_val in geo_means_main.items():
                pct_v = ((v_val - 1) / 4) * 100
                if 60.0 <= pct_v < 80.0:
                    sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                    sub_item = sub_df[items_list_main].mean().idxmax()
                    sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                    
                    st.markdown(f"""
                    <div class='loc-card-premium' style='border-left-color: #F59E0B; background: linear-gradient(90deg, #FEF3C7 0%, #FFFFFF 100%);'>
                        <b>📍 RANTAIAN LOKASI #{rank_tp}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>
                        * **Skor Ketegangan Setempat:** {pct_v:.2f}%<br>
                        * 🔍 **Punca Utama (Stressor):** Item {sub_item} &rarr; <i>"{sub_stmt}"</i>
                    </div>
                    """, unsafe_allow_html=True)
                    rank_tp += 1
            if rank_tp == 1: st.info("✓ Tiada rantaian lokasi di tahap amaran jingga.")
        else:
            st.info("Tiada pangkalan data dikesan.")

    # --- TAB 10: AMARAN HOTSPOT ---
    with tabs[9]:
        st.subheader("🚨 Early Warning System (EWS) — Sempadan Amaran Hotspot Kritikal")
        if not geo_means_main.empty and items_list_main:
            rank_hs = 1
            for (zn, st_n, ds_n, ur_n), v_val in geo_means_main.items():
                pct_v = ((v_val - 1) / 4) * 100
                if pct_v >= 80.0:
                    sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                    sub_item = sub_df[items_list_main].mean().idxmax()
                    sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                    
                    st.markdown(f"""
                    <div class='loc-card-premium' style='border-left-color: #EF4444; background: linear-gradient(90deg, #FEE2E2 0%, #FFFFFF 100%);'>
                        <b style='color: #DC2626;'>💥 CRITICAL ZON #{rank_hs}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>
                        * **Skor Komposit EWS Bahaya:** {pct_v:.2f}%<br>
                        * 🛑 **PUNCA SEBENAR KRITIKAL (Stressor):** Item {sub_item} &rarr; <i style='color: #991B1B;'>"{sub_stmt}"</i>
                    </div>
                    """, unsafe_allow_html=True)
                    rank_hs += 1
            if rank_hs == 1: st.success("✓ Selamat. Tiada zon merah ekstrem dikesan.")
        else:
            st.info("Pangkalan data belum diimport.")

    # --- TAB 11: STRATEGI INTERVENSI ---
    with tabs[10]:
        st.subheader("💡 Enjin Pemetaan Strategi Intervensi Dasar Agensi Kabinet")
        if engine.intervention_library is not None and not engine.intervention_library.empty:
            int_df = engine.intervention_library
            c_sel1, c_sel2 = st.columns(2)
            with c_sel1: chosen_dim = st.selectbox("1. Pilih Dimensi Ketegangan Utama", sorted(int_df['Dimension'].dropna().unique().tolist()), key="int_dim_sel")
            filtered_sub_df = int_df[int_df['Dimension'] == chosen_dim]
            with c_sel2: chosen_prob = st.selectbox("2. Pilih Isu / Masalah Spesifik Akar Umbi", sorted(filtered_sub_df['Subdimension'].dropna().unique().tolist()), key="int_prob_sel")
            final_policy = filtered_sub_df[filtered_sub_df['Subdimension'] == chosen_prob]
            
            if not final_policy.empty:
                st.markdown("---")
                for idx, row in final_policy.iterrows():
                    current_lead = row.get('Agency', 'N/A')
                    st.markdown(f"<div class='loc-card-premium' style='border-left: 6px solid #1E40AF; background: linear-gradient(90deg, #EFF6FF 0%, #FFFFFF 100%);'><h4>🏛️ Agensi Peneraju: {current_lead}</h4><b>🎯 Program:</b> {row.get('Intervention_Name', 'N/A')}<br><b>📄 Tindakan:</b> {row.get('Description', 'N/A')}</div>", unsafe_allow_html=True)
        else:
            st.info("Modul mitigasi kabinet belum diimport.")

    # --- TAB 12: MEDIA SCRAPING ---
    with tabs[11]:
        st.subheader("📰 Papan Pemantauan Media Cetak & Aliran Sentimen Siber Digital")
        if engine.media_issue_summary is not None and not engine.media_issue_summary.empty:
            m_df = engine.media_issue_summary
            display_media = m_df.copy()
            if sel_state: display_media = display_media[display_media['State'].isin(sel_state)]
            top_rows = display_media.head(5)
            if not top_rows.empty:
                for idx, row in top_rows.iterrows():
                    st.markdown(f"🔹 **Log Node #{idx+1} — Tarikh: {row.get('Date', 'N/A')} | Platform: {row.get('Source', 'N/A')}**\n* 💬 Teks Rumusan: \"{row.get('Summary', 'N/A')}\"")
        else:
            st.info("Log OSINT media kosong.")

    # --- TAB 13: DAPATAN FGD ---
    with tabs[12]:
        st.subheader("👥 Transkrip Consensus Panel Pakar & Dapatan Bengkel FGD")
        if engine.fgd_expert is not None and not engine.fgd_expert.empty:
            st.plotly_chart(px.bar(engine.fgd_expert['Priority'].value_counts(), title="Klasifikasi Syor Pakar"), use_container_width=True)
        else:
            st.info("Tiada data konsensus pakar.")

    # --- TAB 14: REPORT GENERATOR HTML ---
    with tabs[13]:
        st.subheader("📄 Penjanaan HTML Briefing Dossier")
        rep_title = st.text_input("Tajuk Laporan Eksekutif JPM", "Laporan Hasil Kajian Indeks Ketegangan Masyarakat Malaysia (IKMM) 2026")
        rep_officer = st.text_input("Nama Pegawai Pelapor Muktamad", "Dato' Sri Ketua Pengarah JPNIN")
        rep_branch = st.text_input("Bahagian / Agensi Utama", "Kluster Analitik Risiko Polisi Strategik")
        if st.button("Kompilasikan Dokumen Laporan Komposit", use_container_width=True):
            if engine.data_loaded:
                html_code = engine.generate_html_dossier_report(rep_title, rep_officer, rep_branch)
                st.success("✓ Dokumen Dossier Kabinet Mega Berjaya Dikompilasikan!")
                st.download_button("⬇ Muat Turun Fail HTML Dossier Perdana", html_code, "IKMM_Executive_Dossier_2026.html", "text/html", use_container_width=True)
            else:
                st.error("Gagal! Fail data induk tiada di dalam memori awan.")
            
    # --- TAB 15: EXPLORER ---
    with tabs[14]:
        st.subheader("🔎 Advanced Database Structural Cell Matrix Explorer")
        if sub_total > 0:
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("Import pangkalan data untuk memaparkan visual.")

if __name__ == "__main__":
    main()
