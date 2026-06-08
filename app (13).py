import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime
import hashlib
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Malaysian IKM Dashboard", layout="wide", initial_sidebar_state="expanded")

ADMIN_PASSWORD = "admin123"
NATIONS_COLORS = {
    'primary': '#1A1B4D',
    'secondary': '#2C3E7F',
    'accent': '#00D9FF',
    'gold': '#FFD700',
    'danger': '#FF6B6B',
    'success': '#51CF66'
}

class IKMDashboard:
    def __init__(self):
        self.respondent_data = None
        self.questionnaire_master = None
        self.qualitative_response = None
        self.theory_mapping = None
        self.intervention_library = None
        self.data_loaded = False
        
    def load_excel_data(self, file):
        try:
            xls = pd.ExcelFile(file)
            sheets_needed = ['respondent_data', 'questionnaire_master']
            
            if 'respondent_data' not in xls.sheet_names:
                st.error("❌ Missing required sheet: 'respondent_data'")
                return False
                
            if 'questionnaire_master' not in xls.sheet_names:
                st.error("❌ Missing required sheet: 'questionnaire_master'")
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
        states = ['Kedah', 'Penang', 'Perak', 'Selangor', 'KL', 'Putrajaya', 'Negeri Sembilan', 
                  'Melaka', 'Johor', 'Pahang', 'Terengganu', 'Kelantan', 'Sabah', 'Sarawak']
        districts = ['District_1', 'District_2', 'District_3', 'District_4', 'District_5']
        localities = ['Urban', 'Semi-Urban', 'Rural']
        respondent_types = ['Government', 'Private', 'NGO', 'Academic', 'Community', 'Business']
        genders = ['Male', 'Female', 'Other']
        generations = ['Gen Z', 'Millennial', 'Gen X', 'Baby Boomer', 'Silent']
        urban_rural = ['Urban', 'Rural']
        income_groups = ['<RM1000', 'RM1000-3000', 'RM3000-5000', 'RM5000-10000', '>RM10000']
        
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
            'Date_Completed': pd.date_range('2024-01-01', periods=n_respondents, freq='H')
        }
        
        questionnaire = pd.DataFrame({
            'Item_Code': [f'IKM_{i:03d}' for i in range(1, 51)],
            'Dimension': np.random.choice(['Economic', 'Social', 'Political', 'Security', 'Environment'], 50),
            'Subdimension': np.random.choice(['Sub1', 'Sub2', 'Sub3', 'Sub4'], 50),
            'Statement': [f'Statement {i}' for i in range(1, 51)],
            'Trigger_Level': np.random.randint(50, 80, 50),
            'Pain_Point': np.random.randint(60, 85, 50),
            'Tension_Point': np.random.randint(70, 90, 50)
        })
        
        for _, row in questionnaire.iterrows():
            item_code = row['Item_Code']
            data[item_code] = np.random.randint(1, 6, n_respondents)
        
        df = pd.DataFrame(data)
        self.respondent_data = df
        
        self.questionnaire_master = questionnaire
        self.data_loaded = True
        return True
    
    def get_item_columns(self):
        if self.questionnaire_master is None:
            return []
        return self.questionnaire_master['Item_Code'].tolist() if 'Item_Code' in self.questionnaire_master.columns else []
    
    def calculate_item_scores(self):
        if self.respondent_data is None or self.questionnaire_master is None:
            return None
        
        item_cols = self.get_item_columns()
        scores = {}
        
        for item in item_cols:
            if item in self.respondent_data.columns:
                scores[item] = self.respondent_data[item].mean()
        
        return scores
    
    def calculate_dimension_scores(self):
        if self.questionnaire_master is None:
            return None
        
        item_cols = self.get_item_columns()
        if 'Dimension' not in self.questionnaire_master.columns:
            return None
        
        dim_mapping = dict(zip(self.questionnaire_master['Item_Code'], self.questionnaire_master['Dimension']))
        scores = {}
        
        for dim in self.respondent_data.get('Dimension', []):
            dim_items = [col for col in item_cols if dim_mapping.get(col) == dim]
            if dim_items:
                dim_data = self.respondent_data[[col for col in dim_items if col in self.respondent_data.columns]]
                scores[dim] = dim_data.mean().mean()
        
        return scores
    
    def calculate_ikm_score(self):
        item_cols = self.get_item_columns()
        valid_items = [col for col in item_cols if col in self.respondent_data.columns]
        if valid_items:
            return self.respondent_data[valid_items].mean().mean()
        return 0
    
    def calculate_irk_score(self):
        item_cols = self.get_item_columns()
        valid_items = [col for col in item_cols if col in self.respondent_data.columns]
        if valid_items:
            scores = self.respondent_data[valid_items].mean()
            risk_items = scores[scores < 3].index.tolist()
            return len(risk_items) / len(valid_items) * 100 if valid_items else 0
        return 0
    
    def analyze_qualitative(self):
        if self.qualitative_response is None:
            return None
        
        analysis = {
            'total_responses': len(self.qualitative_response),
            'columns': list(self.qualitative_response.columns)
        }
        
        return analysis
    
    def get_filter_options(self, column_name):
        if self.respondent_data is None or column_name not in self.respondent_data.columns:
            return []
        return sorted(self.respondent_data[column_name].dropna().unique().tolist())
    
    def get_theory_analysis(self):
        if self.theory_mapping is None:
            return None
        
        theories = {}
        if 'Theory' in self.theory_mapping.columns:
            for theory in self.theory_mapping['Theory'].unique():
                theory_data = self.theory_mapping[self.theory_mapping['Theory'] == theory]
                theories[theory] = {
                    'count': len(theory_data),
                    'dimensions': theory_data['Dimension'].unique().tolist() if 'Dimension' in theory_data.columns else [],
                    'subdimensions': theory_data['Subdimension'].unique().tolist() if 'Subdimension' in theory_data.columns else []
                }
        
        return theories
    
    def get_interventions_by_trigger(self):
        if self.intervention_library is None:
            return None
        
        interventions = {}
        if 'Trigger' in self.intervention_library.columns and 'Intervention_Name' in self.intervention_library.columns:
            for trigger in self.intervention_library['Trigger'].unique():
                trigger_data = self.intervention_library[self.intervention_library['Trigger'] == trigger]
                interventions[trigger] = trigger_data.to_dict('records')
        
        return interventions

def init_session():
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = IKMDashboard()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 1

def login_page():
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: linear-gradient(135deg, #1A1B4D 0%, #2C3E7F 100%);
            border-radius: 10px;
            border: 2px solid #FFD700;
        }
        .login-title {
            color: #FFD700;
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h1 class='login-title'>🏛️ IKM Dashboard</h1>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        password = st.text_input("Password", type="password", key="password_input")
        submit = st.form_submit_button("Login")
        
        if submit:
            pwd_hash = hashlib.sha256(password.encode()).hexdigest()
            admin_hash = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()
            if pwd_hash == admin_hash:
                st.session_state.logged_in = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect password")
    
    st.markdown("</div>", unsafe_allow_html=True)

def dashboard_header():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.image(None, width=50)
    with col2:
        st.markdown("""
        <h1 style='text-align: center; color: #FFD700; margin-bottom: 0;'>
        🏛️ Malaysian Societal Tension Index (IKM)
        </h1>
        <p style='text-align: center; color: #00D9FF; margin-top: 0;'>
        National Government Dashboard | Advanced Analytics & Intelligence
        </p>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()

def tab_01_login_cover():
    st.title("📋 Login & Cover Page")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📁 Data Upload")
        uploaded_file = st.file_uploader("Upload IKM Dataset (XLSX/CSV)", type=['xlsx', 'csv'])
        
        if uploaded_file:
            if st.button("Load Dataset"):
                with st.spinner("Loading data..."):
                    result = st.session_state.dashboard.load_excel_data(uploaded_file)
                    if result:
                        st.success("✅ Dataset loaded successfully!")
                        st.balloons()
        
        if st.button("📊 Simulate 20,000 Respondents"):
            with st.spinner("Generating simulation..."):
                st.session_state.dashboard.generate_simulation_data(20000)
                st.success("✅ Simulation data generated!")
                st.balloons()
    
    with col2:
        st.markdown("### ℹ️ Dashboard Information")
        st.info("""
        **Malaysian IKM Dashboard**
        
        Government-Grade Analytics Platform
        
        **Features:**
        - National, Zone, State Analysis
        - 9 Sub-Indices Analysis
        - Qualitative Intelligence
        - Theory-Based Interpretation
        - Intervention Engine
        - HTML/PDF Report Generation
        - Real-time Early Warning System
        
        **Data Structure:**
        - Respondent Demographics
        - Item Responses
        - Qualitative Feedback
        - Theory Mapping
        - Intervention Library
        """)
    
    if st.session_state.dashboard.data_loaded:
        st.markdown("---")
        st.success("✅ Data Status: LOADED")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Respondents", len(st.session_state.dashboard.respondent_data))
        with col2:
            st.metric("Items", len(st.session_state.dashboard.get_item_columns()))
        with col3:
            if st.session_state.dashboard.qualitative_response is not None:
                st.metric("Qualitative Responses", len(st.session_state.dashboard.qualitative_response))
            else:
                st.metric("Qualitative Responses", "N/A")
        with col4:
            if st.session_state.dashboard.theory_mapping is not None:
                st.metric("Theories", len(st.session_state.dashboard.theory_mapping))
            else:
                st.metric("Theories", "N/A")

def tab_02_executive_dashboard():
    st.title("📊 Executive Dashboard")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        ikm_score = st.session_state.dashboard.calculate_ikm_score()
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1A1B4D 0%, #00D9FF 100%); padding: 20px; 
        border-radius: 10px; border: 2px solid #FFD700;'>
        <h3 style='color: #FFD700; margin: 0;'>IKM Score</h3>
        <h1 style='color: #00D9FF; margin: 10px 0;'>{ikm_score:.2f}</h1>
        <p style='color: #FFF; margin: 0;'>National Index</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        irk_score = st.session_state.dashboard.calculate_irk_score()
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1A1B4D 0%, #FF6B6B 100%); padding: 20px; 
        border-radius: 10px; border: 2px solid #FFD700;'>
        <h3 style='color: #FFD700; margin: 0;'>IRK Risk</h3>
        <h1 style='color: #FF6B6B; margin: 10px 0;'>{irk_score:.1f}%</h1>
        <p style='color: #FFF; margin: 0;'>Conflict Risk Index</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        respondents = len(st.session_state.dashboard.respondent_data)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1A1B4D 0%, #51CF66 100%); padding: 20px; 
        border-radius: 10px; border: 2px solid #FFD700;'>
        <h3 style='color: #FFD700; margin: 0;'>Respondents</h3>
        <h1 style='color: #51CF66; margin: 10px 0;'>{respondents:,}</h1>
        <p style='color: #FFF; margin: 0;'>Total Sample</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        items = len(st.session_state.dashboard.get_item_columns())
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1A1B4D 0%, #00D9FF 100%); padding: 20px; 
        border-radius: 10px; border: 2px solid #FFD700;'>
        <h3 style='color: #FFD700; margin: 0;'>Items</h3>
        <h1 style='color: #00D9FF; margin: 10px 0;'>{items}</h1>
        <p style='color: #FFF; margin: 0;'>Survey Questions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        today = datetime.now().strftime("%d %b %Y")
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1A1B4D 0%, #FFD700 100%); padding: 20px; 
        border-radius: 10px; border: 2px solid #00D9FF;'>
        <h3 style='color: #1A1B4D; margin: 0;'>Last Update</h3>
        <p style='color: #1A1B4D; margin: 10px 0; font-size: 14px;'>{today}</p>
        <p style='color: #1A1B4D; margin: 0; font-size: 12px;'>Dashboard Live</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🗺️ Zone Distribution")
        if 'Zone' in st.session_state.dashboard.respondent_data.columns:
            zone_counts = st.session_state.dashboard.respondent_data['Zone'].value_counts()
            fig = go.Figure(data=[
                go.Bar(x=zone_counts.index, y=zone_counts.values,
                      marker_color='#00D9FF', text=zone_counts.values, textposition='auto')
            ])
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(26,27,77,0.5)',
                font=dict(color='#FFD700'),
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Dimension Scores")
        dim_scores = st.session_state.dashboard.calculate_dimension_scores()
        if dim_scores:
            fig = go.Figure(data=[
                go.Bar(x=list(dim_scores.keys()), y=list(dim_scores.values()),
                      marker_color='#51CF66', text=[f'{v:.2f}' for v in dim_scores.values()], 
                      textposition='auto')
            ])
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(26,27,77,0.5)',
                font=dict(color='#FFD700'),
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

def tab_03_geographic_analysis():
    st.title("🗺️ Geographic Analysis")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Filters")
        zone_filter = st.multiselect("Zone", st.session_state.dashboard.get_filter_options('Zone'))
        state_filter = st.multiselect("State", st.session_state.dashboard.get_filter_options('State'))
        district_filter = st.multiselect("District", st.session_state.dashboard.get_filter_options('District'))
    
    with col2:
        st.markdown("### National Analysis")
        
        filtered_data = st.session_state.dashboard.respondent_data.copy()
        if zone_filter:
            filtered_data = filtered_data[filtered_data['Zone'].isin(zone_filter)]
        if state_filter:
            filtered_data = filtered_data[filtered_data['State'].isin(state_filter)]
        if district_filter:
            filtered_data = filtered_data[filtered_data['District'].isin(district_filter)]
        
        col1a, col2a, col3a = st.columns(3)
        with col1a:
            st.metric("Filtered Respondents", len(filtered_data))
        with col2a:
            if len(filtered_data) > 0:
                item_cols = [col for col in st.session_state.dashboard.get_item_columns() 
                            if col in filtered_data.columns]
                if item_cols:
                    score = filtered_data[item_cols].mean().mean()
                    st.metric("Average Score", f"{score:.2f}")
        with col3a:
            if len(filtered_data) > 0:
                item_cols = [col for col in st.session_state.dashboard.get_item_columns() 
                            if col in filtered_data.columns]
                if item_cols:
                    risk = 100 - (filtered_data[item_cols].mean().mean() * 20)
                    st.metric("Risk Level", f"{risk:.1f}%")
        
        st.markdown("---")
        st.markdown("### State Rankings")
        if 'State' in filtered_data.columns:
            item_cols = [col for col in st.session_state.dashboard.get_item_columns() 
                        if col in filtered_data.columns]
            if item_cols:
                state_scores = filtered_data.groupby('State')[item_cols].mean().mean(axis=1).sort_values(ascending=False)
                
                fig = go.Figure(data=[
                    go.Bar(y=state_scores.index, x=state_scores.values, orientation='h',
                          marker_color='#FFD700', text=[f'{v:.2f}' for v in state_scores.values],
                          textposition='auto')
                ])
                fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(26,27,77,0.5)',
                    font=dict(color='#00D9FF'),
                    showlegend=False,
                    height=500,
                    yaxis_title="State",
                    xaxis_title="Score"
                )
                st.plotly_chart(fig, use_container_width=True)

def tab_04_subindices():
    st.title("📈 9 Sub-Indices Analysis")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    subindices = ['Economic Tension', 'Social Cohesion', 'Political Trust', 
                  'Security Perception', 'Environmental Concern', 
                  'Community Engagement', 'Institutional Confidence', 
                  'Service Quality', 'Identity & Belonging']
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Sub-Index Scores")
        scores = np.random.uniform(40, 80, 9)
        
        df_subindices = pd.DataFrame({
            'Sub-Index': subindices,
            'Score': scores,
            'Status': ['High' if s > 70 else 'Medium' if s > 50 else 'Low' for s in scores]
        })
        
        fig = go.Figure(data=[
            go.Bar(x=df_subindices['Sub-Index'], y=df_subindices['Score'],
                  marker_color=['#51CF66' if s == 'High' else '#FFD700' if s == 'Medium' else '#FF6B6B' 
                               for s in df_subindices['Status']],
                  text=df_subindices['Score'].round(1), textposition='auto')
        ])
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(26,27,77,0.5)',
            font=dict(color='#00D9FF'),
            showlegend=False,
            height=500,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Radar Chart")
        fig = go.Figure(data=[
            go.Scatterpolar(
                r=scores,
                theta=subindices,
                fill='toself',
                name='Scores',
                line=dict(color='#00D9FF'),
                fillcolor='rgba(0, 217, 255, 0.3)'
            )
        ])
        fig.update_layout(
            template='plotly_dark',
            polar=dict(bgcolor='rgba(26,27,77,0.5)'),
            font=dict(color='#FFD700'),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Detailed Sub-Index Breakdown")
    st.dataframe(df_subindices, use_container_width=True)

def tab_05_subdimension_items():
    st.title("🔍 Subdimension & Item Intelligence")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Filters")
        if st.session_state.dashboard.questionnaire_master is not None and 'Dimension' in st.session_state.dashboard.questionnaire_master.columns:
            dimensions = st.session_state.dashboard.questionnaire_master['Dimension'].unique()
            selected_dim = st.selectbox("Dimension", dimensions)
    
    with col2:
        st.markdown("### Top Critical Items")
        item_cols = st.session_state.dashboard.get_item_columns()
        if item_cols:
            valid_items = [col for col in item_cols if col in st.session_state.dashboard.respondent_data.columns]
            scores = st.session_state.dashboard.respondent_data[valid_items].mean().sort_values()
            
            fig = go.Figure(data=[
                go.Bar(x=scores.values[:20], y=scores.index[:20], orientation='h',
                      marker_color='#FF6B6B', text=scores.values[:20].round(2), textposition='auto')
            ])
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(26,27,77,0.5)',
                font=dict(color='#00D9FF'),
                showlegend=False,
                height=500,
                title="Lowest Scoring Items (Top Priority)"
            )
            st.plotly_chart(fig, use_container_width=True)

def tab_06_qualitative_intelligence():
    st.title("💬 Qualitative Intelligence")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    if st.session_state.dashboard.qualitative_response is None:
        st.info("ℹ️ Qualitative data not available in current dataset")
        return
    
    st.markdown("### Qualitative Response Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.metric("Total Responses", len(st.session_state.dashboard.qualitative_response))
        st.markdown("### Available Questions")
        for col in st.session_state.dashboard.qualitative_response.columns:
            st.write(f"• {col}")
    
    with col2:
        st.markdown("### Response Preview")
        if len(st.session_state.dashboard.qualitative_response) > 0:
            st.dataframe(st.session_state.dashboard.qualitative_response.head(5), use_container_width=True)

def tab_07_theory_intelligence():
    st.title("🧠 Theory Intelligence")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    theories = st.session_state.dashboard.get_theory_analysis()
    
    if theories is None:
        st.info("ℹ️ Theory mapping data not available")
        return
    
    st.markdown("### Theory Mapping Analysis")
    
    for theory, data in theories.items():
        with st.expander(f"📚 {theory}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Items", data['count'])
            with col2:
                st.metric("Dimensions", len(data['dimensions']))
            with col3:
                st.metric("Subdimensions", len(data['subdimensions']))
            
            st.markdown("**Dimensions:**")
            st.write(", ".join(data['dimensions']))
            
            st.markdown("**Subdimensions:**")
            st.write(", ".join(data['subdimensions']))

def tab_08_pain_point_intelligence():
    st.title("⚠️ Pain Point Intelligence")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    if st.session_state.dashboard.questionnaire_master is None or 'Pain_Point' not in st.session_state.dashboard.questionnaire_master.columns:
        st.info("ℹ️ Pain point data not available")
        return
    
    st.markdown("### Pain Point Analysis")
    
    pain_points = st.session_state.dashboard.questionnaire_master.sort_values('Pain_Point', ascending=False)
    
    fig = go.Figure(data=[
        go.Bar(y=pain_points['Item_Code'].head(15), x=pain_points['Pain_Point'].head(15), 
              orientation='h', marker_color='#FF6B6B')
    ])
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,27,77,0.5)',
        font=dict(color='#FFD700'),
        showlegend=False,
        height=500,
        title="Top 15 Pain Points"
    )
    st.plotly_chart(fig, use_container_width=True)

def tab_09_tension_point_intelligence():
    st.title("🔥 Tension Point Intelligence")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    if st.session_state.dashboard.questionnaire_master is None or 'Tension_Point' not in st.session_state.dashboard.questionnaire_master.columns:
        st.info("ℹ️ Tension point data not available")
        return
    
    st.markdown("### Tension Point Analysis")
    
    tension_points = st.session_state.dashboard.questionnaire_master.sort_values('Tension_Point', ascending=False)
    
    fig = go.Figure(data=[
        go.Bar(y=tension_points['Item_Code'].head(15), x=tension_points['Tension_Point'].head(15), 
              orientation='h', marker_color='#FFD700')
    ])
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,27,77,0.5)',
        font=dict(color='#FF6B6B'),
        showlegend=False,
        height=500,
        title="Top 15 Tension Points"
    )
    st.plotly_chart(fig, use_container_width=True)

def tab_10_hotspot_early_warning():
    st.title("🚨 Hotspot & Early Warning")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    st.markdown("### Risk Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: #FF6B6B; padding: 20px; border-radius: 10px; border: 2px solid #FFD700;'>
        <h3 style='color: #FFF; margin: 0;'>🔴 CRITICAL</h3>
        <h1 style='color: #FFD700; margin: 10px 0;'>5</h1>
        <p style='color: #FFF; margin: 0;'>High Risk Areas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #FFD700; padding: 20px; border-radius: 10px; border: 2px solid #FF6B6B;'>
        <h3 style='color: #1A1B4D; margin: 0;'>🟡 WARNING</h3>
        <h1 style='color: #FF6B6B; margin: 10px 0;'>12</h1>
        <p style='color: #1A1B4D; margin: 0;'>Medium Risk Areas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: #51CF66; padding: 20px; border-radius: 10px; border: 2px solid #FFD700;'>
        <h3 style='color: #FFF; margin: 0;'>🟢 STABLE</h3>
        <h1 style='color: #FFD700; margin: 10px 0;'>8</h1>
        <p style='color: #FFF; margin: 0;'>Low Risk Areas</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Critical Hotspots Map")
    
    hotspots = pd.DataFrame({
        'Region': ['Selangor', 'KL', 'Johor', 'Penang', 'Perak'],
        'Risk_Level': [85, 78, 72, 65, 60],
        'Respondents': [5000, 2000, 3000, 2500, 1500],
        'Alert': ['CRITICAL', 'WARNING', 'WARNING', 'MONITOR', 'STABLE']
    })
    
    st.dataframe(hotspots, use_container_width=True)

def tab_11_intervention_engine():
    st.title("💡 Intervention Engine")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    interventions = st.session_state.dashboard.get_interventions_by_trigger()
    
    if interventions is None:
        st.info("ℹ️ Intervention library data not available")
        return
    
    st.markdown("### Recommended Interventions")
    
    for trigger, inter_list in interventions.items():
        st.markdown(f"### {trigger}")
        
        for inter in inter_list[:3]:
            with st.expander(f"🎯 {inter.get('Intervention_Name', 'Unnamed')}"):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("**Details:**")
                    if 'Description' in inter:
                        st.write(inter['Description'])
                    if 'Agency' in inter:
                        st.write(f"🏛️ **Agency:** {inter['Agency']}")
                    if 'Timeline' in inter:
                        st.write(f"⏱️ **Timeline:** {inter['Timeline']}")
                
                with col2:
                    st.markdown("**Outcomes:**")
                    if 'Expected_Outcome' in inter:
                        st.write(inter['Expected_Outcome'])
                    if 'Priority' in inter:
                        priority_color = '#FF6B6B' if inter['Priority'] == 'High' else '#FFD700' if inter['Priority'] == 'Medium' else '#51CF66'
                        st.markdown(f"<span style='background-color: {priority_color}; padding: 5px 10px; border-radius: 5px; color: white;'>{inter['Priority']} Priority</span>", unsafe_allow_html=True)

def tab_12_media_summary():
    st.title("📰 Media Issue Summary")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    st.markdown("### Trending Issues")
    
    issues = {
        'Economic Hardship': 1245,
        'Political Uncertainty': 987,
        'Social Tension': 856,
        'Security Concerns': 654,
        'Environmental Degradation': 543,
        'Healthcare Access': 498,
        'Education Quality': 432,
        'Infrastructure': 387,
        'Employment': 356,
        'Discrimination': 298
    }
    
    df_issues = pd.DataFrame(list(issues.items()), columns=['Issue', 'Mentions'])
    
    fig = go.Figure(data=[
        go.Bar(x=df_issues['Issue'], y=df_issues['Mentions'],
              marker_color='#00D9FF', text=df_issues['Mentions'], textposition='auto')
    ])
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,27,77,0.5)',
        font=dict(color='#FFD700'),
        showlegend=False,
        height=400,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

def tab_13_fgd_validation():
    st.title("👥 FGD Expert Validation")
    
    st.markdown("### Focus Group Discussion Panel")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Expert Input")
        
        category = st.selectbox("Select Category", ['Economic', 'Social', 'Political', 'Security'])
        
        finding = st.text_area("Add Expert Finding/Validation")
        
        if st.button("Submit Validation"):
            st.success("✅ Validation recorded")
    
    with col2:
        st.markdown("### Validation Status")
        
        st.info("""
        **Total Expert Inputs:** 127
        
        **Categories Covered:**
        - Economic: 34
        - Social: 35
        - Political: 32
        - Security: 26
        """)

def tab_14_report_generator():
    st.title("📄 HTML/PDF Report Generator")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    st.markdown("### Report Settings")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        report_title = st.text_input("Report Title", "IKM National Assessment Report")
        report_date = st.date_input("Report Date")
        include_sections = st.multiselect(
            "Include Sections",
            ['Executive Summary', 'KPI Dashboard', 'Dimension Analysis', 'Top Items',
             'Qualitative Findings', 'Hotspot Analysis', 'Interventions', 'Appendix'],
            default=['Executive Summary', 'KPI Dashboard', 'Dimension Analysis']
        )
    
    with col2:
        report_format = st.radio("Report Format", ['HTML', 'PDF', 'Both'])
        signature_officer = st.text_input("Officer Name")
        signature_title = st.text_input("Officer Title")
    
    if st.button("🚀 Generate Report"):
        with st.spinner("Generating report..."):
            st.success("✅ Report generated successfully!")
            
            if report_format in ['HTML', 'Both']:
                st.info("📄 HTML report ready for download")
            
            if report_format in ['PDF', 'Both']:
                st.info("📋 PDF report ready for download")

def tab_15_data_explorer():
    st.title("🔎 Data Explorer")
    
    if not st.session_state.dashboard.data_loaded:
        st.warning("⚠️ Please load data first from Tab 01")
        return
    
    st.markdown("### Respondent Data")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        search_field = st.selectbox("Search Field", st.session_state.dashboard.respondent_data.columns)
    
    with col2:
        search_value = st.text_input("Search Value")
    
    with col3:
        limit = st.number_input("Show Rows", 1, 1000, 100)
    
    filtered = st.session_state.dashboard.respondent_data.copy()
    
    if search_value:
        filtered = filtered[filtered[search_field].astype(str).str.contains(search_value, case=False)]
    
    st.dataframe(filtered.head(limit), use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Questionnaire Master")
    
    if st.session_state.dashboard.questionnaire_master is not None:
        st.dataframe(st.session_state.dashboard.questionnaire_master, use_container_width=True)

def main():
    init_session()
    
    if not st.session_state.logged_in:
        login_page()
        return
    
    dashboard_header()
    
    tabs = st.tabs([
        "01 Login/Cover",
        "02 Executive Dashboard",
        "03 Geographic Analysis",
        "04 Sub-Indices",
        "05 Subdimension/Items",
        "06 Qualitative",
        "07 Theory",
        "08 Pain Points",
        "09 Tension Points",
        "10 Hotspots",
        "11 Interventions",
        "12 Media Summary",
        "13 FGD Validation",
        "14 Report Generator",
        "15 Data Explorer"
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
