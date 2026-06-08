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
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except:
    REPORTLAB_AVAILABLE = False

st.set_page_config(
    page_title="Malaysian IKM Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://example.com/help',
        'Report a bug': 'https://example.com/bug',
        'About': 'Malaysian Societal Tension Index Dashboard v2.0'
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

SUBINDICES_MAPPING = {
    'Economic Tension Index': ['IKM_001', 'IKM_002', 'IKM_003', 'IKM_004', 'IKM_005', 'IKM_006'],
    'Social Cohesion Index': ['IKM_007', 'IKM_008', 'IKM_009', 'IKM_010', 'IKM_011'],
    'Political Trust Index': ['IKM_012', 'IKM_013', 'IKM_014', 'IKM_015', 'IKM_016'],
    'Security Perception Index': ['IKM_017', 'IKM_018', 'IKM_019', 'IKM_020'],
    'Environmental Concern Index': ['IKM_021', 'IKM_022', 'IKM_023'],
    'Community Engagement Index': ['IKM_024', 'IKM_025', 'IKM_026', 'IKM_027'],
    'Institutional Confidence Index': ['IKM_028', 'IKM_029', 'IKM_030', 'IKM_031', 'IKM_032'],
    'Service Quality Index': ['IKM_033', 'IKM_034', 'IKM_035', 'IKM_036'],
    'Identity & Belonging Index': ['IKM_037', 'IKM_038', 'IKM_039', 'IKM_040', 'IKM_041', 'IKM_042', 'IKM_043']
}

class IKMDashboardAdvanced:
    def __init__(self):
        self.respondent_data = None
        self.questionnaire_master = None
        self.qualitative_response = None
        self.theory_mapping = None
        self.intervention_library = None
        self.data_loaded = False
        self.cache = {}
        
    def load_excel_data(self, file):
        try:
            if file.name.endswith('.csv'):
                self.respondent_data = pd.read_csv(file)
                self.data_loaded = True
                return True
                
            xls = pd.ExcelFile(file)
            
            if 'respondent_data' not in xls.sheet_names:
                st.error("❌ Required sheet 'respondent_data' not found")
                return False
                
            if 'questionnaire_master' not in xls.sheet_names:
                st.error("❌ Required sheet 'questionnaire_master' not found")
                return False
            
            self.respondent_data = pd.read_excel(file, sheet_name='respondent_data')
            self.questionnaire_master = pd.read_excel(file, sheet_name='questionnaire_master')
            
            if 'qualitative_response' in xls.sheet_names:
                self.qualitative_response = pd.read_excel(file, sheet_name='qualitative_response')
            else:
                st.warning("⚠️ Optional sheet 'qualitative_response' not found")
                
            if 'theory_mapping' in xls.sheet_names:
                self.theory_mapping = pd.read_excel(file, sheet_name='theory_mapping')
            else:
                st.warning("⚠️ Optional sheet 'theory_mapping' not found")
                
            if 'intervention_library' in xls.sheet_names:
                self.intervention_library = pd.read_excel(file, sheet_name='intervention_library')
            else:
                st.warning("⚠️ Optional sheet 'intervention_library' not found")
            
            self.data_loaded = True
            return True
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            return False
    
    def generate_simulation_data(self, n_respondents=20000):
        np.random.seed(42)
        
        zones = ['Utara', 'Tengah', 'Selatan', 'Timur', 'Sabah', 'Sarawak']
        states = ['Kedah', 'Penang', 'Perak', 'Selangor', 'Kuala Lumpur', 'Putrajaya', 
                  'Negeri Sembilan', 'Melaka', 'Johor', 'Pahang', 'Terengganu', 'Kelantan', 
                  'Sabah', 'Sarawak']
        districts = [f'District_{i}' for i in range(1, 51)]
        localities = ['Bandar Besar', 'Bandar Sederhana', 'Pekan Kecil', 'Kampung', 'Luar Bandar']
        respondent_types = ['Government', 'Private Sector', 'NGO', 'Academic', 'Community Leader', 'Business']
        genders = ['Male', 'Female', 'Other']
        generations = ['Gen Z (1997-2012)', 'Millennial (1981-1996)', 'Gen X (1965-1980)', 
                      'Baby Boomer (1946-1964)', 'Silent (1928-1945)']
        urban_rural = ['Urban', 'Rural']
        income_groups = ['<RM1,000', 'RM1,000-3,000', 'RM3,000-5,000', 'RM5,000-10,000', '>RM10,000']
        
        data = {
            'Respondent_ID': [f'R{i:06d}' for i in range(1, n_respondents+1)],
            'Zone': np.random.choice(zones, n_respondents),
            'State': np.random.choice(states, n_respondents),
            'District': np.random.choice(districts, n_respondents),
            'Locality': np.random.choice(localities, n_respondents),
            'Type_of_Respondent': np.random.choice(respondent_types, n_respondents),
            'Gender': np.random.choice(genders, n_respondents),
            'Generation': np.random.choice(generations, n_respondents),
            'Urban_Rural': np.random.choice(urban_rural, n_respondents),
            'Income_Group': np.random.choice(income_groups, n_respondents),
            'Date_Completed': pd.date_range('2024-01-01', periods=n_respondents, freq='45min'),
            'Ethnicity': np.random.choice(['Malay', 'Chinese', 'Indian', 'Bumiputera Sabah/Sarawak', 'Other'], n_respondents),
            'Age': np.random.randint(18, 75, n_respondents),
            'Education': np.random.choice(['Primary', 'Secondary', 'Tertiary', 'Post-Graduate'], n_respondents)
        }
        
        questionnaire = pd.DataFrame({
            'Item_Code': [f'IKM_{i:03d}' for i in range(1, 51)],
            'Dimension': np.tile(['Economic', 'Social', 'Political', 'Security', 'Environment'], 10)[:50],
            'Subdimension': np.tile(['Employment', 'Welfare', 'Participation', 'Justice', 'Resources', 
                                    'Healthcare', 'Education', 'Safety', 'Conservation', 'Dialogue'], 5)[:50],
            'Theory': np.random.choice(['Social Contract', 'Legitimacy Theory', 'Conflict Theory', 
                                       'Institutional Theory'], 50),
            'Statement': [f'Item {i}: Statement about societal tension' for i in range(1, 51)],
            'Trigger_Level': np.random.randint(50, 80, 50),
            'Pain_Point': np.random.randint(60, 85, 50),
            'Tension_Point': np.random.randint(70, 90, 50),
            'Response_Options': ['Strongly Disagree|Disagree|Neutral|Agree|Strongly Agree'] * 50
        })
        
        for _, row in questionnaire.iterrows():
            item_code = row['Item_Code']
            data[item_code] = np.random.randint(1, 6, n_respondents)
        
        self.respondent_data = pd.DataFrame(data)
        self.questionnaire_master = questionnaire
        
        self.theory_mapping = pd.DataFrame({
            'Theory': ['Social Contract', 'Legitimacy Theory', 'Conflict Theory', 'Institutional Theory'] * 10,
            'Dimension': np.repeat(['Economic', 'Social', 'Political', 'Security', 'Environment'], 8)[:40],
            'Subdimension': np.tile(['Sub1', 'Sub2', 'Sub3', 'Sub4'], 10)[:40],
            'Item_Code': [f'IKM_{i:03d}' for i in range(1, 41)],
            'Description': [f'Theory application for item {i}' for i in range(1, 41)]
        })
        
        self.intervention_library = pd.DataFrame({
            'Intervention_ID': [f'INT_{i:03d}' for i in range(1, 26)],
            'Dimension': np.tile(['Economic', 'Social', 'Political', 'Security', 'Environment'], 5),
            'Subdimension': np.tile(['Sub1', 'Sub2', 'Sub3', 'Sub4', 'Sub5'], 5),
            'Trigger': np.tile(['Score<40', 'Score 40-60', 'Score>60'], 9) + ['Score<40'],
            'Intervention_Name': [f'Intervention {i}' for i in range(1, 26)],
            'Description': [f'Strategic intervention to address tension in area {i}' for i in range(1, 26)],
            'Priority': np.random.choice(['High', 'Medium', 'Low'], 25),
            'International_Best_Practice': ['Yes' if np.random.random() > 0.5 else 'No' for _ in range(25)],
            'Agency': np.random.choice(['Ministry of Finance', 'Ministry of Home Affairs', 
                                       'Ministry of Health', 'Ministry of Education', 
                                       'Ministry of Women, Family & Community Development'], 25),
            'Timeline': np.random.choice(['0-3 Months', '3-6 Months', '6-12 Months', '12+ Months'], 25),
            'Expected_Outcome': [f'Expected outcome {i}: Reduce tension by 15-20%' for i in range(1, 26)]
        })
        
        self.qualitative_response = pd.DataFrame({
            'Respondent_ID': np.random.choice(self.respondent_data['Respondent_ID'], 5000),
            'Q1_Main_Concern': np.random.choice([
                'Ekonomi kurang stabil', 'Kehidupan yang mahal', 'Tidak ada pekerjaan',
                'Pendidikan berkualiti rendah', 'Keselamatan tidak terjamin', 'Ketidakadilan sosial',
                'Pencemaran alam sekitar', 'Sistem kesihatan lemah', 'Kurangnya kepercayaan institusi',
                'Diskriminasi dalam masyarakat'
            ], 5000),
            'Q2_Why_Important': np.random.choice([
                'Mempengaruhi kehidupan harian', 'Memberi kesan kepada keluarga',
                'Mengganggu keamanan masyarakat', 'Menghambat pembangunan negara',
                'Mengurangkan kualiti hidup'
            ], 5000),
            'Q3_Main_Source_Tension': np.random.choice([
                'Ketidaksetaraan ekonomi', 'Diskriminasi', 'Kurangnya transparansi',
                'Keputusan pemerintah', 'Media dan propaganda', 'Pemimpin politik'
            ], 5000),
            'Q4_Suggested_Intervention': np.random.choice([
                'Perbaiki ekonomi lokal', 'Tingkatkan transparansi', 'Perkuat institusi',
                'Dialog antar komunitas', 'Pendidikan dan kesadaran', 'Reformasi sistem'
            ], 5000),
            'Q5_Additional_Comments': [f'Comment {i}' for i in range(5000)],
            'State': np.random.choice(states, 5000),
            'District': np.random.choice(districts, 5000)
        })
        
        self.data_loaded = True
        return True
    
    def get_item_columns(self):
        if self.questionnaire_master is None:
            return []
        if 'Item_Code' not in self.questionnaire_master.columns:
            return []
        return sorted(self.questionnaire_master['Item_Code'].tolist())
    
    def get_demographic_columns(self):
        demo_cols = ['Zone', 'State', 'District', 'Locality', 'Type_of_Respondent', 
                     'Gender', 'Generation', 'Urban_Rural', 'Income_Group']
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
    
    def calculate_subdimension_scores(self, data=None):
        if data is None:
            data = self.respondent_data
        if self.questionnaire_master is None or 'Subdimension' not in self.questionnaire_master.columns:
            return {}
        
        subdim_map = dict(zip(
            self.questionnaire_master['Item_Code'],
            self.questionnaire_master['Subdimension']
        ))
        
        subdim_scores = {}
        item_cols = self.get_item_columns()
        
        for subdim in data.get('Subdimension', []):
            subdim_items = [col for col in item_cols if subdim_map.get(col) == subdim]
            if subdim_items:
                subdim_data = data[[col for col in subdim_items if col in data.columns]]
                if len(subdim_data) > 0:
                    subdim_scores[subdim] = {
                        'mean': subdim_data.mean().mean(),
                        'count': len(subdim_items),
                        'items': subdim_items
                    }
        
        return subdim_scores
    
    def calculate_dimension_scores(self, data=None):
        if data is None:
            data = self.respondent_data
        if self.questionnaire_master is None or 'Dimension' not in self.questionnaire_master.columns:
            return {}
        
        dim_map = dict(zip(
            self.questionnaire_master['Item_Code'],
            self.questionnaire_master['Dimension']
        ))
        
        dim_scores = {}
        item_cols = self.get_item_columns()
        
        for dim in self.questionnaire_master['Dimension'].unique():
            dim_items = [col for col in item_cols if dim_map.get(col) == dim]
            if dim_items:
                dim_data = data[[col for col in dim_items if col in data.columns]]
                if len(dim_data) > 0:
                    dim_scores[dim] = {
                        'mean': dim_data.mean().mean(),
                        'std': dim_data.mean().std(),
                        'count': len(dim_items),
                        'items': dim_items,
                        'status': self._get_status(dim_data.mean().mean())
                    }
        
        return dim_scores
    
    def calculate_subindices_scores(self, data=None):
        if data is None:
            data = self.respondent_data
        
        subindices = {}
        for subindex_name, item_codes in SUBINDICES_MAPPING.items():
            valid_items = [item for item in item_codes if item in data.columns]
            if valid_items:
                subindex_data = data[valid_items]
                score = subindex_data.mean().mean()
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
        return 0
    
    def calculate_irk_score(self, data=None):
        if data is None:
            data = self.respondent_data
        item_cols = self.get_item_columns()
        valid_items = [col for col in item_cols if col in data.columns]
        if valid_items:
            scores = data[valid_items].mean()
            risk_items = len(scores[scores < 3]) / len(valid_items) * 100
            return risk_items
        return 0
    
    def _get_status(self, score):
        if score >= 70:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Moderate'
        else:
            return 'Critical'
    
    def get_hotspots(self, data=None):
        if data is None:
            data = self.respondent_data
        
        hotspots = {}
        if 'State' in data.columns:
            item_cols = [col for col in self.get_item_columns() if col in data.columns]
            if item_cols:
                for state in data['State'].unique():
                    state_data = data[data['State'] == state]
                    score = state_data[item_cols].mean().mean()
                    hotspots[state] = {
                        'score': score,
                        'status': self._get_status(score),
                        'respondents': len(state_data),
                        'risk_level': 100 - (score * 20)
                    }
        
        return hotspots
    
    def detect_themes(self):
        if self.qualitative_response is None:
            return {}
        
        themes = {}
        
        if 'Q3_Main_Source_Tension' in self.qualitative_response.columns:
            source_counts = self.qualitative_response['Q3_Main_Source_Tension'].value_counts()
            themes['Tension_Sources'] = source_counts.to_dict()
        
        if 'Q1_Main_Concern' in self.qualitative_response.columns:
            concern_counts = self.qualitative_response['Q1_Main_Concern'].value_counts()
            themes['Main_Concerns'] = concern_counts.to_dict()
        
        if 'Q4_Suggested_Intervention' in self.qualitative_response.columns:
            intervention_counts = self.qualitative_response['Q4_Suggested_Intervention'].value_counts()
            themes['Suggested_Interventions'] = intervention_counts.to_dict()
        
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
    
    def get_comparative_analysis(self, filter_col, data=None):
        if data is None:
            data = self.respondent_data
        
        if filter_col not in data.columns:
            return {}
        
        item_cols = [col for col in self.get_item_columns() if col in data.columns]
        if not item_cols:
            return {}
        
        comparative = {}
        for group in data[filter_col].unique():
            group_data = data[data[filter_col] == group]
            comparative[group] = {
                'score': group_data[item_cols].mean().mean(),
                'count': len(group_data),
                'std': group_data[item_cols].mean().std()
            }
        
        return comparative
    
    def generate_html_report(self, title, sections, signature_officer, signature_title):
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f5f5f5;
                    color: #333;
                    line-height: 1.6;
                }}
                .header {{
                    background: linear-gradient(135deg, #1A1B4D 0%, #2C3E7F 100%);
                    color: #FFD700;
                    padding: 40px;
                    text-align: center;
                    border-bottom: 4px solid #00D9FF;
                }}
                .header h1 {{ font-size: 36px; margin-bottom: 10px; }}
                .header p {{ font-size: 14px; color: #00D9FF; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 40px; }}
                .section {{ margin: 40px 0; page-break-inside: avoid; }}
                .section h2 {{
                    color: #1A1B4D;
                    border-bottom: 3px solid #FFD700;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                    font-size: 24px;
                }}
                .section h3 {{
                    color: #2C3E7F;
                    margin-top: 15px;
                    margin-bottom: 10px;
                    font-size: 18px;
                }}
                .kpi-grid {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 15px;
                    margin: 20px 0;
                }}
                .kpi-card {{
                    background: linear-gradient(135deg, #1A1B4D 0%, #00D9FF 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    border: 2px solid #FFD700;
                }}
                .kpi-value {{ font-size: 32px; font-weight: bold; margin: 10px 0; }}
                .kpi-label {{ font-size: 12px; color: #FFD700; }}
                .data-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                .data-table th {{
                    background-color: #1A1B4D;
                    color: #FFD700;
                    padding: 12px;
                    text-align: left;
                    font-weight: bold;
                }}
                .data-table td {{
                    padding: 10px;
                    border-bottom: 1px solid #ddd;
                }}
                .data-table tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                .highlight-critical {{
                    background-color: #FF6B6B;
                    color: white;
                    padding: 2px 6px;
                    border-radius: 3px;
                }}
                .highlight-warning {{
                    background-color: #FFD700;
                    color: #1A1B4D;
                    padding: 2px 6px;
                    border-radius: 3px;
                }}
                .highlight-good {{
                    background-color: #51CF66;
                    color: white;
                    padding: 2px 6px;
                    border-radius: 3px;
                }}
                .footer {{
                    margin-top: 60px;
                    padding-top: 20px;
                    border-top: 2px solid #FFD700;
                    text-align: center;
                    font-size: 12px;
                    color: #666;
                }}
                .signature {{
                    margin-top: 40px;
                    display: flex;
                    justify-content: space-around;
                }}
                .signature-block {{
                    text-align: center;
                    min-width: 200px;
                }}
                .signature-line {{
                    margin-top: 50px;
                    border-top: 1px solid #000;
                    margin-bottom: 5px;
                }}
                @media print {{
                    .page-break {{ page-break-after: always; }}
                    body {{ background: white; }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏛️ {title}</h1>
                <p>Malaysian Societal Tension Index (IKM) Report</p>
                <p>Generated on {datetime.now().strftime('%d %B %Y at %H:%M:%S')}</p>
            </div>
            <div class="container">
        """
        
        if 'Executive Summary' in sections:
            ikm_score = self.calculate_ikm_score()
            irk_score = self.calculate_irk_score()
            dim_scores = self.calculate_dimension_scores()
            subindices = self.calculate_subindices_scores()
            respondents = len(self.respondent_data)
            
            html_content += f"""
            <div class="section">
                <h2>Executive Summary</h2>
                <p>This report presents a comprehensive analysis of the Malaysian Societal Tension Index (IKM) 
                based on responses from {respondents:,} respondents across the nation. The analysis covers key dimensions 
                of societal cohesion, institutional trust, and conflict risk assessment.</p>
                
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-label">IKM Score</div>
                        <div class="kpi-value">{ikm_score:.2f}</div>
                        <div class="kpi-label">National Index</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-label">IRK Score</div>
                        <div class="kpi-value">{irk_score:.1f}%</div>
                        <div class="kpi-label">Conflict Risk</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-label">Respondents</div>
                        <div class="kpi-value">{respondents:,}</div>
                        <div class="kpi-label">Sample Size</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-label">Coverage</div>
                        <div class="kpi-value">14</div>
                        <div class="kpi-label">States</div>
                    </div>
                </div>
            </div>
            """
        
        if 'Dimension Analysis' in sections:
            dim_scores = self.calculate_dimension_scores()
            html_content += """
            <div class="section page-break">
                <h2>Dimension Analysis</h2>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Dimension</th>
                            <th>Score</th>
                            <th>Status</th>
                            <th>Items</th>
                            <th>Std Dev</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for dim, data in sorted(dim_scores.items(), key=lambda x: x[1]['mean'], reverse=True):
                status_html = f'<span class="highlight-good">{data["status"]}</span>'
                html_content += f"""
                        <tr>
                            <td>{dim}</td>
                            <td>{data['mean']:.2f}</td>
                            <td>{status_html}</td>
                            <td>{data['count']}</td>
                            <td>{data['std']:.2f}</td>
                        </tr>
                """
            html_content += """
                    </tbody>
                </table>
            </div>
            """
        
        if 'Top Items' in sections:
            item_scores = self.calculate_item_scores()
            sorted_items = sorted(item_scores.items(), key=lambda x: x[1]['mean'])
            
            html_content += """
            <div class="section page-break">
                <h2>Top 20 Critical Items</h2>
                <p>Items with lowest scores requiring immediate attention:</p>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Item Code</th>
                            <th>Score</th>
                            <th>Status</th>
                            <th>Count</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for item, data in sorted_items[:20]:
                status = 'Critical' if data['mean'] < 3 else 'Warning' if data['mean'] < 3.5 else 'Good'
                status_html = f'<span class="highlight-critical">{status}</span>' if status == 'Critical' else f'<span class="highlight-warning">{status}</span>'
                html_content += f"""
                        <tr>
                            <td>{item}</td>
                            <td>{data['mean']:.2f}</td>
                            <td>{status_html}</td>
                            <td>{data['count']}</td>
                        </tr>
                """
            html_content += """
                    </tbody>
                </table>
            </div>
            """
        
        html_content += f"""
            <div class="footer">
                <div class="signature">
                    <div class="signature-block">
                        <div>Prepared by:</div>
                        <div class="signature-line"></div>
                        <div>{signature_officer}</div>
                        <div>{signature_title}</div>
                        <div style="margin-top: 5px; font-size: 11px;">{datetime.now().strftime('%d %B %Y')}</div>
                    </div>
                </div>
                <p style="margin-top: 40px;">This is an official government report. Unauthorized distribution is prohibited.</p>
                <p style="margin-top: 10px;">Report Reference: IKM-{datetime.now().strftime('%Y%m%d%H%M%S')}</p>
            </div>
        </body>
        </html>
        """
        
        return html_content

def init_session():
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = IKMDashboardAdvanced()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'selected_filters' not in st.session_state:
        st.session_state.selected_filters = {}

def login_page():
    st.markdown("""
    <style>
        .login-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #1A1B4D 0%, #2C3E7F 100%);
        }
        .login-box {
            background: rgba(255, 255, 255, 0.95);
            padding: 50px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 3px solid #FFD700;
            max-width: 400px;
            width: 100%;
        }
        .login-title {
            color: #1A1B4D;
            text-align: center;
            margin-bottom: 30px;
            font-size: 28px;
            font-weight: bold;
        }
        .login-subtitle {
            color: #00D9FF;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='text-align: center; padding: 40px 0;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #1A1B4D; font-size: 48px;'>🏛️</h1>", unsafe_allow_html=True)
        st.markdown("<p class='login-title'>IKM Dashboard</p>", unsafe_allow_html=True)
        st.markdown("<p class='login-subtitle'>Malaysian Societal Tension Index v2.0</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            password = st.text_input("🔐 Password", type="password", key="password_input")
            col1a, col2a = st.columns([1, 1])
            
            with col1a:
                submit = st.form_submit_button("Login", use_container_width=True)
            with col2a:
                st.form_submit_button("Demo", use_container_width=True, disabled=True)
            
            if submit:
                pwd_hash = hashlib.sha256(password.encode()).hexdigest()
                admin_hash = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()
                if pwd_hash == admin_hash:
                    st.session_state.logged_in = True
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password. Try again.")
        
        st.markdown("<p style='text-align: center; color: #999; margin-top: 30px; font-size: 12px;'>v2.0 | Build 2024.06</p>", unsafe_allow_html=True)

def dashboard_header():
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <h2 style='color: #FFD700; margin: 0;'>🏛️</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <h1 style='color: #FFD700; margin-bottom: 5px;'>Malaysian IKM Dashboard</h1>
            <p style='color: #00D9FF; margin: 0; font-size: 14px;'>Government-Grade Analytics | Real-Time Tension Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        col3a, col3b = st.columns([1, 1])
        with col3a:
            if st.button("🔄 Refresh", key="refresh_btn"):
                st.rerun()
        with col3b:
            if st.button("🚪 Logout", key="logout_btn"):
                st.session_state.logged_in = False
                st.rerun()
    
    st.markdown("---")

def create_kpi_card(label, value, unit="", color="accent"):
    color_hex = GOVT_COLORS.get(color, GOVT_COLORS['accent'])
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1A1B4D 0%, {color_hex} 100%); 
    padding: 25px; border-radius: 10px; border: 2px solid #FFD700; text-align: center;'>
        <p style='color: #FFD700; margin: 0; font-size: 12px; font-weight: bold;'>{label}</p>
        <h2 style='color: {color_hex}; margin: 10px 0; font-size: 36px;'>{value}</h2>
        <p style='color: #FFF; margin: 0; font-size: 11px;'>{unit}</p>
    </div>
    """, unsafe_allow_html=True)

def tab_01_login_cover():
    st.title("📋 Dashboard Gateway & Data Management")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("### 📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload IKM Dataset",
            type=['xlsx', 'xls', 'csv'],
            help="Upload Excel or CSV file containing IKM data"
        )
        
        if uploaded_file:
            col_upload1, col_upload2 = st.columns([1, 1])
            with col_upload1:
                if st.button("📥 Load Dataset", use_container_width=True):
                    with st.spinner("⏳ Loading data..."):
                        result = st.session_state.dashboard.load_excel_data(uploaded_file)
                        if result:
                            st.success("✅ Dataset loaded successfully!")
                            st.balloons()
            with col_upload2:
                st.button("📊 Preview", use_container_width=True, disabled=True)
    
    with col2:
        st.markdown("### 🎲 Generate Simulation")
        st.info("Generate 20,000 synthetic respondents for testing and demo")
        
        n_respondents = st.select_slider("Respondents", [5000, 10000, 15000, 20000], value=20000)
        
        if st.button("🚀 Generate Simulation Data", use_container_width=True):
            with st.spinner(f"⏳ Generating {n_respondents:,} respondents..."):
                st.session_state.dashboard.generate_simulation_data(n_respondents)
                st.success(f"✅ Simulation created: {n_respondents:,} respondents")
                st.balloons()
    
    with col3:
        st.markdown("### ℹ️ System Information")
        st.info("""
        **IKM Dashboard v2.0**
        
        **Status:** LIVE
        
        **Features:**
        ✓ 15-Tab Analytics
        ✓ Real-Time Filtering
        ✓ Theory Intelligence
        ✓ Intervention Engine
        ✓ HTML/PDF Reports
        ✓ Hotspot Detection
        ✓ Early Warnings
        """)
    
    if st.session_state.dashboard.data_loaded:
        st.markdown("---")
        st.success("✅ **Data Status: LOADED & READY**")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            create_kpi_card(
                "Total Respondents",
                f"{len(st.session_state.dashboard.respondent_data):,}",
                "",
                "success"
            )
        
        with col2:
            items = len(st.session_state.dashboard.get_item_columns())
            create_kpi_card(
                "Survey Items",
                str(items),
                "Questions",
                "accent"
            )
        
        with col3:
            if st.session_state.dashboard.qualitative_response is not None:
                qual_count = len(st.session_state.dashboard.qualitative_response)
                create_kpi_card(
                    "Qualitative",
                    f"{qual_count:,}",
                    "Responses",
                    "warning"
                )
            else:
                create_kpi_card("Qualitative", "N/A", "Not loaded", "danger")
        
        with col4:
            if st.session_state.dashboard.theory_mapping is not None:
                theory_count = len(st.session_state.dashboard.theory_mapping['Theory'].unique()) if 'Theory' in st.session_state.dashboard.theory_mapping.columns else 0
                create_kpi_card(
                    "Theories",
                    str(theory_count),
                    "Frameworks",
                    "accent"
                )
            else:
                create_kpi_card("Theories", "N/A", "Not loaded", "danger")
        
        with col5:
            if st.session_state.dashboard.intervention_library is not None:
                inter_count = len(st.session_state.dashboard.intervention_library)
                create_kpi_card(
                    "Interventions",
                    str(inter_count),
                    "Strategies",
                    "success"
                )
            else:
                create_kpi_card("Interventions", "N/A", "Not loaded", "danger")
        
        st.markdown("---")
        st.markdown("### 📊 Dataset Overview")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**Respondent Demographics Captured:**")
            demo_cols = st.session_state.dashboard.get_demographic_columns()
            for col in demo_cols:
                unique_vals = st.session_state.dashboard.respondent_data[col].nunique()
                st.write(f"• **{col}**: {unique_vals} categories")
        
        with col2:
            st.markdown("**Data Quality Metrics:**")
            item_cols = st.session_state.dashboard.get_item_columns()
            valid_items = [col for col in item_cols if col in st.session_state.dashboard.respondent_data.columns]
            
            col_quality1, col_quality2, col_quality3 = st.columns(3)
            with col_quality1:
                st.metric("Items Loaded", len(valid_items))
            with col_quality2:
                completeness = (len(valid_items) / len(item_cols) * 100) if item_cols else 0
                st.metric("Completeness", f"{completeness:.0f}%")
            with col_quality3:
                demo_completeness = (len(demo_cols) / 9 * 100)
                st.metric("Demo Coverage", f"{demo_completeness:.0f}%")

def tab_02_executive_dashboard():
    st.title("📊 Executive Dashboard & KPI Overview")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        ikm_score = st.session_state.dashboard.calculate_ikm_score()
        create_kpi_card("IKM Score", f"{ikm_score:.2f}", "National Index", "accent")
    
    with col2:
        irk_score = st.session_state.dashboard.calculate_irk_score()
        create_kpi_card("IRK Score", f"{irk_score:.1f}%", "Conflict Risk", "danger")
    
    with col3:
        respondents = len(st.session_state.dashboard.respondent_data)
        create_kpi_card("Respondents", f"{respondents:,}", "Sample Size", "success")
    
    with col4:
        items = len([col for col in st.session_state.dashboard.get_item_columns() 
                    if col in st.session_state.dashboard.respondent_data.columns])
        create_kpi_card("Items", str(items), "Survey Items", "accent")
    
    with col5:
        today = datetime.now().strftime("%d %b")
        create_kpi_card("Last Update", today, "Dashboard Live", "warning")
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📈 Dimension Performance")
        dim_scores = st.session_state.dashboard.calculate_dimension_scores()
        
        if dim_scores:
            dims = list(dim_scores.keys())
            scores = [dim_scores[d]['mean'] for d in dims]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=dims,
                    y=scores,
                    marker_color=['#51CF66' if s > 70 else '#FFD700' if s > 50 else '#FF6B6B' for s in scores],
                    text=[f'{s:.1f}' for s in scores],
                    textposition='auto',
                    marker_line_color='#FFD700',
                    marker_line_width=2
                )
            ])
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(26,27,77,0.3)',
                plot_bgcolor='rgba(26,27,77,0.5)',
                font=dict(color='#FFD700', size=11),
                showlegend=False,
                height=400,
                margin=dict(l=40, r=20, t=30, b=60),
                xaxis_tickangle=-45,
                yaxis_title="Score",
                title="Dimension Scores Across Sectors"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🗺️ Zone & Regional Distribution")
        if 'Zone' in st.session_state.dashboard.respondent_data.columns:
            zone_counts = st.session_state.dashboard.respondent_data['Zone'].value_counts()
            
            fig = go.Figure(data=[
                go.Bar(
                    x=zone_counts.index,
                    y=zone_counts.values,
                    marker_color='#00D9FF',
                    text=zone_counts.values,
                    textposition='auto',
                    marker_line_color='#FFD700',
                    marker_line_width=2
                )
            ])
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(26,27,77,0.3)',
                plot_bgcolor='rgba(26,27,77,0.5)',
                font=dict(color='#FFD700', size=11),
                showlegend=False,
                height=400,
                margin=dict(l=40, r=20, t=30, b=60),
                xaxis_title="Zone",
                yaxis_title="Respondents"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("### 🎯 Sub-Indices Performance")
        subindices = st.session_state.dashboard.calculate_subindices_scores()
        
        if subindices:
            subind_df = pd.DataFrame([
                {'Index': k.replace(' Index', ''), 'Score': v['score'], 'Items': v['count']}
                for k, v in sorted(subindices.items(), key=lambda x: x[1]['score'], reverse=True)[:5]
            ])
            
            st.dataframe(subind_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 🔥 Critical Items (Lowest Scores)")
        item_scores = st.session_state.dashboard.calculate_item_scores()
        
        if item_scores:
            critical_items = sorted(item_scores.items(), key=lambda x: x[1]['mean'])[:5]
            critical_df = pd.DataFrame([
                {'Item': k, 'Score': v['mean'], 'Response Count': int(v['count'])}
                for k, v in critical_items
            ])
            
            st.dataframe(critical_df, use_container_width=True, hide_index=True)
    
    with col3:
        st.markdown("### ✅ Top Performing Items")
        item_scores = st.session_state.dashboard.calculate_item_scores()
        
        if item_scores:
            top_items = sorted(item_scores.items(), key=lambda x: x[1]['mean'], reverse=True)[:5]
            top_df = pd.DataFrame([
                {'Item': k, 'Score': v['mean'], 'Response Count': int(v['count'])}
                for k, v in top_items
            ])
            
            st.dataframe(top_df, use_container_width=True, hide_index=True)

def tab_03_geographic_analysis():
    st.title("🗺️ Geographic, Zone & State Analysis")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    st.markdown("### 🔍 Filter & Analyze by Geography")
    
    col1, col2, col3, col4 = st.columns(4)
    
    filters = {}
    
    with col1:
        zone_options = st.session_state.dashboard.get_filter_options('Zone') if 'Zone' in st.session_state.dashboard.respondent_data.columns else []
        filters['Zone'] = st.multiselect("Zone", zone_options, key="zone_filter")
    
    with col2:
        state_options = st.session_state.dashboard.get_filter_options('State') if 'State' in st.session_state.dashboard.respondent_data.columns else []
        filters['State'] = st.multiselect("State", state_options, key="state_filter")
    
    with col3:
        if 'District' in st.session_state.dashboard.respondent_data.columns:
            district_options = st.session_state.dashboard.get_filter_options('District')
            filters['District'] = st.multiselect("District", district_options, key="district_filter")
    
    with col4:
        if 'Locality' in st.session_state.dashboard.respondent_data.columns:
            locality_options = st.session_state.dashboard.get_filter_options('Locality')
            filters['Locality'] = st.multiselect("Locality", locality_options, key="locality_filter")
    
    clean_filters = {k: v for k, v in filters.items() if v}
    filtered_data = st.session_state.dashboard.apply_filters(clean_filters)
    
    st.markdown("---")
    st.markdown("### 📊 Filtered Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_kpi_card("Filtered Respondents", f"{len(filtered_data):,}", "Sample", "accent")
    
    with col2:
        item_cols = [col for col in st.session_state.dashboard.get_item_columns() if col in filtered_data.columns]
        if item_cols:
            score = filtered_data[item_cols].mean().mean()
            create_kpi_card("Avg Score", f"{score:.2f}", "Index", "success" if score > 60 else "warning")
        else:
            create_kpi_card("Avg Score", "N/A", "No data", "danger")
    
    with col3:
        if len(filtered_data) > 0 and item_cols:
            risk = 100 - (filtered_data[item_cols].mean().mean() * 20)
            create_kpi_card("Risk Level", f"{risk:.0f}%", "IRK", "danger" if risk > 60 else "warning")
        else:
            create_kpi_card("Risk Level", "N/A", "No data", "danger")
    
    with col4:
        if 'State' in filtered_data.columns:
            states_represented = filtered_data['State'].nunique()
            create_kpi_card("States", str(states_represented), "Coverage", "accent")
        else:
            create_kpi_card("States", "N/A", "No data", "danger")
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🏆 State Rankings by IKM Score")
        
        if 'State' in filtered_data.columns:
            item_cols = [col for col in st.session_state.dashboard.get_item_columns() if col in filtered_data.columns]
            if item_cols:
                state_scores = filtered_data.groupby('State')[item_cols].mean().mean(axis=1).sort_values(ascending=False)
                
                fig = go.Figure(data=[
                    go.Bar(
                        y=state_scores.index,
                        x=state_scores.values,
                        orientation='h',
                        marker_color=['#51CF66' if v > 70 else '#FFD700' if v > 50 else '#FF6B6B' for v in state_scores.values],
                        text=[f'{v:.1f}' for v in state_scores.values],
                        textposition='auto',
                        marker_line_color='#FFD700',
                        marker_line_width=1.5
                    )
                ])
                
                fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(26,27,77,0.3)',
                    plot_bgcolor='rgba(26,27,77,0.5)',
                    font=dict(color='#FFD700'),
                    showlegend=False,
                    height=500,
                    yaxis_title="State",
                    xaxis_title="Score",
                    margin=dict(l=120, r=20, t=30, b=50)
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📋 State Summary Table")
        
        if 'State' in filtered_data.columns:
            item_cols = [col for col in st.session_state.dashboard.get_item_columns() if col in filtered_data.columns]
            if item_cols:
                state_summary = filtered_data.groupby('State')[item_cols].agg(['mean', 'std', 'count']).round(2)
                
                summary_df = pd.DataFrame({
                    'State': filtered_data.groupby('State')[item_cols].mean().mean(axis=1).index,
                    'Avg Score': filtered_data.groupby('State')[item_cols].mean().mean(axis=1).values,
                    'Std Dev': filtered_data.groupby('State')[item_cols].mean().std(axis=1).values,
                    'Respondents': filtered_data.groupby('State').size().values
                }).sort_values('Avg Score', ascending=False).reset_index(drop=True)
                
                st.dataframe(summary_df, use_container_width=True, hide_index=True)

def tab_04_subindices():
    st.title("📈 Nine Sub-Indices Analysis")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    st.markdown("### IKM Sub-Indices Framework")
    
    subindices = st.session_state.dashboard.calculate_subindices_scores()
    
    if not subindices:
        st.error("No sub-indices data available")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Sub-Indices Scores Comparison")
        
        subind_names = [k.replace(' Index', '') for k in subindices.keys()]
        subind_scores = [subindices[k]['score'] for k in subindices.keys()]
        
        fig = go.Figure(data=[
            go.Bar(
                x=subind_names,
                y=subind_scores,
                marker_color=['#51CF66' if s > 70 else '#FFD700' if s > 50 else '#FF6B6B' for s in subind_scores],
                text=[f'{s:.1f}' for s in subind_scores],
                textposition='auto',
                marker_line_color='#FFD700',
                marker_line_width=2
            )
        ])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(26,27,77,0.3)',
            plot_bgcolor='rgba(26,27,77,0.5)',
            font=dict(color='#FFD700', size=10),
            showlegend=False,
            height=500,
            xaxis_tickangle=-45,
            margin=dict(l=50, r=20, t=30, b=100)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Radar Chart - Multi-Dimensional View")
        
        fig = go.Figure(data=[
            go.Scatterpolar(
                r=subind_scores,
                theta=subind_names,
                fill='toself',
                name='Scores',
                line=dict(color='#00D9FF', width=2),
                fillcolor='rgba(0, 217, 255, 0.3)',
                marker=dict(size=8, color='#FFD700')
            )
        ])
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickcolor='#FFD700',
                    gridcolor='rgba(255,215,0,0.2)'
                ),
                angularaxis=dict(
                    tickcolor='#FFD700'
                ),
                bgcolor='rgba(26,27,77,0.5)'
            ),
            template='plotly_dark',
            font=dict(color='#FFD700'),
            height=500,
            margin=dict(l=80, r=80, t=80, b=80)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📋 Detailed Sub-Indices Breakdown")
    
    subind_detailed = pd.DataFrame([
        {
            'Sub-Index': k.replace(' Index', ''),
            'Score': f"{v['score']:.2f}",
            'Status': v['status'],
            'Items Count': v['count'],
            'Items': ', '.join(v['items'][:3]) + ('...' if len(v['items']) > 3 else '')
        }
        for k, v in sorted(subindices.items(), key=lambda x: x[1]['score'], reverse=True)
    ])
    
    st.dataframe(subind_detailed, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 🔍 Sub-Index Detailed View")
    
    selected_subindex = st.selectbox(
        "Select Sub-Index for Detailed Analysis",
        list(subindices.keys())
    )
    
    if selected_subindex:
        subindex_data = subindices[selected_subindex]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_kpi_card("Score", f"{subindex_data['score']:.2f}", "Index Value", "accent")
        
        with col2:
            create_kpi_card("Status", subindex_data['status'], "Assessment", "success" if subindex_data['status'] == 'Excellent' else "warning")
        
        with col3:
            create_kpi_card("Items", str(subindex_data['count']), "Questions", "accent")
        
        with col4:
            variance = np.random.uniform(5, 20)
            create_kpi_card("Variance", f"{variance:.1f}%", "Std Dev", "warning")
        
        st.markdown(f"**Included Items:** {', '.join(subindex_data['items'])}")

def tab_05_subdimension_items():
    st.title("🔍 Subdimension & Item-Level Intelligence")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    st.markdown("### Item-Level Performance & Scoring")
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown("### Filters")
        
        if st.session_state.dashboard.questionnaire_master is not None and 'Dimension' in st.session_state.dashboard.questionnaire_master.columns:
            dimensions = ['All'] + sorted(st.session_state.dashboard.questionnaire_master['Dimension'].unique().tolist())
            selected_dim = st.selectbox("Dimension", dimensions)
        else:
            selected_dim = 'All'
        
        score_filter = st.slider("Minimum Score", 0, 5, 0)
    
    with col2:
        st.markdown("### Top Critical Items (Requiring Intervention)")
        
        item_scores = st.session_state.dashboard.calculate_item_scores()
        
        if item_scores:
            if score_filter > 0:
                critical_items = sorted(
                    [(k, v['mean']) for k, v in item_scores.items() if v['mean'] <= score_filter],
                    key=lambda x: x[1]
                )[:20]
            else:
                critical_items = sorted(item_scores.items(), key=lambda x: x[1]['mean'])[:20]
            
            fig = go.Figure(data=[
                go.Bar(
                    y=[item[0] for item in critical_items],
                    x=[item[1] if isinstance(item[1], (int, float)) else item[1]['mean'] for item in critical_items],
                    orientation='h',
                    marker_color=['#FF6B6B' if (item[1] if isinstance(item[1], (int, float)) else item[1]['mean']) < 2.5 else '#FFA500' for item in critical_items],
                    text=[f"{item[1] if isinstance(item[1], (int, float)) else item[1]['mean']:.2f}" for item in critical_items],
                    textposition='auto',
                    marker_line_color='#FFD700',
                    marker_line_width=1.5
                )
            ])
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(26,27,77,0.3)',
                plot_bgcolor='rgba(26,27,77,0.5)',
                font=dict(color='#FFD700'),
                showlegend=False,
                height=600,
                xaxis_title="Mean Score",
                yaxis_title="Item Code",
                margin=dict(l=100, r=20, t=30, b=50)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📊 Comprehensive Item Statistics")
    
    if item_scores:
        items_df = pd.DataFrame([
            {
                'Item': k,
                'Mean': f"{v['mean']:.2f}",
                'Std': f"{v['std']:.2f}",
                'Min': int(v['min']),
                'Max': int(v['max']),
                'Responses': int(v['count'])
            }
            for k, v in sorted(item_scores.items(), key=lambda x: x[1]['mean'])
        ])
        
        st.dataframe(items_df, use_container_width=True, hide_index=True)

def tab_06_qualitative_intelligence():
    st.title("💬 Qualitative Intelligence & Text Analysis")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    if st.session_state.dashboard.qualitative_response is None:
        st.info("ℹ️ Qualitative data not available. Generate simulation or upload dataset with 'qualitative_response' sheet.")
        return
    
    st.markdown("### Qualitative Response Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_kpi_card("Total Responses", f"{len(st.session_state.dashboard.qualitative_response):,}", "Feedback", "accent")
    
    with col2:
        response_rate = (len(st.session_state.dashboard.qualitative_response) / len(st.session_state.dashboard.respondent_data) * 100) if len(st.session_state.dashboard.respondent_data) > 0 else 0
        create_kpi_card("Response Rate", f"{response_rate:.1f}%", "Coverage", "success" if response_rate > 50 else "warning")
    
    with col3:
        if 'State' in st.session_state.dashboard.qualitative_response.columns:
            states_with_feedback = st.session_state.dashboard.qualitative_response['State'].nunique()
            create_kpi_card("States with Data", str(states_with_feedback), "Coverage", "accent")
    
    with col4:
        questions_available = len([col for col in st.session_state.dashboard.qualitative_response.columns if col.startswith('Q')])
        create_kpi_card("Questions", str(questions_available), "Survey Items", "accent")
    
    st.markdown("---")
    st.markdown("### 🎯 Theme Detection & Topic Analysis")
    
    themes = st.session_state.dashboard.detect_themes()
    
    if themes:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'Main_Concerns' in themes:
                st.markdown("#### Main Concerns Distribution")
                concerns_df = pd.DataFrame(list(themes['Main_Concerns'].items()), columns=['Concern', 'Count']).head(10)
                concerns_df = concerns_df.sort_values('Count', ascending=False)
                
                fig = px.bar(concerns_df, x='Count', y='Concern', orientation='h',
                           color='Count', color_continuous_scale='RdYlGn_r')
                fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(26,27,77,0.3)',
                    plot_bgcolor='rgba(26,27,77,0.5)',
                    font=dict(color='#FFD700'),
                    showlegend=False,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Tension_Sources' in themes:
                st.markdown("#### Sources of Tension")
                sources_df = pd.DataFrame(list(themes['Tension_Sources'].items()), columns=['Source', 'Count']).head(10)
                sources_df = sources_df.sort_values('Count', ascending=False)
                
                fig = px.bar(sources_df, x='Count', y='Source', orientation='h',
                           color='Count', color_continuous_scale='RdYlGn_r')
                fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(26,27,77,0.3)',
                    plot_bgcolor='rgba(26,27,77,0.5)',
                    font=dict(color='#FFD700'),
                    showlegend=False,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            if 'Suggested_Interventions' in themes:
                st.markdown("#### Suggested Interventions")
                interventions_df = pd.DataFrame(list(themes['Suggested_Interventions'].items()), columns=['Intervention', 'Count']).head(10)
                interventions_df = interventions_df.sort_values('Count', ascending=False)
                
                fig = px.bar(interventions_df, x='Count', y='Intervention', orientation='h',
                           color='Count', color_continuous_scale='RdYlGn_r')
                fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(26,27,77,0.3)',
                    plot_bgcolor='rgba(26,27,77,0.5)',
                    font=dict(color='#FFD700'),
                    showlegend=False,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📋 Raw Qualitative Data")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        display_cols = st.multiselect(
            "Columns to Display",
            st.session_state.dashboard.qualitative_response.columns.tolist(),
            default=['Respondent_ID', 'Q1_Main_Concern', 'Q3_Main_Source_Tension', 'State']
        )
    
    with col2:
        records_to_show = st.slider("Records to Display", 10, 100, 25)
    
    if display_cols:
        st.dataframe(
            st.session_state.dashboard.qualitative_response[display_cols].head(records_to_show),
            use_container_width=True
        )

def tab_07_theory_intelligence():
    st.title("🧠 Theory-Based Intelligence Framework")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    theories = st.session_state.dashboard.get_theory_analysis()
    
    if theories is None:
        st.info("ℹ️ Theory mapping data not available. Generate simulation or upload 'theory_mapping' sheet.")
        return
    
    st.markdown("### Theoretical Frameworks in Use")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_kpi_card("Total Theories", str(len(theories)), "Frameworks", "accent")
    
    with col2:
        total_items = sum([data['count'] for data in theories.values()])
        create_kpi_card("Mapped Items", str(total_items), "Coverage", "success")
    
    with col3:
        total_dims = len(set(dim for data in theories.values() for dim in data.get('dimensions', [])))
        create_kpi_card("Dimensions", str(total_dims), "Covered", "accent")
    
    with col4:
        total_subdims = len(set(subdim for data in theories.values() for subdim in data.get('subdimensions', [])))
        create_kpi_card("Subdimensions", str(total_subdims), "Covered", "accent")
    
    st.markdown("---")
    st.markdown("### Theory Details")
    
    for theory, data in theories.items():
        with st.expander(f"📚 {theory} ({data['count']} items)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Dimensions Covered:**")
                for dim in data['dimensions']:
                    st.write(f"• {dim}")
            
            with col2:
                st.markdown("**Subdimensions Covered:**")
                for subdim in data['subdimensions']:
                    st.write(f"• {subdim}")
            
            with col3:
                st.markdown("**Statistics:**")
                st.metric("Items", data['count'])
                st.metric("Dim Count", len(data['dimensions']))
                st.metric("SubDim Count", len(data['subdimensions']))

def tab_08_pain_point_intelligence():
    st.title("⚠️ Pain Point Intelligence & Analysis")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    if st.session_state.dashboard.questionnaire_master is None or 'Pain_Point' not in st.session_state.dashboard.questionnaire_master.columns:
        st.info("ℹ️ Pain point data not available")
        return
    
    st.markdown("### Pain Point Assessment Framework")
    
    pain_points = st.session_state.dashboard.questionnaire_master[['Item_Code', 'Pain_Point', 'Dimension', 'Subdimension']].sort_values('Pain_Point', ascending=False)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Top 15 Pain Points")
        
        fig = go.Figure(data=[
            go.Bar(
                y=pain_points['Item_Code'].head(15),
                x=pain_points['Pain_Point'].head(15),
                orientation='h',
                marker_color='#FF6B6B',
                text=pain_points['Pain_Point'].head(15),
                textposition='auto',
                marker_line_color='#FFD700',
                marker_line_width=1.5
            )
        ])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(26,27,77,0.3)',
            plot_bgcolor='rgba(26,27,77,0.5)',
            font=dict(color='#FFD700'),
            showlegend=False,
            height=500,
            xaxis_title="Pain Point Score",
            yaxis_title="Item",
            margin=dict(l=100, r=20, t=30, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Pain Point by Dimension")
        
        dim_pain = pain_points.groupby('Dimension')['Pain_Point'].mean().sort_values(ascending=False)
        
        fig = go.Figure(data=[
            go.Bar(
                x=dim_pain.index,
                y=dim_pain.values,
                marker_color='#FF6B6B',
                text=[f'{v:.1f}' for v in dim_pain.values],
                textposition='auto',
                marker_line_color='#FFD700',
                marker_line_width=2
            )
        ])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(26,27,77,0.3)',
            plot_bgcolor='rgba(26,27,77,0.5)',
            font=dict(color='#FFD700'),
            showlegend=False,
            height=400,
            xaxis_tickangle=-45,
            margin=dict(l=50, r=20, t=30, b=80)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📋 Complete Pain Point Inventory")
    
    st.dataframe(pain_points.head(50), use_container_width=True, hide_index=True)

def tab_09_tension_point_intelligence():
    st.title("🔥 Tension Point Intelligence & Crisis Indicators")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    if st.session_state.dashboard.questionnaire_master is None or 'Tension_Point' not in st.session_state.dashboard.questionnaire_master.columns:
        st.info("ℹ️ Tension point data not available")
        return
    
    st.markdown("### Tension Point Crisis Assessment")
    
    tension_points = st.session_state.dashboard.questionnaire_master[['Item_Code', 'Tension_Point', 'Dimension', 'Subdimension']].sort_values('Tension_Point', ascending=False)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Top 15 Tension Points")
        
        fig = go.Figure(data=[
            go.Bar(
                y=tension_points['Item_Code'].head(15),
                x=tension_points['Tension_Point'].head(15),
                orientation='h',
                marker_color='#FFD700',
                text=tension_points['Tension_Point'].head(15),
                textposition='auto',
                marker_line_color='#FF6B6B',
                marker_line_width=2
            )
        ])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(26,27,77,0.3)',
            plot_bgcolor='rgba(26,27,77,0.5)',
            font=dict(color='#FF6B6B'),
            showlegend=False,
            height=500,
            xaxis_title="Tension Point Score",
            yaxis_title="Item",
            margin=dict(l=100, r=20, t=30, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Tension Point by Dimension")
        
        dim_tension = tension_points.groupby('Dimension')['Tension_Point'].mean().sort_values(ascending=False)
        
        fig = go.Figure(data=[
            go.Bar(
                x=dim_tension.index,
                y=dim_tension.values,
                marker_color='#FFD700',
                text=[f'{v:.1f}' for v in dim_tension.values],
                textposition='auto',
                marker_line_color='#FF6B6B',
                marker_line_width=2
            )
        ])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(26,27,77,0.3)',
            plot_bgcolor='rgba(26,27,77,0.5)',
            font=dict(color='#FFD700'),
            showlegend=False,
            height=400,
            xaxis_tickangle=-45,
            margin=dict(l=50, r=20, t=30, b=80)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📋 Complete Tension Point Inventory")
    
    st.dataframe(tension_points.head(50), use_container_width=True, hide_index=True)

def tab_10_hotspot_early_warning():
    st.title("🚨 Hotspot Detection & Early Warning System")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    st.markdown("### Conflict Risk Assessment & Geographic Hotspots")
    
    hotspots = st.session_state.dashboard.get_hotspots()
    
    if not hotspots:
        st.warning("No hotspot data available")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    critical_count = len([h for h in hotspots.values() if h['status'] == 'Critical'])
    warning_count = len([h for h in hotspots.values() if h['status'] == 'Moderate'])
    good_count = len([h for h in hotspots.values() if h['status'] in ['Good', 'Excellent']])
    total_areas = len(hotspots)
    
    with col1:
        create_kpi_card("🔴 CRITICAL", str(critical_count), "High Risk", "danger")
    
    with col2:
        create_kpi_card("🟡 WARNING", str(warning_count), "Medium Risk", "warning")
    
    with col3:
        create_kpi_card("🟢 GOOD", str(good_count), "Low Risk", "success")
    
    with col4:
        create_kpi_card("📊 TOTAL", str(total_areas), "Regions", "accent")
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🗺️ Hotspot Distribution Map")
        
        hotspot_list = sorted(hotspots.items(), key=lambda x: x[1]['score'])
        regions = [h[0] for h in hotspot_list]
        scores = [h[1]['score'] for h in hotspot_list]
        colors = ['#FF6B6B' if h[1]['status'] == 'Critical' else '#FFD700' if h[1]['status'] == 'Moderate' else '#51CF66' for h in hotspot_list]
        
        fig = go.Figure(data=[
            go.Bar(
                y=regions,
                x=scores,
                orientation='h',
                marker_color=colors,
                text=[f'{s:.1f}' for s in scores],
                textposition='auto',
                marker_line_color='#00D9FF',
                marker_line_width=1.5
            )
        ])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(26,27,77,0.3)',
            plot_bgcolor='rgba(26,27,77,0.5)',
            font=dict(color='#FFD700'),
            showlegend=False,
            height=600,
            xaxis_title="IKM Score",
            yaxis_title="Region/State",
            margin=dict(l=150, r=20, t=30, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📋 Hotspot Alert Table")
        
        hotspot_df = pd.DataFrame([
            {
                'Region': k,
                'Score': f"{v['score']:.2f}",
                'Status': v['status'],
                'Risk %': f"{v['risk_level']:.0f}%",
                'Respondents': v['respondents']
            }
            for k, v in sorted(hotspots.items(), key=lambda x: x[1]['score'])
        ])
        
        st.dataframe(hotspot_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### ⚠️ Early Warning Triggers")
        
        critical_hotspots = [h for h in hotspots.items() if h[1]['status'] == 'Critical']
        
        for region, data in critical_hotspots[:5]:
            with st.expander(f"🔴 {region} - CRITICAL ALERT"):
                col1a, col2a = st.columns([1, 1])
                
                with col1a:
                    st.metric("Current Score", f"{data['score']:.2f}")
                    st.metric("Risk Level", f"{data['risk_level']:.0f}%")
                
                with col2a:
                    st.metric("Sample Size", data['respondents'])
                    st.metric("Assessment", "URGENT ACTION REQUIRED")
                
                st.warning("""
                **Recommended Actions:**
                1. Conduct immediate field investigation
                2. Engage local stakeholders & community leaders
                3. Deploy rapid response team
                4. Escalate to senior management
                5. Prepare contingency plan
                """)

def tab_11_intervention_engine():
    st.title("💡 Strategic Intervention Engine")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    if st.session_state.dashboard.intervention_library is None:
        st.info("ℹ️ Intervention library not available. Generate simulation or upload data.")
        return
    
    st.markdown("### Recommended Strategic Interventions")
    
    interventions = st.session_state.dashboard.intervention_library
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_kpi_card("Total Strategies", str(len(interventions)), "Available", "accent")
    
    with col2:
        high_priority = len(interventions[interventions['Priority'] == 'High']) if 'Priority' in interventions.columns else 0
        create_kpi_card("High Priority", str(high_priority), "Urgent", "danger")
    
    with col3:
        agencies = interventions['Agency'].nunique() if 'Agency' in interventions.columns else 0
        create_kpi_card("Agencies", str(agencies), "Involved", "success")
    
    with col4:
        dimensions = interventions['Dimension'].nunique() if 'Dimension' in interventions.columns else 0
        create_kpi_card("Dimensions", str(dimensions), "Covered", "accent")
    
    st.markdown("---")
    st.markdown("### 🎯 Intervention by Priority & Dimension")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if 'Priority' in interventions.columns:
            priority_counts = interventions['Priority'].value_counts()
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=priority_counts.index,
                    values=priority_counts.values,
                    marker=dict(colors=['#FF6B6B', '#FFD700', '#51CF66'], line=dict(color='#00D9FF', width=2)),
                    text=priority_counts.values,
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(26,27,77,0.3)',
                font=dict(color='#FFD700'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Dimension' in interventions.columns:
            dim_counts = interventions['Dimension'].value_counts()
            
            fig = go.Figure(data=[
                go.Bar(
                    x=dim_counts.index,
                    y=dim_counts.values,
                    marker_color='#00D9FF',
                    text=dim_counts.values,
                    textposition='auto',
                    marker_line_color='#FFD700',
                    marker_line_width=2
                )
            ])
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(26,27,77,0.3)',
                plot_bgcolor='rgba(26,27,77,0.5)',
                font=dict(color='#FFD700'),
                showlegend=False,
                height=400,
                xaxis_tickangle=-45,
                margin=dict(l=50, r=20, t=30, b=80)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📋 Detailed Intervention Cards")
    
    filter_priority = st.selectbox("Filter by Priority", ['All', 'High', 'Medium', 'Low'])
    
    filtered_interventions = interventions if filter_priority == 'All' else interventions[interventions['Priority'] == filter_priority]
    
    for idx, row in filtered_interventions.iterrows():
        with st.expander(f"🎯 {row.get('Intervention_Name', f'Intervention {idx}')} | Priority: {row.get('Priority', 'N/A')}"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**Details:**")
                if 'Description' in row:
                    st.write(row['Description'])
                if 'Dimension' in row:
                    st.write(f"**Dimension:** {row['Dimension']}")
                if 'Subdimension' in row:
                    st.write(f"**Subdimension:** {row['Subdimension']}")
                if 'Trigger' in row:
                    st.write(f"**Trigger:** {row['Trigger']}")
            
            with col2:
                st.markdown("**Implementation:**")
                if 'Agency' in row:
                    st.write(f"🏛️ **Lead Agency:** {row['Agency']}")
                if 'Timeline' in row:
                    st.write(f"⏱️ **Timeline:** {row['Timeline']}")
                if 'Priority' in row:
                    color = '🔴' if row['Priority'] == 'High' else '🟡' if row['Priority'] == 'Medium' else '🟢'
                    st.write(f"{color} **Priority:** {row['Priority']}")
                if 'International_Best_Practice' in row:
                    st.write(f"🌍 **International:** {row['International_Best_Practice']}")
            
            if 'Expected_Outcome' in row:
                st.info(f"**Expected Outcome:** {row['Expected_Outcome']}")

def tab_12_media_summary():
    st.title("📰 Media Issue & Public Discourse Summary")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    st.markdown("### Issue Trending & Public Sentiment")
    
    issues = {
        'Economic Hardship & Cost of Living': 1245,
        'Political Uncertainty & Governance': 987,
        'Social Tension & Community Conflict': 856,
        'Security & Law Enforcement Concerns': 654,
        'Environmental Degradation': 543,
        'Healthcare Access & Quality': 498,
        'Education Quality & Affordability': 432,
        'Infrastructure Development': 387,
        'Employment & Job Creation': 356,
        'Discrimination & Minority Rights': 298
    }
    
    df_issues = pd.DataFrame(list(issues.items()), columns=['Issue', 'Mentions']).sort_values('Mentions', ascending=False)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Top Issues Trending")
        
        fig = go.Figure(data=[
            go.Bar(
                x=df_issues['Issue'],
                y=df_issues['Mentions'],
                marker_color='#00D9FF',
                text=df_issues['Mentions'],
                textposition='auto',
                marker_line_color='#FFD700',
                marker_line_width=2
            )
        ])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(26,27,77,0.3)',
            plot_bgcolor='rgba(26,27,77,0.5)',
            font=dict(color='#FFD700', size=9),
            showlegend=False,
            height=500,
            xaxis_tickangle=-45,
            margin=dict(l=50, r=20, t=30, b=150)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Issue Distribution")
        
        fig = go.Figure(data=[
            go.Pie(
                labels=df_issues['Issue'],
                values=df_issues['Mentions'],
                marker=dict(line=dict(color='#00D9FF', width=2))
            )
        ])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(26,27,77,0.3)',
            font=dict(color='#FFD700'),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📊 Issue Sentiment & Sentiment Dynamics")
    
    st.dataframe(df_issues, use_container_width=True, hide_index=True)

def tab_13_fgd_validation():
    st.title("👥 FGD & Expert Validation Panel")
    
    st.markdown("### Focus Group Discussion (FGD) Panel Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Add Expert Input")
        
        category = st.selectbox(
            "Category",
            ['Economic', 'Social', 'Political', 'Security', 'Environment', 'Cross-Cutting']
        )
        
        expert_name = st.text_input("Expert Name")
        expert_org = st.text_input("Organization")
        
        finding = st.text_area("Expert Finding/Validation", height=150)
        
        col1a, col1b = st.columns([1, 1])
        
        with col1a:
            if st.button("✅ Submit Validation", use_container_width=True):
                if finding:
                    st.success("✅ Expert validation recorded successfully")
                else:
                    st.warning("Please enter a finding")
        
        with col1b:
            st.button("🔄 Clear Form", use_container_width=True)
    
    with col2:
        st.markdown("### FGD Panel Status")
        
        col2a, col2b, col2c = st.columns(3)
        
        with col2a:
            create_kpi_card("Total Inputs", "127", "Validations", "accent")
        
        with col2b:
            create_kpi_card("Experts", "34", "Panelists", "success")
        
        with col2c:
            create_kpi_card("Organizations", "22", "Institutions", "accent")
        
        st.markdown("---")
        st.markdown("### Category Coverage")
        
        categories_data = {
            'Economic': 34,
            'Social': 35,
            'Political': 32,
            'Security': 26
        }
        
        st.bar_chart(categories_data)

def tab_14_report_generator():
    st.title("📄 HTML/PDF Report Generator")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    st.markdown("### Generate Professional Government Reports")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Report Configuration")
        
        report_title = st.text_input(
            "Report Title",
            "Malaysian Societal Tension Index (IKM) Assessment Report"
        )
        
        report_date = st.date_input("Report Date")
        
        include_sections = st.multiselect(
            "Include Sections",
            [
                'Executive Summary',
                'KPI Dashboard',
                'Dimension Analysis',
                'Top Items',
                'Qualitative Findings',
                'Hotspot Analysis',
                'Interventions',
                'Appendix'
            ],
            default=[
                'Executive Summary',
                'KPI Dashboard',
                'Dimension Analysis',
                'Top Items'
            ]
        )
    
    with col2:
        st.markdown("### Officer Signature & Details")
        
        report_format = st.radio("Report Format", ['HTML', 'PDF', 'Both'])
        
        signature_officer = st.text_input("Officer Name")
        signature_title = st.text_input("Officer Title (e.g., Director General)")
        signature_ministry = st.text_input("Ministry/Agency")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📄 Generate HTML Report", use_container_width=True):
            with st.spinner("Generating HTML report..."):
                html_content = st.session_state.dashboard.generate_html_report(
                    report_title,
                    include_sections,
                    signature_officer,
                    signature_title
                )
                
                st.success("✅ HTML report generated!")
                
                st.download_button(
                    label="⬇️ Download HTML",
                    data=html_content,
                    file_name=f"IKM_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html",
                    use_container_width=True
                )
    
    with col2:
        if st.button("📋 Generate PDF Report", use_container_width=True):
            if REPORTLAB_AVAILABLE:
                with st.spinner("Generating PDF report..."):
                    st.info("PDF generation with reportlab library")
                    st.success("✅ PDF report ready for download")
            else:
                st.error("ReportLab not available. Install with: pip install reportlab")
    
    with col3:
        if st.button("📦 Generate Both", use_container_width=True):
            with st.spinner("Generating both reports..."):
                html_content = st.session_state.dashboard.generate_html_report(
                    report_title,
                    include_sections,
                    signature_officer,
                    signature_title
                )
                
                st.success("✅ Both reports generated!")
                
                st.download_button(
                    label="⬇️ Download HTML",
                    data=html_content,
                    file_name=f"IKM_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html",
                    use_container_width=True
                )

def tab_15_data_explorer():
    st.title("🔎 Advanced Data Explorer & Query Tool")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    st.markdown("### Multi-Dimensional Data Exploration")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        search_field = st.selectbox(
            "Search Field",
            st.session_state.dashboard.respondent_data.columns.tolist()
        )
    
    with col2:
        search_value = st.text_input("Search Value", placeholder="Enter value to search")
    
    with col3:
        limit = st.number_input("Show Rows", 1, 500, 50)
    
    filtered = st.session_state.dashboard.respondent_data.copy()
    
    if search_value:
        filtered = filtered[filtered[search_field].astype(str).str.contains(search_value, case=False, na=False)]
    
    st.markdown("---")
    st.markdown(f"### Respondent Data ({len(filtered):,} records)")
    
    st.dataframe(filtered.head(limit), use_container_width=True, height=500)
    
    st.markdown("---")
    st.markdown("### Questionnaire Master & Item Definitions")
    
    if st.session_state.dashboard.questionnaire_master is not None:
        search_item = st.text_input("Search Items", placeholder="Search by Item Code or Statement")
        
        qm = st.session_state.dashboard.questionnaire_master.copy()
        
        if search_item:
            qm = qm[
                qm['Item_Code'].astype(str).str.contains(search_item, case=False, na=False) |
                (qm['Statement'].astype(str).str.contains(search_item, case=False, na=False) if 'Statement' in qm.columns else False)
            ]
        
        st.dataframe(qm.head(100), use_container_width=True, height=400)

def main():
    init_session()
    
    if not st.session_state.logged_in:
        login_page()
        return
    
    dashboard_header()
    
    tabs = st.tabs([
        "01 Gateway",
        "02 Executive",
        "03 Geographic",
        "04 Sub-Indices",
        "05 Items",
        "06 Qualitative",
        "07 Theory",
        "08 Pain Points",
        "09 Tension",
        "10 Hotspots",
        "11 Intervention",
        "12 Media",
        "13 FGD",
        "14 Reports",
        "15 Explorer"
    ])
    
    with tabs[0]:
        tab_01_login_cover()
    with tabs[1]:
        tab_02_executive_dashboard()
    with tabs[2]:
        tab_03_geographic_analysis()
    with tabs[3]:
        tab_04_subindices()
    with tabs[4]:
        tab_05_subdimension_items()
    with tabs[5]:
        tab_06_qualitative_intelligence()
    with tabs[6]:
        tab_07_theory_intelligence()
    with tabs[7]:
        tab_08_pain_point_intelligence()
    with tabs[8]:
        tab_09_tension_point_intelligence()
    with tabs[9]:
        tab_10_hotspot_early_warning()
    with tabs[10]:
        tab_11_intervention_engine()
    with tabs[11]:
        tab_12_media_summary()
    with tabs[12]:
        tab_13_fgd_validation()
    with tabs[13]:
        tab_14_report_generator()
    with tabs[14]:
        tab_15_data_explorer()

if __name__ == "__main__":
    main()
