import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import hashlib
from io import BytesIO
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except:
    REPORTLAB_AVAILABLE = False

# Configuration Aplikasi Utama
st.set_page_config(
    page_title="Malaysian IKM Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'Malaysian Societal Tension Index Dashboard v3.1'
    }
)

ADMIN_PASSWORD = "admin123"
GOVT_COLORS = {
    'primary': '#1A1B4D',
    'secondary': '#2C3E7F',
    'accent': '#00D9FF',
    'gold': '#FFD700',
    'danger': '#FF6B6B',
    'success': '#51CF66',
    'warning': '#FFA500',
    'navy': '#0A1D3D',
    'cyan': '#00B4D8',
    'light_gold': '#FFED4E'
}

# Pemetaan Struktur 9 Dimensi Mengikut Fail Master IKM (108 Items)
SUBINDICES_MAPPING = {
    'D1 Ethnic Tension Index': [f'IKM_{i:03d}' for i in range(1, 13)],
    'D2 Religious Tension Index': [f'IKM_{i:03d}' for i in range(13, 25)],
    'D3 Economic Tension Index': [f'IKM_{i:03d}' for i in range(25, 37)],
    'D4 Political Tension Index': [f'IKM_{i:03d}' for i in range(37, 49)],
    'D5 Generational Tension Index': [f'IKM_{i:03d}' for i in range(49, 61)],
    'D6 Urban-Rural Tension Index': [f'IKM_{i:03d}' for i in range(61, 73)],
    'D7 Institutional & Governance Index': [f'IKM_{i:03d}' for i in range(73, 85)],
    'D8 Social Resilience Index': [f'IKM_{i:03d}' for i in range(85, 97)],
    'D9 Digital Tension Index': [f'IKM_{i:03d}' for i in range(97, 109)]
}

class IKMDashboardAdvanced:
    def __init__(self):
        self.respondent_data = None
        self.questionnaire_master = None
        self.qualitative_response = None
        self.theory_mapping = None
        self.intervention_library = None
        self.media_issue_summary = None
        self.fgd_expert = None
        self.state_zone_mapping = None
        self.dashboard_config = None
        self.data_loaded = False
        
    def load_excel_data(self, file):
        try:
            xls = pd.ExcelFile(file)
            
            if 'respondent_data' in xls.sheet_names:
                self.respondent_data = pd.read_excel(file, sheet_name='respondent_data')
            else:
                st.error("❌ Required sheet 'respondent_data' not found")
                return False
                
            if 'questionnaire_master' in xls.sheet_names:
                self.questionnaire_master = pd.read_excel(file, sheet_name='questionnaire_master')
            else:
                st.error("❌ Required sheet 'questionnaire_master' not found")
                return False
            
            if 'qualitative_response' in xls.sheet_names:
                self.qualitative_response = pd.read_excel(file, sheet_name='qualitative_response')
            if 'theory_mapping' in xls.sheet_names:
                self.theory_mapping = pd.read_excel(file, sheet_name='theory_mapping')
            if 'intervention_library' in xls.sheet_names:
                self.intervention_library = pd.read_excel(file, sheet_name='intervention_library')
            if 'media_issue_summary' in xls.sheet_names:
                self.media_issue_summary = pd.read_excel(file, sheet_name='media_issue_summary')
            if 'fgd_expert' in xls.sheet_names:
                self.fgd_expert = pd.read_excel(file, sheet_name='fgd_expert')
            if 'state_zone_mapping' in xls.sheet_names:
                self.state_zone_mapping = pd.read_excel(file, sheet_name='state_zone_mapping')
            if 'dashboard_config' in xls.sheet_names:
                self.dashboard_config = pd.read_excel(file, sheet_name='dashboard_config')
                
            self.data_loaded = True
            return True
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            return False
    
    def get_item_columns(self):
        if self.questionnaire_master is None:
            return []
        return sorted(self.questionnaire_master['Item_Code'].dropna().unique().tolist())
    
    def get_demographic_columns(self):
        demo_cols = ['Zone', 'State', 'District', 'Locality', 'Type_of_Respondent', 
                     'Gender', 'Generation', 'Urban_Rural', 'Income_Group', 'Ethnicity', 'Religion']
        return [col for col in demo_cols if col in self.respondent_data.columns]
    
    def calculate_item_scores(self, data=None):
        if data is None:
            data = self.respondent_data
        if data is None or self.questionnaire_master is None:
            return {}
        
        item_cols = self.get_item_columns()
        scores = {}
        for item in item_cols:
            if item in data.columns:
                scores[item] = {
                    'mean': data[item].mean(),
                    'std': data[item].std(),
                    'min': data[item].min(),
                    'max': data[item].max(),
                    'median': data[item].median(),
                    'count': len(data[item].dropna())
                }
        return scores
    
    def calculate_dimension_scores(self, data=None):
        if data is None:
            data = self.respondent_data
        if self.questionnaire_master is None or 'Dimension' not in self.questionnaire_master.columns:
            return {}
        
        dim_map = dict(zip(self.questionnaire_master['Item_Code'], self.questionnaire_master['Dimension']))
        dim_scores = {}
        item_cols = self.get_item_columns()
        
        for dim in self.questionnaire_master['Dimension'].dropna().unique():
            dim_items = [col for col in item_cols if dim_map.get(col) == dim]
            valid_items = [col for col in dim_items if col in data.columns]
            if valid_items:
                dim_data = data[valid_items].mean(axis=1)
                dim_scores[dim] = {
                    'mean': dim_data.mean(),
                    'std': dim_data.std(),
                    'count': len(valid_items),
                    'status': self._get_status(dim_data.mean())
                }
        return dim_scores
    
    def calculate_subindices_scores(self, data=None):
        if data is None:
            data = self.respondent_data
        
        subindices = {}
        for subindex_name, item_codes in SUBINDICES_MAPPING.items():
            valid_items = [item for item in item_codes if item in data.columns]
            if valid_items:
                score = data[valid_items].mean().mean()
                subindices[subindex_name] = {
                    'score': score,
                    'status': self._get_status(score),
                    'items': valid_items,
                    'count': len(valid_items)
                }
        return subindices
    
    def calculate_ikm_score(self, data=None):
        if data is None:
            data = self.respondent_data
        item_cols = self.get_item_columns()
        valid_items = [col for col in item_cols if col in data.columns]
        if valid_items:
            return data[valid_items].mean().mean()
        return 0.0
    
    def calculate_irk_score(self, data=None):
        if data is None:
            data = self.respondent_data
        item_cols = self.get_item_columns()
        valid_items = [col for col in item_cols if col in data.columns]
        if valid_items:
            scores = data[valid_items].mean()
            risk_items = (len(scores[scores >= 3.8]) / len(valid_items)) * 100
            return risk_items
        return 0.0
    
    def _get_status(self, score):
        if score >= 4.2:
            return 'Critical'
        elif score >= 3.8:
            return 'Elevated'
        elif score >= 3.0:
            return 'Moderate'
        else:
            return 'Stable'
    
    def get_hotspots(self, data=None):
        if data is None:
            data = self.respondent_data
        hotspots = {}
        if 'State' in data.columns:
            item_cols = [col for col in self.get_item_columns() if col in data.columns]
            if item_cols:
                for state in data['State'].dropna().unique():
                    state_data = data[data['State'] == state]
                    score = state_data[item_cols].mean().mean()
                    hotspots[state] = {
                        'score': score,
                        'status': self._get_status(score),
                        'respondents': len(state_data),
                        'risk_level': (score / 5.0) * 100
                    }
        return hotspots
    
    def detect_themes(self):
        if self.qualitative_response is None:
            return {}
        themes = {}
        for col, key in [('Q3_Main_Source_of_Tension', 'Tension_Sources'), 
                         ('Q1_Main_Concern', 'Main_Concerns'), 
                         ('Q4_Suggested_Intervention', 'Suggested_Interventions')]:
            matched_col = [c for c in self.qualitative_response.columns if c.lower() == col.lower()]
            if matched_col:
                themes[key] = self.qualitative_response[matched_col[0]].value_counts().to_dict()
        return themes
    
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
    
    def get_theory_analysis(self):
        df = None
        if self.theory_mapping is not None and 'Theory' in self.theory_mapping.columns:
            df = self.theory_mapping
        elif self.questionnaire_master is not None and 'Theory' in self.questionnaire_master.columns:
            df = self.questionnaire_master
            
        if df is None:
            return None

        theories = {}
        for theory, group in df.groupby('Theory'):
            dimensions = group['Dimension'].dropna().unique().tolist() if 'Dimension' in group.columns else []
            subdimensions = group['Subdimension'].dropna().unique().tolist() if 'Subdimension' in group.columns else []
            theories[theory] = {
                'count': len(group),
                'dimensions': sorted(dimensions),
                'subdimensions': sorted(subdimensions),
            }
        return theories if theories else None

    def generate_html_report(self, title, sections, signature_officer, signature_title):
        ikm_score = self.calculate_ikm_score()
        irk_score = self.calculate_irk_score()
        respondents = len(self.respondent_data) if self.respondent_data is not None else 0
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #1A1B4D 0%, #2C3E7F 100%); color: white; padding: 30px; text-align: center; border-bottom: 4px solid #00D9FF; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
                .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0; }}
                .kpi-card {{ background: #1A1B4D; color: white; padding: 20px; border-radius: 6px; text-align: center; border: 2px solid #FFD700; }}
                .kpi-value {{ font-size: 28px; font-weight: bold; color: #00D9FF; }}
                .data-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .data-table th {{ background-color: #1A1B4D; color: #FFD700; padding: 12px; text-align: left; }}
                .data-table td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                .data-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .footer {{ margin-top: 40px; padding-top: 20px; border-top: 2px solid #FFD700; font-size: 12px; text-align: center; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏛️ {title}</h1>
                    <p>Malaysian Societal Tension Index (IKM) Official Report</p>
                    <p>Generated on {datetime.now().strftime('%d %B %Y')}</p>
                </div>
                
                <div class="kpi-grid">
                    <div class="kpi-card"><div class="kpi-value">{ikm_score:.2f}</div><div>National Index Mean</div></div>
                    <div class="kpi-card"><div class="kpi-value">{irk_score:.1f}%</div><div>Early Warning Alert Rate</div></div>
                    <div class="kpi-card"><div class="kpi-value">{respondents:,}</div><div>Total Sample Pool</div></div>
                </div>
        """
        if 'Dimension Analysis' in sections:
            dim_scores = self.calculate_dimension_scores()
            html_content += """
                <h2>Dimension Analysis</h2>
                <table class="data-table">
                    <thead><tr><th>Dimension</th><th>Score (1-5)</th><th>Status</th><th>Items</th></tr></thead>
                    <tbody>"""
            for dim, d_data in dim_scores.items():
                html_content += f"<tr><td>{dim}</td><td>{d_data['mean']:.2f}</td><td>{d_data['status']}</td><td>{d_data['count']}</td></tr>"
            html_content += "</tbody></table>"
            
        html_content += f"""
                <div class="footer">
                    <p>Prepared by: <b>{signature_officer}</b> ({signature_title})</p>
                    <p>CONFIDENTIAL - INTERNAL GOVERNMENT USE ONLY</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content

def apply_premium_theme():
    st.markdown("""
        <style>
            .stApp {
                background: radial-gradient(circle at top right, #0A1128 0%, #02040A 100%) !important;
                color: #E2E8F0 !important;
            }
            [data-testid="stSidebar"] {
                background-color: #050B1A !important;
                border-right: 1px solid rgba(0, 217, 255, 0.1) !important;
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: rgba(5, 11, 26, 0.7);
                padding: 8px 12px;
                border-radius: 12px;
                border: 1px solid rgba(255, 215, 0, 0.1);
                backdrop-filter: blur(10px);
            }
            .stTabs [data-baseweb="tab"] {
                height: 40px;
                padding: 0px 16px !important;
                background-color: transparent !important;
                border-radius: 8px !important;
                color: #A0AEC0 !important;
                font-weight: 600 !important;
                border: none !important;
                transition: all 0.3s ease;
            }
            .stTabs [data-baseweb="tab"]:hover {
                color: #00D9FF !important;
                background-color: rgba(0, 217, 255, 0.05) !important;
            }
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, rgba(0, 217, 255, 0.2) 0%, rgba(44, 62, 127, 0.2) 100%) !important;
                color: #FFD700 !important;
                border: 1px solid rgba(255, 215, 0, 0.3) !important;
                box-shadow: 0 0 15px rgba(0, 217, 255, 0.1);
            }
            .kpi-container-premium {
                background: linear-gradient(135deg, rgba(10, 25, 47, 0.6) 0%, rgba(5, 11, 26, 0.8) 100%);
                border: 1px solid rgba(0, 217, 255, 0.2);
                border-left: 4px solid #00D9FF;
                border-radius: 12px;
                padding: 24px;
                text-align: center;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                backdrop-filter: blur(8px);
                transition: transform 0.3s ease, border-color 0.3s ease;
            }
            .kpi-container-premium:hover {
                transform: translateY(-4px);
                border-color: #FFD700;
                box-shadow: 0 12px 20px 0 rgba(255, 215, 0, 0.1);
            }
            .kpi-danger-premium {
                border-left: 4px solid #FF6B6B !important;
                border-color: rgba(255, 107, 107, 0.2);
            }
            .kpi-danger-premium:hover {
                border-color: #FF6B6B !important;
                box-shadow: 0 12px 20px 0 rgba(255, 107, 107, 0.15);
            }
            .streamlit-expanderHeader {
                background-color: rgba(10, 25, 47, 0.4) !important;
                border-radius: 8px !important;
                border: 1px solid rgba(255, 255, 255, 0.05) !important;
            }
            ::-webkit-scrollbar { width: 8px; height: 8px; }
            ::-webkit-scrollbar-track { background: #02040A; }
            ::-webkit-scrollbar-thumb { background: #1A1B4D; border-radius: 4px; }
            ::-webkit-scrollbar-thumb:hover { background: #00D9FF; }
        </style>
    """, unsafe_allow_html=True)

def create_kpi_card(label, value, unit="", color="accent"):
    is_danger = "kpi-danger-premium" if color == "danger" else ""
    st.markdown(f"""
    <div class="kpi-container-premium {is_danger}">
        <p style='color: #8892B0; margin: 0; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>{label}</p>
        <h2 style='color: #FFFFFF; margin: 12px 0; font-size: 38px; font-weight: 700; font-family: sans-serif; letter-spacing: -0.5px;'>{value}</h2>
        <p style='color: #00D9FF; margin: 0; font-size: 11px; font-weight: 500;'>{unit}</p>
    </div>
    """, unsafe_allow_html=True)

def init_session():
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = IKMDashboardAdvanced()
    else:
        # LOGIK AUTO-REPAIR: Memastikan objek hot-reload mempunyai semua atribut terkini
        required_attrs = [
            'respondent_data', 'questionnaire_master', 'qualitative_response', 
            'theory_mapping', 'intervention_library', 'media_issue_summary', 
            'fgd_expert', 'state_zone_mapping', 'dashboard_config', 'data_loaded'
        ]
        for attr in required_attrs:
            if not hasattr(st.session_state.dashboard, attr):
                setattr(st.session_state.dashboard, attr, None if attr != 'data_loaded' else False)
                
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

def login_page():
    apply_premium_theme()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='text-align: center; padding-top: 100px;'><h1>🏛️ System Intelligence IKM</h1><p>National Societal Tension Security Framework</p></div>", unsafe_allow_html=True)
        with st.form("login_form"):
            password = st.text_input("🔑 Administration Access Key Token", type="password")
            if st.form_submit_button("Authenticate System Access", use_container_width=True):
                if hashlib.sha256(password.encode()).hexdigest() == hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest():
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Administration Security Credentials")

# --- STRUKTUR ANTARAMUKA TAB ---

def tab_01_gateway():
    st.title("📂 Core Framework Gateway Pipeline")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📥 Load Analytics Framework Model")
        uploaded_file = st.file_uploader("Upload Active Matrix Excel Database (.xlsx)", type=['xlsx'])
        if uploaded_file and st.button("Initialize Data Pipeline Engine", use_container_width=True):
            if st.session_state.dashboard.load_excel_data(uploaded_file):
                st.success("🎯 Workbook Connected & Database Topology Map Synchronized Successfully!")
                st.balloons()
    with col2:
        st.markdown("### ℹ️ Engine Topology Monitoring")
        if st.session_state.dashboard.data_loaded:
            st.info(f"✓ Matrix Node Verification: {len(st.session_state.dashboard.respondent_data):,} Records Active.")
        else:
            st.warning("⚠️ Connection Pipeline Status: Disconnected. Upload target schema database.")

def tab_02_executive():
    st.title("📊 Macro KPI Command Center")
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Active connection missing. Connect workbook via Tab 01 Gateway.")
        return
        
    c1, c2, c3, c4 = st.columns(4)
    with c1: create_kpi_card("National Index Mean", f"{st.session_state.dashboard.calculate_ikm_score():.2f}", "Likert Scale Range (1-5)", "accent")
    with c2: create_kpi_card("Early Warning Core Trigger", f"{st.session_state.dashboard.calculate_irk_score():.1f}%", "Indicator Items >= 3.8 Threshold", "danger")
    with c3: create_kpi_card("Active Matrix Respondents", f"{len(st.session_state.dashboard.respondent_data):,}", "Comprehensive Sample Node", "success")
    with c4: create_kpi_card("System Topology Health", "Operational Live", "2026 Core Sync Module", "warning")
    
    st.markdown("---")
    dim_scores = st.session_state.dashboard.calculate_dimension_scores()
    if dim_scores:
        dims = list(dim_scores.keys())
        means = [d['mean'] for d in dim_scores.values()]
        fig = go.Figure([go.Bar(x=dims, y=means, marker_color='#00D9FF', text=[f'{m:.2f}' for m in means], textposition='auto')])
        fig.update_layout(template='plotly_dark', title="Societal Tension Core Vector Profile Across Mapped Dimensions", height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def tab_03_geographic():
    st.title("🗺️ Stratified Demographic Multi-Vector Filtering")
    if not st.session_state.dashboard.data_loaded: return
    
    col1, col2 = st.columns([1, 3])
    with col1:
        filters = {}
        for geo in ['Zone', 'State', 'Urban_Rural', 'Income_Group']:
            if geo in st.session_state.dashboard.respondent_data.columns:
                filters[geo] = st.multiselect(f"Filter Node: {geo}", st.session_state.dashboard.get_filter_options(geo))
        filtered_df = st.session_state.dashboard.apply_filters({k:v for k,v in filters.items() if v})
    with col2:
        st.metric("Sub-Sample Node Size Range", f"{len(filtered_df):,} Matching Rows Active")
        if 'State' in filtered_df.columns:
            item_cols = [c for c in st.session_state.dashboard.get_item_columns() if c in filtered_df.columns]
            if item_cols:
                state_means = filtered_df.groupby('State')[item_cols].mean().mean(axis=1).sort_values()
                fig = px.bar(x=state_means.values, y=state_means.index, orientation='h', title="Regional Vulnerability Index Mean Performance Chart")
                fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

def tab_04_subindices():
    st.title("📈 9 Core Sub-Indices Analytics Matrix")
    if not st.session_state.dashboard.data_loaded: return
    subindices = st.session_state.dashboard.calculate_subindices_scores()
    sub_df = pd.DataFrame([{'Index Classification Field': k, 'Composite Structural Score (1-5)': f"{v['score']:.3f}", 'Operational Vulnerability Assessment Class': v['status']} for k,v in subindices.items()])
    st.dataframe(sub_df, use_container_width=True, hide_index=True)

def tab_05_items():
    st.title("🔍 Indicator Node Psychometric Data Excavation")
    if not st.session_state.dashboard.data_loaded: return
    scores = st.session_state.dashboard.calculate_item_scores()
    if scores:
        items_df = pd.DataFrame([{'Item Identifier Code': k, 'Arithmetic Mean Value': f"{v['mean']:.3f}", 'Standard Deviation Variance': f"{v['std']:.3f}", 'Completeness Target Check': v['count']} for k,v in scores.items()])
        st.dataframe(items_df.sort_values('Arithmetic Mean Value', ascending=False), use_container_width=True, hide_index=True)

def tab_06_qualitative():
    st.title("💬 NLP Text Content Vector Themes")
    if not st.session_state.dashboard.data_loaded: return
    if st.session_state.dashboard.qualitative_response is None:
        st.info("Missing 'qualitative_response' framework data table cluster matrix inside model file.")
        return
    themes = st.session_state.dashboard.detect_themes()
    if 'Main_Concerns' in themes:
        fig = px.pie(names=list(themes['Main_Concerns'].keys()), values=list(themes['Main_Concerns'].values()), title="Natural Language Theme Analysis Extraction Engine")
        fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def tab_07_theory():
    st.title("🧠 Theoretical Framework Structural Mapping Intelligence")
    if not st.session_state.dashboard.data_loaded: return
    th_analysis = st.session_state.dashboard.get_theory_analysis()
    if th_analysis:
        for th, data in th_analysis.items():
            st.markdown(f"#### 📚 {th} - ({data['count']} Indicator Variables Verified)")
            st.caption(f"**Structural Mapping Alignment:** Dimension Target: {', '.join(data['dimensions'])}")

def tab_08_pain_points():
    st.title("⚠️ Structural Pain Point Field Asset Matrix")
    if not st.session_state.dashboard.data_loaded: return
    qm = st.session_state.dashboard.questionnaire_master
    if qm is not None and 'Pain_Point' in qm.columns:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Top Pain Point Category Densities")
            pp_counts = qm['Pain_Point'].value_counts().head(15)
            st.bar_chart(pp_counts)
        with col2:
            st.markdown("### Unique Pain Points Count per Dimension Layer")
            dim_pain = qm.groupby('Dimension')['Pain_Point'].nunique().sort_values(ascending=False)
            st.dataframe(dim_pain, use_container_width=True)

def tab_09_tension():
    st.title("🔥 Crisis Escalation Profile Architecture")
    if not st.session_state.dashboard.data_loaded: return
    qm = st.session_state.dashboard.questionnaire_master
    if qm is not None and 'Tension_Point' in qm.columns:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Top Tension Flashpoint Metrics Distribution")
            tp_counts = qm['Tension_Point'].value_counts().head(15)
            st.bar_chart(tp_counts)
        with col2:
            st.markdown("### Unique Tension Structural Flashpoints Count per Dimension")
            dim_tension = qm.groupby('Dimension')['Tension_Point'].nunique().sort_values(ascending=False)
            st.dataframe(dim_tension, use_container_width=True)

def tab_10_hotspots():
    st.title("🚨 Early Warning System Map Flashpoints")
    if not st.session_state.dashboard.data_loaded: return
    hotspots = st.session_state.dashboard.get_hotspots()
    if hotspots:
        h_df = pd.DataFrame([{'Geographic Boundary Area': k, 'Mean Index Target (1-5)': f"{v['score']:.2f}", 'System Critical Alarm Trigger': v['status'], 'Risk Proportional Factor Weighting': f"{v['risk_level']:.1f}%"} for k,v in hotspots.items()])
        st.dataframe(h_df.sort_values('Mean Index Target (1-5)', ascending=False), use_container_width=True, hide_index=True)

def tab_11_intervention():
    st.title("💡 Policy Directive Recommendation Database Library")
    if not st.session_state.dashboard.data_loaded: return
    if st.session_state.dashboard.intervention_library is not None:
        st.dataframe(st.session_state.dashboard.intervention_library, use_container_width=True, hide_index=True)

def tab_12_media():
    st.title("📰 Scraped Media Vector Sentiment Tracker Engine")
    if not st.session_state.dashboard.data_loaded: return
    if st.session_state.dashboard.media_issue_summary is not None:
        st.dataframe(st.session_state.dashboard.media_issue_summary, use_container_width=True, hide_index=True)

def tab_13_fgd():
    st.title("👥 Expert FGD Panel Directive Documentation")
    if not st.session_state.dashboard.data_loaded: return
    if st.session_state.dashboard.fgd_expert is not None:
        st.dataframe(st.session_state.dashboard.fgd_expert, use_container_width=True, hide_index=True)

def tab_14_reports():
    st.title("📄 Dossier Ledger Generation Engine Module")
    if not st.session_state.dashboard.data_loaded: return
    title = st.text_input("Document Security Classification Header Subject", "National Societal Security Strategic Briefing Dossier")
    officer = st.text_input("Approving Executive Authority Full Name", "Director General")
    role = st.text_input("Institutional Structural Branch Affiliation", "National Security Analytics Division")
    if st.button("Compile Certified Data Summary Report", use_container_width=True):
        html = st.session_state.dashboard.generate_html_report(title, ['Dimension Analysis'], officer, role)
        st.download_button("⬇️ Download Compiled Intelligence Dossier File", html, "IKM_Security_Brief_Dossier.html", "text/html", use_container_width=True)

def tab_15_explorer():
    st.title("🔎 Structural Cell Row Raw Node Inspector")
    if not st.session_state.dashboard.data_loaded: return
    st.dataframe(st.session_state.dashboard.respondent_data.head(250), use_container_width=True)

# --- UTAMA DAN NAVIGATION LOGIK ---

def main():
    init_session()
    if not st.session_state.logged_in:
        login_page()
        return
        
    apply_premium_theme()
        
    st.markdown("""
        <div style='background: linear-gradient(90deg, rgba(26,27,77,0.4) 0%, rgba(5,11,26,0) 100%); padding: 20px; border-radius: 12px; border-left: 5px solid #FFD700; margin-bottom: 25px;'>
            <h1 style='color: #FFFFFF; margin:0; font-size: 32px; font-weight: 800;'>🏛️ Malaysian Societal Tension Index (IKM)</h1>
            <p style='color: #00D9FF; margin: 5px 0 0 0; font-size: 14px; font-weight: 500; letter-spacing: 0.5px;'>Strategic Governance Risk Assessment & Early Warning Analytics Engine</p>
        </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs([
        "01 Gateway", "02 Executive", "03 Demographics", "04 Indices", "05 Indicators",
        "06 NLP Narrative", "07 Core Theories", "08 Pain Points", "09 Flashpoints", 
        "10 EWS Warnings", "11 Policy Framework", "12 Media Stream", "13 FGD Review", 
        "14 Transcripts", "15 Cell Data"
    ])
    
    with tabs[0]: tab_01_gateway()
    with tabs[1]: tab_02_executive()
    with tabs[2]: tab_03_geographic()
    with tabs[3]: tab_04_subindices()
    with tabs[4]: tab_05_items()
    with tabs[5]: tab_06_qualitative()
    with tabs[6]: tab_07_theory()
    with tabs[7]: tab_08_pain_points()
    with tabs[8]: tab_09_tension()
    with tabs[9]: tab_10_hotspots()
    with tabs[10]: tab_11_intervention()
    with tabs[11]: tab_12_media()
    with tabs[12]: tab_13_fgd()
    with tabs[13]: tab_14_reports()
    with tabs[14]: tab_15_explorer()

if __name__ == "__main__":
    main()
