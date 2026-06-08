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

# --- 1. REKA BENTUK VISUAL: ULTRA-LUXE EXECUTIVE GRADIENT WITH ZERO-PADDING ---
def apply_executive_premium_theme():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
            
            .block-container {
                padding-top: 1.5rem !important;
                padding-bottom: 2rem !important;
                max-width: 95% !important;
            }
            [data-testid="stHeader"] {
                display: none !important;
            }
            
            .stApp { 
                background: radial-gradient(circle at 50% 0%, #F8FAFC 0%, #EFF6FF 100%) !important; 
                color: #0F172A !important; 
                font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important; 
            }
            
            .system-banner-premium {
                background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
                padding: 30px 40px;
                border-radius: 18px;
                box-shadow: 0 10px 30px rgba(37, 99, 235, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 30px;
                color: #FFFFFF !important;
                position: relative;
                overflow: hidden;
            }
            .system-banner-premium::after {
                content: '';
                position: absolute;
                top: -50%; right: -20%;
                width: 300px; height: 300px;
                background: rgba(255,255,255,0.03);
                border-radius: 50%;
            }
            .system-tag {
                background: linear-gradient(90deg, #EF4444 0%, #B91C1C 100%);
                color: white !important;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 800;
                border-radius: 30px;
                letter-spacing: 1.5px;
                display: inline-block;
                margin-bottom: 10px;
                box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3);
            }
            
            [data-testid="stSidebar"] { 
                background: linear-gradient(180deg, #0A0F1D 0%, #111827 100%) !important; 
                border-right: 1px solid rgba(255, 255, 255, 0.05) !important; 
                box-shadow: 5px 0 25px rgba(0, 0, 0, 0.2) !important;
            }
            [data-testid="stSidebar"] * { color: #F8FAFC !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
            [data-testid="stSidebar"] .stMultiSelect span { color: #0F172A !important; }
            
            h2, h3, h4, h5 { 
                font-family: 'Plus Jakarta Sans', sans-serif !important; 
                font-weight: 700 !important; 
                color: #0F172A !important;
                letter-spacing: -0.5px !important;
            }
            
            .stTabs [data-baseweb="tab-list"] { 
                gap: 8px; 
                background: rgba(15, 23, 42, 0.04) !important; 
                padding: 8px; 
                border-radius: 14px; 
                border: 1px solid rgba(15, 23, 42, 0.05);
                backdrop-filter: blur(10px);
            }
            .stTabs [data-baseweb="tab"] { 
                height: 44px; 
                padding: 0px 22px !important; 
                background-color: transparent !important; 
                border-radius: 10px !important; 
                color: #475569 !important; 
                font-weight: 600 !important; 
                font-size: 13.5px !important;
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); 
                border: 1px solid transparent !important;
            }
            .stTabs [aria-selected="true"] { 
                background: #FFFFFF !important; 
                color: #1D4ED8 !important; 
                box-shadow: 0 4px 14px rgba(37, 99, 235, 0.15) !important; 
                border: 1px solid rgba(37, 99, 235, 0.2) !important; 
                font-weight: 700 !important;
            }
            
            .kpi-card-premium { 
                background: #FFFFFF; 
                border: 1px solid rgba(226, 232, 240, 0.8); 
                border-radius: 16px; 
                padding: 26px; 
                text-align: center; 
                box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.04), 0 8px 10px -6px rgba(15, 23, 42, 0.02); 
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .kpi-card-premium:hover {
                transform: translateY(-4px);
                box-shadow: 0 20px 35px -5px rgba(15, 23, 42, 0.08), 0 12px 16px -6px rgba(15, 23, 42, 0.04);
            }
            
            .highlight-analysis-box { 
                background: linear-gradient(90deg, #EFF6FF 0%, #FFFFFF 100%); 
                border-left: 6px solid #2563EB; 
                padding: 24px; border-radius: 0 16px 16px 0; margin: 20px 0; 
                color: #1E40AF !important; line-height: 1.7; font-size: 14.5px;
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.04);
            }
            .danger-analysis-box { 
                background: linear-gradient(90deg, #FEF2F2 0%, #FFFFFF 100%); 
                border-left: 6px solid #DC2626; 
                padding: 24px; border-radius: 0 16px 16px 0; margin: 20px 0; 
                color: #991B1B !important; line-height: 1.7; font-size: 14.5px;
                box-shadow: 0 4px 12px rgba(220, 38, 38, 0.04);
            }
            
            .demo-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; margin: 25px 0; }
            .demo-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); transition: transform 0.2s; }
            .demo-card:hover { transform: translateY(-2px); }
            
            .card-blue h4 { color: #1E40AF; border-left: 4px solid #2563EB; padding-left: 8px; font-size: 14px; margin: 0 0 12px 0; text-transform: uppercase; }
            .card-purple h4 { color: #6D28D9; border-left: 4px solid #8B5CF6; padding-left: 8px; font-size: 14px; margin: 0 0 12px 0; text-transform: uppercase; }
            .card-amber h4 { color: #B45309; border-left: 4px solid #F59E0B; padding-left: 8px; font-size: 14px; margin: 0 0 12px 0; text-transform: uppercase; }
            .card-emerald h4 { color: #047857; border-left: 4px solid #10B981; padding-left: 8px; font-size: 14px; margin: 0 0 12px 0; text-transform: uppercase; }
            
            .table-premium { width: 100%; border-collapse: collapse; font-size: 13px; }
            .table-premium th { background: #1E293B; color: #FFFFFF; padding: 10px; text-align: left; font-weight: 600; font-size: 12px; }
            .table-premium td { padding: 9px 8px; border-bottom: 1px solid #F1F5F9; color: #334155; }
            .col-param { width: 60%; font-weight: 600; color: #111827; }
            .col-val { width: 18%; text-align: right; }
            .col-percent { width: 22%; text-align: right; font-weight: 700; color: #2563EB; }
            
            .badge-status { padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; text-align: center; display: inline-block; }
            .badge-hotspot { background: #FEE2E2; color: #EF4444; border: 1px solid rgba(239,68,68,0.2); }
            .badge-pain { background: #FCE7F3; color: #DB2777; border: 1px solid rgba(219,39,119,0.2); }
            .badge-tension { background: #FFFBEB; color: #D97706; border: 1px solid rgba(217,119,6,0.2); }
            .badge-low { background: #ECFDF5; color: #10B981; border: 1px solid rgba(16,185,129,0.2); }

            .loc-card-html { border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-bottom: 14px; background: #FFFFFF; box-shadow: 0 4px 10px rgba(0,0,0,0.01); }
            .loc-card-html.danger-zone { border-left: 6px solid #EF4444; background: linear-gradient(90deg, #FFF5F5 0%, #FFFFFF 100%); }
            .loc-card-html.warning-zone { border-left: 6px solid #F59E0B; background: linear-gradient(90deg, #FFFDF5 0%, #FFFFFF 100%); }
            
            .highlight-box { background: linear-gradient(90deg, #EFF6FF 0%, #F8FAFC 100%); border-left: 5px solid #3B82F6; padding: 22px; border-radius: 0 10px 10px 0; margin: 20px 0; font-size: 14px; color: #1E3A8A; font-weight: 500; }
            .page-break { page-break-before: always; }
            .meta-footer { margin-top: 50px; padding-top: 20px; border-top: 2px dashed #CBD5E1; text-align: center; font-size: 12px; color: #64748B; }
        </style>
    """, unsafe_allow_html=True)

def render_kpi_card(label, value, unit, tier="low"):
    color_map = {
        "low": {"border": "#10B981", "bg": "linear-gradient(135deg, #ECFDF5 0%, #FFFFFF 100%)"},
        "tension": {"border": "#F59E0B", "bg": "linear-gradient(135deg, #FFFBEB 0%, #FFFFFF 100%)"},
        "pain": {"border": "#DB2777", "bg": "linear-gradient(135deg, #FDF2F8 0%, #FFFFFF 100%)"},
        "hotspot": {"border": "#EF4444", "bg": "linear-gradient(135deg, #FEF2F2 0%, #FFFFFF 100%)"}
    }
    tier_design = color_map.get(tier, {"border": "#1E40AF", "bg": "linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 100%)"})
    st.markdown(f"""
    <div class="kpi-card-premium" style="border-left: 6px solid {tier_design['border']}; background: {tier_design['bg']};">
        <p style="color: #64748B !important; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin: 0 0 6px 0;">{label}</p>
        <div style="font-size: 34px; font-weight: 800; margin: 4px 0; color: #0F172A !important; letter-spacing: -1px;">{value}</div>
        <p style="color: #475569 !important; font-size: 11.5px; font-weight: 500; margin: 6px 0 0 0; opacity: 0.8;">{unit}</p>
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
            'D1 Ethnic Tension': [f'IKM_{i:03d}' for i in range(1, 12)],
            'D2 Religious Tension': [f'IKM_{i:03d}' for i in range(12, 23)],
            'D3 Economic Tension': [f'IKM_{i:03d}' for i in range(23, 34)],
            'D4 Political Tension': [f'IKM_{i:03d}' for i in range(34, 45)],
            'D5 Generational Tension': [f'IKM_{i:03d}' for i in range(45, 56)],
            'D6 Urban-Rural Tension': [f'IKM_{i:03d}' for i in range(56, 67)],
            'D7 Institutional and Governance Tension': [f'IKM_{i:03d}' for i in range(67, 78)],
            'D8 Social Resilience': [f'IKM_{i:03d}' for i in range(78, 89)],
            'D9 Digital Tension': [f'IKM_{i:03d}' for i in range(89, 100)]
        }

    def connect_and_load_workbook(self, file_source=None):
        try:
            if file_source is not None:
                xls = pd.ExcelFile(file_source)
            else:
                xls = pd.ExcelFile(self.filename)
                
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
        except Exception as e:
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
        all_items = [f'IKM_{i:03d}' for i in range(1, 100) if f'IKM_{i:03d}' in df.columns]
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
        all_items = [f'IKM_{i:03d}' for i in range(1, 100) if f'IKM_{i:03d}' in df.columns]
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
        if self.questionnaire_master is None or self.respondent_data is None: return []
        master_list = self.questionnaire_master['Item_Code'].dropna().unique().tolist()
        return sorted([item for item in master_list if item in self.respondent_data.columns])

    def get_demographic_columns(self):
        if self.respondent_data is None: return []
        demo_cols = ['Zone', 'State', 'District', 'Locality', 'Gender', 'Generation', 'Ethnicity', 'Religion', 'Education', 'Occupation', 'Income_Group', 'Urban_Rural', 'Type_of_Respondent']
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
                body {{ font-family: 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #F0F4F8; color: #0F172A; padding: 40px; line-height: 1.7; }}
                .dossier-wrapper {{ max-width: 1100px; margin: 0 auto; background: #FFFFFF; padding: 50px; border-radius: 20px; border: 1px solid #E2E8F0; box-shadow: 0 15px 35px rgba(15, 23, 42, 0.06); }}
                .header-banner {{ background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #2563EB 100%); color: #FFFFFF; padding: 45px; text-align: center; border-radius: 14px; border-bottom: 6px solid #F59E0B; margin-bottom: 40px; position: relative; }}
                .confidential-tag {{ background: rgba(239, 68, 68, 0.15); color: #EF4444; font-weight: 800; letter-spacing: 2px; font-size: 12px; padding: 4px 14px; border-radius: 30px; display: inline-block; margin-bottom: 15px; border: 1px solid rgba(239, 68, 68, 0.3); }}
                .section-title {{ color: #1E3A8A; border-bottom: 3px solid #3B82F6; padding-bottom: 8px; margin-top: 40px; font-size: 19px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; page-break-after: avoid; }}
                .demo-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; margin: 25px 0; }}
                .demo-card {{ background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); transition: transform 0.2s; }}
                .demo-card:hover {{ transform: translateY(-2px); }}
                .card-blue h4 {{ color: #1E40AF; border-left: 4px solid #2563EB; padding-left: 8px; font-size: 14px; margin: 0 0 12px 0; text-transform: uppercase; }}
                .card-purple h4 {{ color: #6D28D9; border-left: 4px solid #8B5CF6; padding-left: 8px; font-size: 14px; margin: 0 0 12px 0; text-transform: uppercase; }}
                .card-amber h4 {{ color: #B45309; border-left: 4px solid #F59E0B; padding-left: 8px; font-size: 14px; margin: 0 0 12px 0; text-transform: uppercase; }}
                .card-emerald h4 {{ color: #047857; border-left: 4px solid #10B981; padding-left: 8px; font-size: 14px; margin: 0 0 12px 0; text-transform: uppercase; }}
                .table-premium {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
                .table-premium th {{ background: #1E293B; color: #FFFFFF; padding: 10px; text-align: left; font-weight: 600; font-size: 12px; }}
                .table-premium td {{ padding: 9px 8px; border-bottom: 1px solid #F1F5F9; color: #334155; }}
                .col-param {{ width: 60%; font-weight: 600; color: #111827; }}
                .col-val {{ width: 18%; text-align: right; }}
                .col-percent {{ width: 22%; text-align: right; font-weight: 700; color: #2563EB; }}
                .badge-status {{ padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; text-align: center; display: inline-block; }}
                .badge-hotspot {{ background: #FEE2E2; color: #EF4444; border: 1px solid rgba(239,68,68,0.2); }}
                .badge-pain {{ background: #FCE7F3; color: #DB2777; border: 1px solid rgba(219,39,119,0.2); }}
                .badge-tension {{ background: #FFFBEB; color: #D97706; border: 1px solid rgba(217,119,6,0.2); }}
                .badge-low {{ background: #ECFDF5; color: #10B981; border: 1px solid rgba(16,185,129,0.2); }}
                .loc-card-html {{ border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-bottom: 14px; background: #FFFFFF; box-shadow: 0 4px 10px rgba(0,0,0,0.01); }}
                .loc-card-html.danger-zone {{ border-left: 6px solid #EF4444; background: linear-gradient(90deg, #FFF5F5 0%, #FFFFFF 100%); }}
                .loc-card-html.warning-zone {{ border-left: 6px solid #F59E0B; background: linear-gradient(90deg, #FFFDF5 0%, #FFFFFF 100%); }}
                .highlight-box {{ background: linear-gradient(90deg, #EFF6FF 0%, #F8FAFC 100%); border-left: 5px solid #3B82F6; padding: 22px; border-radius: 0 10px 10px 0; margin: 20px 0; font-size: 14px; color: #1E3A8A; font-weight: 500; }}
                .page-break {{ page-break-before: always; }}
                .meta-footer {{ margin-top: 50px; padding-top: 20px; border-top: 2px dashed #CBD5E1; text-align: center; font-size: 12px; color: #64748B; }}
            </style>
        </head>
        <body>
            <div class="dossier-wrapper">
                <div class="header-banner">
                    <div class="confidential-tag">🚨 RAHSIA RASMI — AMANAH KABINET MALAYSIA</div>
                    <h1 style="margin: 0; font-size: 25px; font-weight: 800; letter-spacing: -0.5px;">{title}</h1>
                    <p style="margin: 8px 0 0 0; font-size: 13px; color: #94A3B8; font-weight: 500;">Modul Output Analitik Visualisasi Strategik Perdana</p>
                    <p style="margin: 4px 0 0 0; font-size: 11px; color: #CBD5E1;">Tarikh Cetakan Dokumen: {now_str} | Urus Setia Keselamatan Kebangsaan</p>
                </div>
                
                <div class="section-title">1.0 Ringkasan Eksekutif Petunjuk Prestasi Utama</div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 25px 0;">
                    <div style="background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%); color: white; padding: 22px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(30,58,138,0.2);">
                        <div style="font-size:11px; font-weight:700; text-transform:uppercase; opacity:0.8; letter-spacing:1px;">Skor Indeks Nasional</div>
                        <div style="font-size:32px; font-weight:800; margin:8px 0;">{score:.2f}%</div>
                        <div style="font-size:11px; background:rgba(255,255,255,0.15); padding:3px 10px; border-radius:4px; display:inline-block; font-weight:600;">Status: {tier.upper()}</div>
                    </div>
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 5px solid #10B981; padding: 22px; border-radius: 12px; text-align: center;">
                        <div style="color:#64748B; font-weight:700; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Pool Responden Aktif</div>
                        <div style="font-size:32px; font-weight:800; color:#0F172A; margin:8px 0;">{total_resp:,}</div>
                        <div style="font-size:11px; color:#475569; font-weight:500;">Strata Multikultural DOSM</div>
                    </div>
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 5px solid #EF4444; padding: 22px; border-radius: 12px; text-align: center;">
                        <div style="color:#64748B; font-weight:700; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Ketegangan Dimensi Siber (D9)</div>
                        <div style="font-size:32px; font-weight:800; color:#EF4444; margin:8px 0;">{self.calculate_single_dimension_score('D9 Digital Tension'):.2f}%</div>
                        <div style="font-size:11px; color:#EF4444; font-weight:700;">Zon Kritikal Radar EWS</div>
                    </div>
                </div>

                <div class="highlight-box">
                    <b>💡 MEMORANDUM ANALISIS IMPAK STRATEGIK:</b><br>
                    Teras ancaman polarisasi dikesan bergerak pantas di atas paksi ekosistem digital (D9) and tekanan sosioekonomi akar umbi (D3). Corak data membuktikan ketidakstabilan pasaran kos sara hidup telah memicu defisit keyakinan struktural yang ketara terhadap governans institusi. Segala bentuk tindakan mitigasi harus dijajarkan terus ke lokaliti merah yang dipaparkan dalam laporan ini.
                </div>

                <div class="page-break"></div>

                <div class="section-title">2.0 Grafik Keamatan 9 Dimensi Utama Kebangsaan</div>
                <div class="chart-container">
                    <canvas id="dimensionsChart" style="max-height: 380px;"></canvas>
                </div>
        """

        html_master += """
                <div class="section-title">3.0 Matriks Profil Kumpulan Sasar Pemboleh Ubah Demografi</div>
                <p>Berikut dipaparkan pecahan data agregasi responden menggunakan struktur taburan warna dinamik:</p>
                <div class="demo-grid">"""
                
        color_patterns = ["card-blue", "card-purple", "card-amber", "card-emerald"]
        pattern_idx = 0
        
        if 'Age' in self.respondent_data.columns:
            age_bins = [0, 24, 39, 59, 120]
            age_labels = ['Bawah 25 Tahun (Belia/Remaja)', '25 - 39 Tahun (Dewasa Muda)', '40 - 59 Tahun (Pertengahan Umur)', '60 Tahun & Ke Atas (Warga Emas)']
            age_grouped = pd.cut(self.respondent_data['Age'], bins=age_bins, labels=age_labels).value_counts()
            
            current_pattern = color_patterns[pattern_idx % len(color_patterns)]
            pattern_idx += 1
            
            html_master += f"""
                    <div class="demo-card {current_pattern}">
                        <h4>📊 Profil: Umur (Selang Kumpulan Sasar)</h4>
                        <table class="table-premium">
                            <thead>
                                <tr>
                                    <th class="col-param">Julat Selang Umur</th>
                                    <th class="col-val" style="text-align:right;">Bilangan</th>
                                    <th class="col-percent" style="text-align:right;">Peratus (%)</th>
                                </tr>
                            </thead>
                            <tbody>"""
            for cat, val in age_grouped.items():
                pct = (val / total_resp) * 100
                html_master += f"""
                                <tr>
                                    <td class="col-param">{cat}</td>
                                    <td class="col-val">{val:,}</td>
                                    <td class="col-percent">{pct:.2f}%</td>
                                </tr>"""
            html_master += """
                            </tbody>
                        </table>
                    </div>"""

        for col in self.get_demographic_columns():
            counts = self.respondent_data[col].value_counts()
            current_pattern = color_patterns[pattern_idx % len(color_patterns)]
            pattern_idx += 1
            
            html_master += f"""
                    <div class="demo-card {current_pattern}">
                        <h4>📊 Profil: {col.replace('_', ' ')}</h4>
                        <table class="table-premium">
                            <thead>
                                <tr>
                                    <th class="col-param">Kluster / Parameter</th>
                                    <th class="col-val" style="text-align:right;">Bilangan</th>
                                    <th class="col-percent" style="text-align:right;">Peratus (%)</th>
                                </tr>
                            </thead>
                            <tbody>"""
            for cat, val in counts.items():
                pct = (val / total_resp) * 100
                html_master += f"""
                                <tr>
                                    <td class="col-param">{cat}</td>
                                    <td class="col-val">{val:,}</td>
                                    <td class="col-percent">{pct:.2f}%</td>
                                </tr>"""
            html_master += """
                            </tbody>
                        </table>
                    </div>"""
                    
        html_master += """
                </div>
                <div class="page-break"></div>
        """

        html_master += """
                <div class="section-title">4.0 Analisis Keamatan Aras Ketegangan Komposit 9 Dimensi Utama</div>
                <p>Status risiko dikelaskan secara visual berasaskan kod ambang keselamatan siber nasional:</p>
                <table class="table-premium" style="margin-top:15px;">
                    <thead>
                        <tr>
                            <th style="width:10%;">Kod</th>
                            <th style="width:50%;">Nama Dimensi Skrining Kebangsaan</th>
                            <th style="width:20%;">Skor Ketegangan (%)</th>
                            <th style="width:20%; text-align:center;">Klasifikasi Risiko Sektoral</th>
                        </tr>
                    </thead>
                    <tbody>"""
        for d_key in self.dim_item_ranges.keys():
            d_score = self.calculate_single_dimension_score(d_key)
            d_tier = self.get_tier(d_score)
            badge_class = f"badge-{d_tier}"
            
            html_master += f"""
                        <tr>
                            <td><b>{d_key[:2]}</b></td>
                            <td>{d_key}</td>
                            <td><b style="font-size:14px; color:#1E3A8A;">{d_score:.2f}%</b></td>
                            <td style="text-align:center;"><span class="badge-status {badge_class}">{d_tier}</span></td>
                        </tr>"""
        html_master += """
                    </tbody>
                </table>
                <div class="page-break"></div>
        """

        # RENDER BLOK DATA TEORI SUB-ITEM DENGAN COLORFUL UNTUK OUTPUT HTML DOCK REPORT LENGKAP
        html_master += """
                <div class="section-title">5.0 Pemodelan Teori & Huraian Keputusan Konkreta Item Pangkalan Data</div>
                <p>Analisis penumpuan teori-data menghubungkan angka kuantitatif secara langsung dengan kerangka teori dasar serta sub-item stressor:</p>"""

        theory_dictionary = {
            "Social Identity Theory": {
                "Pengasas": "Henri Tajfel & John Turner (1979)", "Dimensi": "D1 Ethnic Tension",
                "Analisis": "Membuktikan sempadan In-group vs Out-group menebal akibat prasangka rentas etnik. Mengesahkan modal amanah rentas kaum wujud tetapi berada pada tahap rapuh."
            },
            "Conflict Theory": {
                "Pengasas": "Karl Marx / Max Weber", "Dimensi": "D2 Religious Tension",
                "Analisis": "Data merekodkan wujudnya perebutan berterusan antara kumpulan ideologi bagi mendominasi pengaruh institusi dan perundangan dasar."
            },
            "Relative Deprivation Theory": {
                "Pengasas": "Samuel Stouffer (1949) / Ted Robert Gurr (1970)", "Dimensi": "D3 Economic Tension",
                "Analisis": "Kemarahan psikologi terhasıl akibat jurang kos sara hidup yang mendadak. Rakyat membandingkan status ekonomi mereka dengan kelas kapitalis, memicu risiko eskalasi protes fizikal terbuka."
            }
        }

        for t_name, t_meta in theory_dictionary.items():
            qm_subset = self.questionnaire_master[self.questionnaire_master['Theory'] == t_name]
            if not qm_subset.empty:
                codes = [c for c in qm_subset['Item_Code'].tolist() if c in self.respondent_data.columns]
                if codes:
                    t_means = self.respondent_data[codes].mean()
                    t_index_pct = ((t_means.mean() - 1) / 4) * 100
                    
                    html_master += f"""
                    <div style='margin-bottom: 25px; padding: 22px; border: 1px solid #E2E8F0; border-radius: 12px; background: #FFFFFF; box-shadow: 0 4px 6px rgba(0,0,0,0.01); border-left: 6px solid #8B5CF6;'>
                        <h4 style='margin:0 0 8px 0; color:#4C1D95; font-size:15px;'>📚 Kerangka Kerja: {t_name} — Mapped to {t_meta['Dimensi']}</h4>
                        <p style='margin:0 0 10px 0; font-size:12px; color:#64748B;'><b>Tokoh Pelopor:</b> {t_meta['Pengasas']} | <b style='color:#6D28D9;'>Theory Composite Index: {t_index_pct:.2f}%</b></p>
                        <p style='margin:0 0 15px 0; font-size:13.5px; color:#334155;'><b>Analisis Dinamika Teori-Data JPM:</b> {t_meta['Analisis']}</p>
                        
                        <div style='background-color:#F8FAFC; padding:15px; border-radius:8px; border:1px solid #E2E8F0;'>
                            <b style='font-size:12.5px; color:#0F172A; text-transform:uppercase; letter-spacing:0.5px;'>🗂️ Pecahan Isu Sub-Item Akar Umbi (Stressor Real-Time):</b>
                            <table style='width:100%; border-collapse:collapse; margin-top:10px; font-size:12px;'>"""
                    
                    for c_code in codes:
                        c_mean = t_means[c_code]
                        c_stmt = self.questionnaire_master[self.questionnaire_master['Item_Code'] == c_code]['Statement'].values[0]
                        html_master += f"""
                                <tr style='border-bottom:1px solid #F1F5F9;'>
                                    <td style='padding:8px 0; width:15%; color:#2563EB;'><b>{c_code}</b></td>
                                    <td style='padding:8px 0; width:70%; color:#475569;'><i>{c_stmt}</i></td>
                                    <td style='padding:8px 0; width:15%; text-align:right; color:#111827;'><b>Min Sebenar: {c_mean:.2f}/5</b></td>
                                </tr>"""
                    html_master += """
                            </table>
                        </div>
                    </div>"""
        html_master += """<div class="page-break"></div>"""

        html_master += """
                <div class="section-title">6.0 Laporan Hierarki Spasial Rantaian Lokasi Paling Terjejas (Top 10 Hotspots)</div>
                <p>Rantaian geografi kritikal di bawah dipaparkan mengikut skema impak suhu konflik siber setempat:</p>"""
        
        if not geo_means_html.empty:
            for rank, ((zn, st_n, ds_n, ur_n), v_score) in enumerate(geo_means_html.head(10).items()):
                pct_v = ((v_score - 1) / 4) * 100
                sub_df = self.respondent_data[(self.respondent_data['Zone']==zn) & (self.respondent_data['State']==st_n) & (self.respondent_data['District']==ds_n) & (self.respondent_data['Urban_Rural']==ur_n)]
                if not sub_df.empty:
                    sub_item = sub_df[items].mean().idxmax() if items else None
                    if sub_item:
                        sub_stmt = self.questionnaire_master[self.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                        zone_color_style = "danger-zone" if pct_v >= 70.0 else "warning-zone"
                        
                        html_master += f"""
                        <div class="loc-card-html {zone_color_style}">
                            <span style="font-weight:800; text-transform:uppercase; font-size:11px; color:#1E3A8A;">🔥 Hotspot Rank #{rank+1}</span>
                            <h3 style="margin:4px 0 8px 0; font-size:15px; color:#111827;">📍 Wilayah {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} ({ur_n})</h3>
                            <p style="margin:0; font-size:13px; color:#475569;">
                                * Skor Komposit Komparatif Indeks: <b style="color:#EF4444;">{pct_v:.2f}%</b> (EWS Klasifikasi: {self.get_tier(pct_v).upper()})<br>
                                * 🔍 <b>Punca Akar Umbi Utama (Stressor):</b> Item {sub_item} &rarr; <i style="color:#0F172A; font-weight:500;">"{sub_stmt}"</i>
                            </p>
                        </div>"""
        html_master += """<div class="page-break"></div>"""

        html_master += """
                <div class="section-title">7.0 Log Tangkapan Data Scraping Siber Digital (Top 10 OSINT Logs)</div>
                <p>Berikut dipaparkan 10 data perbincangan siber utama yang disaring berdasarkan keutamaan profil isu risiko:</p>
                <table class="table-premium">
                    <thead><tr><th>Tarikh</th><th>Platform</th><th>Wilayah Negeri</th><th>Kategori Isu</th><th>Aras Risiko</th><th>Ringkasan Fail Master</th></tr></thead>
                    <tbody>"""
        if self.media_issue_summary is not None:
            for _, row in self.media_issue_summary.head(10).iterrows():
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
                                backgroundColor: [
                                    'rgba(37, 99, 235, 0.8)',   'rgba(139, 92, 246, 0.8)',
                                    'rgba(245, 158, 11, 0.8)',  'rgba(239, 68, 68, 0.8)',
                                    'rgba(16, 185, 129, 0.8)',  'rgba(6, 182, 212, 0.8)',
                                    'rgba(236, 72, 153, 0.8)',  'rgba(100, 116, 139, 0.8)',
                                    'rgba(15, 23, 42, 0.8)'
                                ],
                                borderColor: 'rgba(15, 23, 42, 1)',
                                borderWidth: 1
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            plugins: {{ legend: {{ display: false }} }},
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
        st.markdown("<div style='text-align: center; padding-top: 100px;'><h2>🏛️ Urus Setia Polisi IKMM 2026</h2><p>Sistem Intelligence Amaran Awal Konflik Kebangsaan (JPM)</p></div>", unsafe_allow_html=True)
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
    
    # --- RENDER TOP HERO BANNER ---
    st.markdown("""
        <div class="system-banner-premium">
            <div class="system-tag">🔐 KAWALAN RAHSIA RASMI</div>
            <h1 style='margin: 0; padding-bottom: 6px; font-size: 28px; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 800;'>
                🏛️ SISTEM ANALITIK KOMPOSIT IKMM 2026
            </h1>
            <p style='margin: 0; font-size: 14px; color: #E2E8F0 !important; font-weight: 500; opacity: 0.95;'>
                Sistem Intelligence & Amaran Awal Konflik Kebangsaan | Jabatan Perdana Menteri (JPM)
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- INITIALISE SIDEBAR PENAPIS SECARA MANDATORI (ANTI-GHAIB & KALIS CRASH) ---
    active_filters = {}
    sel_state = []
    
    with st.sidebar:
        st.markdown("### 🗺️ Pengendali Penapis Geografi Dinamik")
        zon_options = engine.get_filter_options('Zone') if engine.data_loaded else []
        sel_zone = st.multiselect("🧭 1. Pilih Wilayah / Zon", zon_options)
        
        if sel_zone and engine.data_loaded:
            state_subset = engine.respondent_data[engine.respondent_data['Zone'].isin(sel_zone)]
            state_options = sorted(state_subset['State'].dropna().unique().tolist())
        else:
            state_options = engine.get_filter_options('State') if engine.data_loaded else []
        sel_state = st.multiselect("🏛️ 2. Pilih Negeri", state_options)
        
        if sel_state and engine.data_loaded:
            district_subset = engine.respondent_data[engine.respondent_data['State'].isin(sel_state)]
            district_options = sorted(district_subset['District'].dropna().unique().tolist())
        elif sel_zone and engine.data_loaded:
            district_subset = engine.respondent_data[engine.respondent_data['Zone'].isin(sel_zone)]
            district_options = sorted(district_subset['District'].dropna().unique().tolist())
        else:
            district_options = engine.get_filter_options('District') if engine.data_loaded else []
        sel_district = st.multiselect("🏙️ 3. Pilih Daerah / Parlimen", district_options)
        
        st.markdown("---")
        st.markdown("### 📊 Tapisan Sosioekonomi Kumpulan")
        urban_opts = engine.get_filter_options('Urban_Rural') if engine.data_loaded else []
        income_opts = engine.get_filter_options('Income_Group') if engine.data_loaded else []
        
        sel_urban = st.multiselect("🏢 Klasifikasi Lokaliti", urban_opts)
        sel_income = st.multiselect("💰 Kumpulan Pendapatan", income_opts)
        
        if sel_zone: active_filters['Zone'] = sel_zone
        if sel_state: active_filters['State'] = sel_state
        if sel_district: active_filters['District'] = sel_district
        if sel_urban: active_filters['Urban_Rural'] = sel_urban
        if sel_income: active_filters['Income_Group'] = sel_income

    # --- EMULASI PROSES DATA SETELAH PENAPIS SELESAI DIBACA ---
    if engine.data_loaded and engine.respondent_data is not None:
        filtered_df = engine.apply_filters(active_filters)
        sub_total = len(filtered_df)
        items_list_main = engine.get_registered_items()
        if sub_total > 0 and items_list_main:
            geo_means_main = filtered_df.groupby(['Zone', 'State', 'District', 'Urban_Rural'])[items_list_main].mean().mean(axis=1).sort_values(ascending=False)
        else:
            geo_means_main = pd.Series()
    else:
        filtered_df = pd.DataFrame()
        sub_total = 0
        items_list_main = []
        geo_means_main = pd.Series()

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
        uploaded_file = st.file_uploader("Sila Pilih / Lepaskan Fail Pangkalan Data Excel Master IKMM (.xlsx)", type=['xlsx'], key="excel_uploader_core")
        
        if uploaded_file is not None:
            if st.button("Proses & Hubungkan Fail Excel Baharu", use_container_width=True, key="trigger_process_btn"):
                success = engine.connect_and_load_workbook(uploaded_file)
                if success:
                    st.success("🔥 Sempurna! Fail data berjaya dihubungkan ke memori sistem.")
                    st.rerun()
                else:
                    st.error("Ralat: Struktur helaian (Sheets) dalam fail Excel tidak sepadan dengan master model.")
        
        st.markdown("---")

    # --- MENYEKAT PAPARAN KANDUNGAN TAB JIKA DATA BELUM DIMUAT NAIK ---
    if not engine.data_loaded or engine.respondent_data is None:
        with tabs[0]:
            st.warning("⚠️ Amaran Keselamatan Model: Sila muat naik fail data induk atau letakkan dokumen 'IKM_Master_Dataset_20000_Respondents.xlsx' untuk membongkar portal analitik premium.")
    else:
        with tabs[0]:
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

        with tabs[1]:
            st.subheader("📈 Pusat Kawalan KPI Ketegangan Nasional")
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

        with tabs[2]:
            st.subheader("🗺️ Analisis Ketegangan Geospatial Mengikut Negeri")
            if items_list_main and not filtered_df.empty:
                state_df = filtered_df.groupby('State')[items_list_main].mean().mean(axis=1).reset_index(name='Indeks Ketegangan (IKM %)')
                state_df['Indeks Ketegangan (IKM %)'] = ((state_df['Indeks Ketegangan (IKM %)'] - 1) / 4) * 100
                state_df = state_df.rename(columns={'State': 'Negeri / Wilayah'}).sort_values('Indeks Ketegangan (IKM %)', ascending=False)
                col_ch, col_tb = st.columns([3, 2])
                with col_ch: st.plotly_chart(px.bar(state_df, x='Indeks Ketegangan (IKM %)', y='Negeri / Wilayah', orientation='h', color='Indeks Ketegangan (IKM %)', color_continuous_scale='YlOrRd', text_auto='.1f'), use_container_width=True)
                with col_tb: st.dataframe(state_df, use_container_width=True, hide_index=True)

        with tabs[3]:
            st.subheader("📊 Pengiraan Spesifik Komposit Setiap Dimensi Skrining")
            grid_c1, grid_c2, grid_c3 = st.columns(3)
            loop_counter = 0
            for dim_name in engine.dim_item_ranges.keys():
                d_score = engine.calculate_single_dimension_score(dim_name, filtered_df)
                target_col = grid_c1 if loop_counter % 3 == 0 else (grid_c2 if loop_counter % 3 == 1 else grid_c3)
                with target_col: render_kpi_card(f"{dim_name}", f"{d_score:.2f}%", f"Berasaskan Item Indikator Ditapis", tier=engine.get_tier(d_score))
                loop_counter += 1

        with tabs[4]:
            st.subheader("🚨 Pengesanan Awal: 5 Indikator Utama Paling Tegang (Stressor Wilayah)")
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

        with tabs[5]:
            st.subheader("💬 Suara Marhaen: Analisis Klasifikasi Tema & Sentimen NLP Teks Rakyat")
            if engine.qualitative_response is not None and not engine.qualitative_response.empty:
                c_filter_q, _ = st.columns([1, 2])
                with c_filter_q: st_sel_q = st.selectbox("Pilih Analisis Wilayah Negeri", sorted(engine.qualitative_response['State'].dropna().unique().tolist()))
                st.markdown(f"#### 🎯 Dapatan Ekstraksi Algoritma NLP bagi Wilayah: **{st_sel_q}**")
                st.markdown("> *Contoh Petikan Teks Rakyat (Verbatim):* \"Gaji tak naik-naik tapi harga barang dapur makin melampau.\"")

        # --- TAB 7: PUSAT INTERPRETASI PSIKOMETRIK LENGKAP BERSERTA PECAHAN SUB-ITEM ---
        with tabs[6]:
            st.subheader("🧠 Pusat Interpretasi Psikometrik & Analisis Penumpuan Teori-Data")
            st.markdown("#### Kerangka Tafsir Konvergen Teori Dasar Sosial Nasional (JPM)")
            
            theory_map_dashboard = {
                "Social Identity Theory": {
                    "Dimensi": "D1 Ethnic Tension",
                    "Desc": "Membuktikan sempadan In-group vs Out-group menebal akibat prasangka rentas etnik. Mengesahkan modal amanah rentas kaum wujud tetapi berada pada tahap rapuh."
                },
                "Conflict Theory": {
                    "Dimensi": "D2 Religious Tension",
                    "Desc": "Data merekodkan wujudnya perebutan berterusan antara kumpulan ideologi bagi mendominasi pengaruh institusi dan perundangan dasar."
                },
                "Relative Deprivation Theory": {
                    "Dimensi": "D3 Economic Tension",
                    "Desc": "Kemarahan psikologi terhasıl akibat jurang kos sara hidup yang mendadak. Rakyat membandingkan status ekonomi mereka dengan kelas kapitalis, memicu risiko eskalasi protes fizikal terbuka."
                }
            }
            
            for t_name, t_meta in theory_map_dashboard.items():
                qm_sub = engine.questionnaire_master[engine.questionnaire_master['Theory'] == t_name]
                if not qm_sub.empty:
                    valid_codes = [c for c in qm_sub['Item_Code'].tolist() if c in filtered_df.columns]
                    if valid_codes:
                        # Kirim matriks pengiraan index peratusan teori
                        t_means = filtered_df[valid_codes].mean()
                        t_index_pct = ((t_means.mean() - 1) / 4) * 100
                        t_tier = engine.get_tier(t_index_pct)
                        
                        st.markdown(f"""
                        <div class="loc-card-premium" style="border-left: 6px solid #8B5CF6; background: linear-gradient(90deg, #F5F3FF 0%, #FFFFFF 100%); margin-bottom:25px;">
                            <span style="font-weight:800; font-size:11px; color:#6D28D9; text-transform:uppercase; letter-spacing:0.8px;">Model Teras Analitik Strategik</span>
                            <h3 style="margin:4px 0 6px 0; color:#4C1D95; font-size:16px;">📚 Kerangka Teori: {t_name} (&rarr; Terikat {t_meta['Dimensi']})</h3>
                            <p style="margin:0 0 12px 0; font-size:13.5px; color:#475569;">{t_meta['Desc']}</p>
                            <div style="font-size:14px; font-weight:700; color:#6D28D9; margin-bottom:15px;">📈 Hasil Keamatan Indeks Teori: {t_index_pct:.2f}% (Status: {t_tier.upper()})</div>
                            
                            <div style="background:#F8FAFC; padding:12px; border-radius:8px; border:1px solid #E2E8F0;">
                                <span style="font-size:11.5px; font-weight:700; color:#0F172A; text-transform:uppercase;">🗂️ Pecahan Isu Sub-Item Stressor Real-Time:</span>
                                <table style="width:100%; border-collapse:collapse; margin-top:8px; font-size:12.5px; color:#334155;">
                        """, unsafe_allow_html=True)
                        
                        # Loop sub-item untuk dipaparkan secara details
                        for c_code in valid_codes:
                            c_mean = t_means[c_code]
                            c_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == c_code]['Statement'].values[0]
                            st.markdown(f"""
                                    <tr style="border-bottom:1px solid #EFF6FF;">
                                        <td style="padding:6px 0; width:12%; color:#2563EB;"><b>{c_code}</b></td>
                                        <td style="padding:6px 0; width:73%; color:#475569;"><i>{c_stmt}</i></td>
                                        <td style="padding:6px 0; width:15%; text-align:right; color:#111827;"><b>Skala Min: {c_mean:.2f}/5</b></td>
                                    </tr>
                            """, unsafe_allow_html=True)
                            
                        st.markdown("""
                                </table>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        with tabs[7]:
            st.subheader("⚠️ Pengelasan Petunjuk Titik Kelemahan Struktur (Pain Points)")
            if not geo_means_main.empty and items_list_main:
                rank_pp = 1
                for (zn, st_n, ds_n, ur_n), v_val in geo_means_main.items():
                    pct_v = ((v_val - 1) / 4) * 100
                    if 40.0 <= pct_v < 60.0:
                        sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                        if not sub_df.empty:
                            sub_item = sub_df[items_list_main].mean().idxmax()
                            sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                            st.markdown(f"""
                            <div class='loc-card-premium' style='border-left-color: #DB2777; background: linear-gradient(90deg, #FDF2F8 0%, #FFFFFF 100%);'>
                                <b>📍 RANTAIAN LOKASI #{rank_pp}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>
                                * **Skor Ketegangan Setempat:** {pct_v:.2f}%<br>
                                * 🔍 **Punca Utama (Stressor):** Item {sub_item} &rarr; <i>"{sub_stmt}"</i>
                            </div>
                            """, unsafe_allow_html=True)
                            rank_pp += 1
                if rank_pp == 1: st.success("✓ Sempurna. Tiada rantaian lokasi di dalam zon amaran Pain Points.")

        with tabs[8]:
            st.subheader("🔥 Kerangka Eskalasi Indikator Titik Ketegangan (Tension Points)")
            if not geo_means_main.empty and items_list_main:
                rank_tp = 1
                for (zn, st_n, ds_n, ur_n), v_val in geo_means_main.items():
                    pct_v = ((v_val - 1) / 4) * 100
                    if 60.0 <= pct_v < 80.0:
                        sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                        if not sub_df.empty:
                            sub_item = sub_df[items_list_main].mean().idxmax()
                            sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                            st.markdown(f"""
                            <div class='loc-card-premium' style='border-left-color: #F59E0B; background: linear-gradient(90deg, #FFFBEB 0%, #FFFFFF 100%);'>
                                <b>📍 RANTAIAN LOKASI #{rank_tp}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>
                                * **Skor Ketegangan Setempat:** {pct_v:.2f}%<br>
                                * 🔍 **Punca Utama (Stressor):** Item {sub_item} &rarr; <i>"{sub_stmt}"</i>
                        </div>
                        """, unsafe_allow_html=True)
                        rank_tp += 1
                if rank_tp == 1: st.success("✓ Tiada rantaian lokasi di tahap amaran jingga.")

        with tabs[9]:
            st.subheader("🚨 Early Warning System (EWS) — Sempadan Amaran Hotspot Kritikal")
            if not geo_means_main.empty and items_list_main:
                rank_hs = 1
                for (zn, st_n, ds_n, ur_n), v_val in geo_means_main.items():
                    pct_v = ((v_val - 1) / 4) * 100
                    if pct_v >= 80.0:
                        sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                        if not sub_df.empty:
                            sub_item = sub_df[items_list_main].mean().idxmax()
                            sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                            st.markdown(f"""
                            <div class='loc-card-premium' style='border-left-color: #EF4444; background: linear-gradient(90deg, #FEF2F2 0%, #FFFFFF 100%);'>
                                <b style='color: #DC2626;'>💥 CRITICAL ZON #{rank_hs}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>
                                * **Skor Komposit EWS Bahaya:** {pct_v:.2f}%<br>
                                * 🛑 **PUNCA SEBENAR KRITIKAL (Stressor):** Item {sub_item} &rarr; <i style='color: #991B1B;'>"{sub_stmt}"</i>
                            </div>
                            """, unsafe_allow_html=True)
                            rank_hs += 1
                if rank_hs == 1: st.success("✓ Selamat. Tiada zon merah ekstrem dikesan.")

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

        with tabs[11]:
            st.subheader("📰 Papan Pemantauan Media Cetak & Aliran Sentimen Siber Digital")
            if engine.media_issue_summary is not None and not engine.media_issue_summary.empty:
                m_df = engine.media_issue_summary
                display_media = m_df.copy()
                if sel_state: display_media = display_media[display_media['State'].isin(sel_state)]
                top_rows = display_media.head(5)
                for idx, row in top_rows.iterrows():
                    st.markdown(f"🔹 **Log Node #{idx+1} — Tarikh: {row.get('Date', 'N/A')} | Platform: {row.get('Source', 'N/A')}**\n* 💬 Teks Rumusan: \"{row.get('Summary', 'N/A')}\"")

        with tabs[12]:
            st.subheader("👥 Transkrip Consensus Panel Pakar & Dapatan Bengkel FGD")
            if engine.fgd_expert is not None and not engine.fgd_expert.empty:
                st.plotly_chart(px.bar(engine.fgd_expert['Priority'].value_counts(), title="Klasifikasi Syor Pakar"), use_container_width=True)

        with tabs[13]:
            st.subheader("📄 Penjanaan HTML Briefing Dossier")
            rep_title = st.text_input("Tajuk Laporan Eksekutif JPM", "Laporan Hasil Kajian Indeks Ketegangan Masyarakat Malaysia (IKMM) 2026")
            rep_officer = st.text_input("Nama Pegawai Pelapor Muktamad", "Dato' Sri Ketua Pengarah JPNIN")
            rep_branch = st.text_input("Bahagian / Agensi Utama", "Kluster Analitik Risiko Polisi Strategik")
            if st.button("Kompilasikan Dokumen Laporan Komposit", use_container_width=True):
                html_code = engine.generate_html_dossier_report(rep_title, rep_officer, rep_branch)
                st.success("✓ Dokumen Dossier Kabinet Mega Berjaya Dikompilasikan!")
                st.download_button("⬇ Muat Turun Fail HTML Dossier Perdana", html_code, "IKMM_Executive_Dossier_2026.html", "text/html", use_container_width=True)
                
        with tabs[14]:
            st.subheader("🔎 Advanced Database Structural Cell Matrix Explorer")
            st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
