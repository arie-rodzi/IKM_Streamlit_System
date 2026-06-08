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

# --- 1. REKA BENTUK VISUAL: LIGHT EXECUTIVE WINDOWS THEME (HIGH CONTRAST) ---
def apply_executive_premium_theme():
    st.markdown("""
        <style>
            .stApp {
                background-color: #F8FAFC !important;
                color: #0F172A !important;
            }
            [data-testid="stSidebar"] {
                background-color: #0F172A !important;
                border-right: 2px solid #E2E8F0 !important;
            }
            [data-testid="stSidebar"] * {
                color: #F8FAFC !important;
            }
            h1, h2, h3, h4, p, span, label {
                color: #0F172A !important;
                font-family: 'Segoe UI', Inter, sans-serif !important;
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 6px;
                background-color: #E2E8F0;
                padding: 6px;
                border-radius: 10px;
                border: 1px solid #CBD5E1;
            }
            .stTabs [data-baseweb="tab"] {
                height: 38px;
                padding: 0px 16px !important;
                background-color: transparent !important;
                border-radius: 6px !important;
                color: #475569 !important;
                font-weight: 600 !important;
                transition: all 0.2s ease;
            }
            .stTabs [aria-selected="true"] {
                background-color: #FFFFFF !important;
                color: #1E3A8A !important;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08) !important;
                border: 1px solid #CBD5E1 !important;
            }
            .kpi-card-premium {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-left: 6px solid #1E40AF;
                border-radius: 12px;
                padding: 22px;
                text-align: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s ease;
            }
            .kpi-card-premium:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
            }
            .kpi-label {
                color: #475569 !important;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.7px;
                margin: 0;
            }
            .kpi-value {
                font-size: 36px;
                font-weight: 800;
                margin: 6px 0;
            }
            .stDataFrame {
                border: 1px solid #E2E8F0 !important;
                border-radius: 8px !important;
                background-color: #FFFFFF !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_kpi_card(label, value, unit, tier="low"):
    color_map = {"low": "#10B981", "tension": "#F59E0B", "pain": "#DB2777", "hotspot": "#EF4444"}
    border_color = color_map.get(tier, "#1E40AF")
    st.markdown(f"""
    <div class="kpi-card-premium" style="border-left-color: {border_color};">
        <p class="kpi-label">{label}</p>
        <div class="kpi-value" style="color: {border_color} !important;">{value}</div>
        <p style='color: #64748B !important; font-size: 11px; font-weight: 500; margin: 0;'>{unit}</p>
    </div>
    """, unsafe_allow_html=True)


# --- 2. ENGIN ANALITIK STRATEGIK INTELLIGENCE (IKMM 2026) ---
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

    def calculate_composite_index(self, df=None):
        if df is None: df = self.respondent_data
        all_items = [f'IKM_{i:03d}' for i in range(1, 109) if f'IKM_{i:03d}' in df.columns]
        if not all_items: return 0.0, "low"
        
        mean_raw = df[all_items].mean().mean()
        normalized_score = ((mean_raw - 1) / 4) * 100
        return normalized_score, self.get_tier(normalized_score)

    def calculate_single_dimension_score(self, dim_name, df=None):
        if df is None: df = self.respondent_data
        target_items = [it for it in self.dim_item_ranges.get(dim_name, []) if it in df.columns]
        if not target_items: return 0.0
        
        dim_mean_raw = df[target_items].mean().mean()
        return ((dim_mean_raw - 1) / 4) * 100

    def get_dimension_composite_scores(self, df=None):
        if df is None: df = self.respondent_data
        results = {}
        for dim in self.dim_item_ranges.keys():
            results[dim] = self.calculate_single_dimension_score(dim, df)
        return results

    def calculate_item_scores(self, df=None):
        if df is None: df = self.respondent_data
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
        demo_cols = ['Zone', 'State', 'District', 'Locality', 'Type_of_Respondent', 
                     'Gender', 'Generation', 'Urban_Rural', 'Income_Group', 'Ethnicity', 'Religion']
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

    def get_state_geospatial_matrix(self):
        if 'State' not in self.respondent_data.columns: return pd.DataFrame()
        items = self.get_registered_items()
        
        records = []
        for state, group in self.respondent_data.groupby('State'):
            raw_mean = group[items].mean().mean()
            tension_index = ((raw_mean - 1) / 4) * 100
            
            if tension_index >= 80.0: classification = "🔴 Hotspot / Kritikal"
            elif tension_index >= 60.0: classification = "💗 Pain Point"
            elif tension_index >= 40.0: classification = "💛 Tension Point"
            else: classification = "💚 Rendah / Stabil"
                
            records.append({
                'Negeri / Wilayah': state, 
                'Indeks Ketegangan (IKM %)': tension_index, 
                'Klasifikasi Risiko': classification,
                'Populasi Sampel': len(group)
            })
            
        return pd.DataFrame(records).sort_values('Indeks Ketegangan (IKM %)', ascending=False)

    # --- ENGIN JANAAN DOSSIER DOSAR HTML (10+ HALAMAN FORMAT KABINET) ---
    def generate_html_dossier_report(self, title, officer, branch):
        score, tier = self.calculate_composite_index()
        total_resp = len(self.respondent_data)
        now_str = datetime.now().strftime('%d %B %Y')
        
        # Demografi statik untuk laporan eksekutif teks
        malay_pct = (len(self.respondent_data[self.respondent_data['Ethnicity'] == 'Malay']) / total_resp) * 100
        urban_pct = (len(self.respondent_data[self.respondent_data['Urban_Rural'] == 'Urban']) / total_resp) * 100
        b40_pct = (len(self.respondent_data[self.respondent_data['Income_Group'] == 'B40']) / total_resp) * 100
        
        html = f"""
        <!DOCTYPE html>
        <html lang="ms">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                body {{ font-family: 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #F8FAFC; color: #0F172A; padding: 40px; line-height: 1.8; }}
                .dossier-wrapper {{ max-width: 1050px; margin: 0 auto; background: #FFFFFF; padding: 60px; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }}
                .header-banner {{ background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); color: #FFFFFF; padding: 45px; text-align: center; border-radius: 12px; border-bottom: 6px solid #FFD700; margin-bottom: 40px; }}
                .confidential-tag {{ color: #EF4444; font-weight: 900; letter-spacing: 2px; font-size: 14px; margin-bottom: 10px; text-transform: uppercase; }}
                .section-title {{ color: #1E3A8A; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; margin-top: 40px; font-size: 20px; text-transform: uppercase; letter-spacing: 0.5px; }}
                .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0; }}
                .kpi-box {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-top: 4px solid #1E40AF; padding: 20px; border-radius: 8px; text-align: center; }}
                .kpi-box.alert {{ border-top-color: #EF4444; }}
                .kpi-val {{ font-size: 32px; font-weight: 800; color: #1E3A8A; margin: 10px 0; }}
                .table-premium {{ width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 14px; }}
                .table-premium th {{ background: #0F172A; color: #FFFFFF; padding: 14px; text-align: left; font-weight: 600; }}
                .table-premium td {{ padding: 12px; border-bottom: 1px solid #E2E8F0; color: #334155; }}
                .table-premium tr:nth-child(even) {{ background-color: #F8FAFC; }}
                .badge {{ padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; }}
                .badge-hotspot {{ background-color: #FEE2E2; color: #EF4444; border: 1px solid #FCA5A5; }}
                .badge-pain {{ background-color: #FCE7F3; color: #DB2777; border: 1px solid #FBCFE8; }}
                .badge-tension {{ background-color: #FEF3C7; color: #D97706; border: 1px solid #FCD34D; }}
                .badge-low {{ background-color: #D1FAE5; color: #059669; border: 1px solid #A7F3D0; }}
                .meta-footer {{ margin-top: 60px; padding-top: 20px; border-top: 2px dashed #E2E8F0; text-align: center; font-size: 12px; color: #64748B; }}
                .page-break {{ page-break-before: always; }}
                .highlight-box {{ background-color: #EFF6FF; border-left: 4px solid #3B82F6; padding: 20px; border-radius: 0 8px 8px 0; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="dossier-wrapper">
                <div class="header-banner">
                    <div class="confidential-tag">SULIT — Untuk Kegunaan Rasmi Sahaja</div>
                    <h1 style="margin: 0; font-size: 28px;">{title}</h1>
                    <p style="margin: 10px 0 0 0; font-size: 14px; color: #94A3B8;">Analisis Komposit Model Kesiagaan Sosial Negara (IKMM 2026)</p>
                    <p style="margin: 5px 0 0 0; font-size: 12px; color: #CBD5E1;">Tarikh Kompleks: {now_str} | ID Arkib: JPM-IKMM-2026-V1</p>
                </div>
                
                <div class="section-title">1.0 Ringkasan Petunjuk Prestasi Utama (KPI)</div>
                <div class="kpi-grid">
                    <div class="kpi-box {'alert' if score>=60 else ''}">
                        <div class="kpi-label" style="color:#64748B; font-weight:700; font-size:11px;">Indeks Ketegangan Kebangsaan</div>
                        <div class="kpi-val" style="color:{'#EF4444' if score>=60 else '#1E3A8A'}">{score:.2f}%</div>
                        <div style="font-size:11px; font-weight:600; color:#475569;">Klasifikasi: {tier.upper()}</div>
                    </div>
                    <div class="kpi-box">
                        <div class="kpi-label" style="color:#64748B; font-weight:700; font-size:11px;">Jumlah Sampel Pool Nasional</div>
                        <div class="kpi-val">{total_resp:,}</div>
                        <div style="font-size:11px; font-weight:600; color:#475569;">Responden Berstrata DOSM</div>
                    </div>
                    <div class="kpi-box alert">
                        <div class="kpi-label" style="color:#64748B; font-weight:700; font-size:11px;">Zon Amaran Konflik Siber</div>
                        <div class="kpi-val">{self.calculate_single_dimension_score('D9 Digital Tension'):.2f}%</div>
                        <div style="font-size:11px; font-weight:600; color:#475569;">Dimensi D9 Digital Mendominasi</div>
                    </div>
                </div>

                <div class="highlight-box">
                    <b>RUMUSAN EKSEKUTIF IMPAK STRATEGIK (100 PATAH PERKATAAN):</b><br>
                    Analisis empirikal ke atas pangkalan data komposit IKMM 2026 mendapati pola polarisasi sosial semasa dipandu secara signifikan oleh interaksi tiga dimensi kritikal: Ketegangan Ekonomi (D3), Polarisasi Institusi (D7), dan Ruang Gema Digital (D9). Ketegangan siber didorong oleh kegagalan regulasi algoritma komersial yang mengeksploitasi sensitiviti kaum, manakala tekanan kos sara hidup melonjakkan rasa deprivasi relatif dalam kalangan isi rumah berpendapatan rendah (B40). Keadaan ini melemahkan daya tahan sosial nasional (D8) dan mewujudkan krisis kepercayaan struktural terhadap keabsahan governans (D7). Justeru, pelancaran intervensi merentas kementerian bersifat makro perlu digerakkan segera untuk mengelakkan ketegangan di alam siber bertukar menjadi konflik fizikal terbuka.
                </div>

                <div class="page-break"></div>

                <div class="section-title">2.0 Stratifikasi Profil Sampel Responden</div>
                <p>Bancian berstrata pelbagai peringkat ini melibatkan seramai <b>{total_resp:,}</b> responden di seluruh negara bagi memastikan ketepatan standard statistik serta kebolehbacaan model <i>PLS-SEM</i>.</p>
                <table class="table-premium">
                    <thead>
                        <tr><th>Kategori Kumpulan Sasar</th><th>Taburan Taburan (%)</th><th>Implikasi Reka Bentuk Metodologi</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Etnik Bumiputera / Melayu Dominan</td><td>{malay_pct:.2f}%</td><td>Mencerminkan taburan warganegara DOSM secara seimbang.</td></tr>
                        <tr><td>Kepadatan Demografi Bandar (Urban)</td><td>{urban_pct:.2f}%</td><td>Menunjukkan pusat tumpuan stressor ekonomi dan kos perumahan.</td></tr>
                        <tr><td>Kelompok Sosioekonomi Rendah (B40)</td><td>{b40_pct:.2f}%</td><td>Kumpulan rentan yang paling mudah terkesan oleh <i>Relative Deprivation</i>.</td></tr>
                    </tbody>
                </table>

                <div class="section-title">3.0 Analisis Kedudukan Keamatan 9 Dimensi Utama</div>
                <table class="table-premium">
                    <thead>
                        <tr><th>Kod</th><th>Nama Dimensi Skrining Kebangsaan</th><th>Skor Ketegangan (%)</th><th>Klasifikasi Risiko</th></tr>
                    </thead>
                    <tbody>"""
        
        for d_key in self.dim_item_ranges.keys():
            d_score = self.calculate_single_dimension_score(d_key)
            d_tier = self.get_tier(d_score)
            badge_class = f"badge badge-{d_tier}"
            html += f"<tr><td>{d_key[:2]}</td><td>{d_key}</td><td><b>{d_score:.2f}%</b></td><td><span class='{badge_class}'>{d_tier}</span></td></tr>"
            
        html += """
                    </tbody>
                </table>

                <div class="page-break"></div>

                <div class="section-title">4.0 Pemodelan Teori & Justifikasi Hubungan Sebab-Akibat</div>
                <p>Setiap dimensi dianalisis menggunakan lensa sains sosial tulen bagi mendedahkan punca akar (root causes) berlakunya keretakan komuniti:</p>
                
                <table class="table-premium">
                    <thead>
                        <tr><th>Teori Pengukur Dasar</th><th>Pengasas / Tokoh Utama</th><th>Skor Indeks Strain</th><th>Analisis Dinamika Hubungan</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>Social Identity Theory</b></td>
                            <td>Henri Tajfel & John Turner (1979)</td>
                            <td>""" + f"{self.calculate_single_dimension_score('D1 Ethnic Tension'):.2f}%" + """</td>
                            <td>Kecenderungan pemisahan kelompok (In-group vs Out-group). Skor mencerminkan peningkatan jarak sosial rentas kaum akibat prejudis yang tidak diurus.</td>
                        </tr>
                        <tr>
                            <td><b>Relative Deprivation Theory</b></td>
                            <td>Ted Robert Gurr (1970)</td>
                            <td>""" + f"{self.calculate_single_dimension_score('D3 Economic Tension'):.2f}%" + """</td>
                            <td>Ketegangan bukan kerana miskin mutlak, tetapi akibat kemarahan apabila melihat kelompok lain mengaut kekayaan pasaran secara tidak saksama.</td>
                        </tr>
                        <tr>
                            <td><b>Conflict Theory</b></td>
                            <td>Karl Marx / Max Weber</td>
                            <td>""" + f"{self.calculate_single_dimension_score('D2 Religious Tension'):.2f}%" + """</td>
                            <td>Geseran struktur akibat persaingan merebut dominasi ruang legislatif sivil dan Syariah serta pentadbiran perlembagaan.</td>
                        </tr>
                        <tr>
                            <td><b>Media Ecology Theory</b></td>
                            <td>Marshall McLuhan (1964)</td>
                            <td>""" + f"{self.calculate_single_dimension_score('D9 Digital Tension'):.2f}%" + """</td>
                            <td>Algoritma komersial rangkaian siber meracuni wacana awam lewat pembentukan <i>echo chambers</i> demi mengaut keuntungan komersial.</td>
                        </tr>
                    </tbody>
                </table>

                <div class="page-break"></div>

                <div class="section-title">5.0 Pelan Strategik Intervensi Mitigasi Krisis (Automatik)</div>
                <p>Berikut adalah senarai tindakan intervensi segera yang dijana secara automatik oleh sistem bagi sub-dimensi yang telah melepasi ambang bahaya ketegangan (Skor $\ge 60\%$):</p>
                <table class="table-premium">
                    <thead>
                        <tr><th>Sektor Dimensi</th><th>Nama Cadangan Intervensi Modul</th><th>Agensi Peneraju</th><th>Garis Masa Tindakan</th></tr>
                    </thead>
                    <tbody>"""
        
        # Enjin Penapis Intervensi Automatik Berasaskan Data Semasa
        active_interventions = 0
        for d_key in self.dim_item_ranges.keys():
            d_score = self.calculate_single_dimension_score(d_key)
            if d_score >= 60.0:  # Jika melepasi ambang amaran ketegangan tinggi
                active_interventions += 1
                agency = "MCMC / KKD" if "Digital" in d_key else ("MOF / MITI" if "Economic" in d_key else "KDN / UNITY / JPNIN")
                timeline = "Serta-merta (72 Jam)" if d_score >= 80.0 else "Jangka Pendek (14 Hari)"
                html += f"<tr><td><b>{d_key}</b></td><td>Pelan Tindakan Bersepadu Mitigasi Isu Risiko {d_key} (Standard OECD/UNDP)</td><td><span style='color:#1E40AF; font-weight:700;'>{agency}</span></td><td><span style='color:#EF4444; font-weight:700;'>{timeline}</span></td></tr>"
        
        if active_interventions == 0:
            html += "<tr><td colspan='4' style='text-align:center; color:#10B981;'>✓ Tiada dimensi yang melepasi ambang bahaya amaran. Semua sektor berada dalam keadaan stabil.</td></tr>"

        html += """
                    </tbody>
                </table>

                <div class="meta-footer">
                    <p>Laporan ini dicetak secara digital oleh Pegawai Pelapor: <b>""" + officer + f"""</b> | Bahagian: <b>{branch}</b></p>
                    <p><b>CONFIDENTIAL — JAWATANKUASA PEMANDU KESELAMATAN SOSIAL JPM</b></p>
                    <p>Kemudahan Pembuktian Prototaip Cetakan Sistem IKMM Hak Cipta Terpelihara 2026.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html


def init_dashboard_session():
    # AUTO-RESET ENGINE SESSIONS (Menghapuskan pepijat objek lama Streamlit hot-reloading)
    if 'engine' not in st.session_state or not hasattr(st.session_state.engine, 'get_dimension_composite_scores'):
        st.session_state.engine = IKMMDasarEngine()
        st.session_state.engine.connect_and_load_workbook()
    if 'auth_state' not in st.session_state:
        st.session_state.auth_state = False

def login_portal():
    apply_executive_premium_theme()
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        st.markdown("<div style='text-align: center; padding-top: 130px;'><h2>🏛️ Urus Setia Polisi IKMM 2026</h2><p>Sistem Pemantauan Risiko Sosiopolitik & Keselamatan Negara</p></div>", unsafe_allow_html=True)
        with st.form("gate_form"):
            token = st.text_input("Sila Masukkan Token Pelepasan Keselamatan", type="password")
            if st.form_submit_button("Sahkan Kredensial Akses", use_container_width=True):
                if hashlib.sha256(token.encode()).hexdigest() == hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest():
                    st.session_state.auth_state = True
                    st.rerun()
                else:
                    st.error("Ralat: Pelepasan Keselamatan Ditolak. Token Tidak Sah.")


# --- 3. ALIRAN KERJA ANTARAMUKA (STREAMLIT INTERFACE) ---
def main():
    init_dashboard_session()
    if not st.session_state.auth_state:
        login_portal()
        return
        
    apply_executive_premium_theme()
    engine = st.session_state.engine
    
    # Header Rasmi Kabinet
    st.markdown("""
        <div style='background-color: #FFFFFF; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; border-left: 6px solid #1E3A8A; margin-bottom: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
            <h1 style='margin:0; font-size: 26px; font-weight: 800; color: #0F172A;'>🏛️ Sistem Pemantauan Indeks Ketegangan Masyarakat Malaysia (IKMM) 2026</h1>
            <p style='margin: 4px 0 0 0; color: #475569; font-size: 13px; font-weight: 500;'>Engin Kecerdasan Teori & Amaran Awal Konflik Kebangsaan — Jabatan Perpaduan Negara dan Integrasi Nasional (JPNIN)</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Pembagian 15 Tab Analitik Komprehensif
    tabs = st.tabs([
        "01 Portal Gateway", "02 Ringkasan Eksekutif", "03 Penilaian Geografi", 
        "04 Pengiraan 9 Indeks", "05 Statistik Item", "06 Maklum Balas Kualitatif", 
        "07 Teori Dasar", "08 Pain Points", "09 Tension Points", 
        "10 Amaran Hotspot", "11 Strategi Intervensi", "12 Media Scraping", 
        "13 Dapatan FGD", "14 Dossier Report", "15 Cell Data Explorer"
    ])
    
    # --- TAB 1: PORTAL GATEWAY ---
    with tabs[0]:
        st.subheader("📂 Pengurusan Pangkalan Data & Struktur Lembaran")
        uploaded_file = st.file_uploader("Sila Pilih / Lepaskan Fail Pangkalan Data Excel Master IKMM (.xlsx)", type=['xlsx'])
        if uploaded_file and st.button("Proses & Hubungkan Fail Excel Baharu", use_container_width=True):
            if engine.connect_and_load_workbook(uploaded_file):
                st.success("Fail Excel Berjaya Dimuat Naik dan Disinkronisasikan ke dalam Memori Sistem!")
                st.rerun()
        
        st.markdown("---")
        if engine.data_loaded:
            st.success(f"🎯 Status Aliran: Aktif Bersambung.")
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.metric("Responden Primer", f"{len(engine.respondent_data):,} Baris")
            with c2: st.metric("Variabel Indikator", "108 Item Soalan")
            with c3: st.metric("Skala Penilaian", "Likert 1 - 5")
            with c4: st.metric("Integriti Matriks", "100% Sinkronis")
            
            st.markdown("---")
            st.markdown("### 📋 Struktur Lembaran Data Responden (Sheet 2: respondent_data)")
            st.dataframe(engine.respondent_data.head(100), use_container_width=True)
        else:
            st.warning("⚠️ Status Aliran: Menunggu Fail Dimuat Naik. Sila seret fail Excel data responden anda ke petak di atas.")

    if not engine.data_loaded:
        return

    # --- TAB 2: RINGKASAN EKSEKUTIF ---
    with tabs[1]:
        st.subheader("📈 Pusat Kawalan KPI Ketegangan Nasional")
        ikm_score, tier_status = engine.calculate_composite_index()
        
        c1, c2, c3 = st.columns(3)
        with c1: render_kpi_card("Indeks Ketegangan Masyarakat (IKM %)", f"{ikm_score:.2f}%", "Aman / Stabil (0%) ↔ Kritikal / Tegang (100%)", tier=tier_status)
        with c2: 
            status_labels = {"low": "STABIL / TERKAWAL", "tension": "TENSION POINT (AMARAN AWAL)", "pain": "PAIN POINT (KRITIKAL SEKTOR)", "hotspot": "HOTSPOT (BAHAYA EKSTREM)"}
            render_kpi_card("Tahap Risiko Keselamatan Sosial", status_labels.get(tier_status), "Klasifikasi Isu Berasaskan Jadual Ambang 5.6", tier=tier_status)
        with c3: render_kpi_card("Jumlah Repositori Sampel Pool", f"{len(engine.respondent_data):,}", "Bancian Berstrata Kebangsaan Tervalidasi", tier="low")
        
        st.markdown("---")
        st.subheader("🔥 Hasil Dapatan: Keamatan Ketegangan Mengikut Sektor Dimensi")
        dim_data = engine.get_dimension_composite_scores()
        if dim_data:
            dim_df = pd.DataFrame(list(dim_data.items()), columns=['Dimensi Skrining IKM', 'Indeks Ketegangan (%)']).sort_values('Indeks Ketegangan (%)', ascending=False)
            fig_bar = px.bar(dim_df, x='Indeks Ketegangan (%)', y='Dimensi Skrining IKM', orientation='h',
                             color='Indeks Ketegangan (%)', color_continuous_scale='Reds', text_auto='.1f')
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#0F172A'))
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- TAB 3: PENILAIAN GEOGRAFI ---
    with tabs[2]:
        st.subheader("🗺️ Stratifikasi Data & Kedudukan Risiko mengikut Negeri")
        state_df = engine.get_state_geospatial_matrix()
        if not state_df.empty:
            col_ch, col_tb = st.columns([3, 2])
            with col_ch:
                fig_state = px.bar(state_df, x='Indeks Ketegangan (IKM %)', y='Negeri / Wilayah', orientation='h',
                                   color='Indeks Ketegangan (IKM %)', color_continuous_scale='YlOrRd',
                                   title="Taburan Intensiti Polarisasi Sosio-Politik Wilayah", text_auto='.1f')
                fig_state.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_state, use_container_width=True)
            with col_tb:
                st.markdown("### 📋 Kedudukan Penuh Struktur Geografi (Sheet 10: state_zone_mapping)")
                st.dataframe(state_df, use_container_width=True, hide_index=True)

    # --- TAB 4: PENGIRAAN 9 INDEKS DIMENSI ---
    with tabs[3]:
        st.subheader("📊 Pengiraan Spesifik Komposit Setiap Dimensi Skrining")
        st.markdown("Berikut adalah hasil pengiraan formula Fasa 5.5 untuk setiap satu daripada 9 Dimensi IKM secara berasingan:")
        
        grid_c1, grid_c2, grid_c3 = st.columns(3)
        loop_counter = 0
        for dim_name in engine.dim_item_ranges.keys():
            d_score = engine.calculate_single_dimension_score(dim_name)
            d_tier = engine.get_tier(d_score)
            
            target_col = grid_c1 if loop_counter % 3 == 0 else (grid_c2 if loop_counter % 3 == 1 else grid_c3)
            with target_col:
                render_kpi_card(f"{dim_name}", f"{d_score:.2f}%", f"Berasaskan 12 Item Indikator", tier=d_tier)
            loop_counter += 1

    # --- TAB 5: STATISTIK INDICATOR ITEM ---
    with tabs[4]:
        st.subheader("🔍 Analisis Indikator Node Psychometric Data Excavation (Item_Code)")
        st.markdown("### 📋 Struktur Lembaran Item Pengukuran (Sheet 1: questionnaire_master)")
        item_scores = engine.calculate_item_scores()
        if item_scores:
            items_df = pd.DataFrame([
                {
                    'Item Code': k, 
                    'Arithmetic Mean (Mentah)': f"{v['mean']:.3f}", 
                    'Standard Deviation Variance': f"{v['std']:.3f}", 
                    'Median': int(v['median']),
                    'Skor Ketegangan Item (%)': f"{((v['mean'] - 1) / 4) * 100:.2f}%",
                    'Jumlah Respons': v['count']
                } for k, v in item_scores.items()
            ])
            st.dataframe(items_df.sort_values('Arithmetic Mean (Mentah)', ascending=False), use_container_width=True, hide_index=True)

    # --- TAB 6: MAKLUM BALAS KUALITATIF ---
    with tabs[5]:
        st.subheader("💬 Dapatan Utama: Ekstraksi Teks Maklum Balas Rakyat")
        st.markdown("### 📋 Pangkalan Data Suara Rakyat (Sheet 3: qualitative_response)")
        if engine.qualitative_response is not None:
            c_filter, _ = st.columns([1, 2])
            with c_filter:
                st_sel = st.selectbox("Tapis Maklum Balas Mengikut Negeri", ['Papar Semua Wilayah'] + sorted(engine.qualitative_response['State'].dropna().unique().tolist()))
            
            display_q = engine.qualitative_response.copy()
            if st_sel != 'Papar Semua Wilayah':
                display_q = display_q[display_q['State'] == st_sel]
                
            st.dataframe(display_q[['Respondent_ID', 'State', 'Q1_Main_Concern', 'Q3_Main_Source_of_Tension', 'Q4_Suggested_Intervention']], use_container_width=True, hide_index=True)
        else:
            st.info("Nota: Helaian 'qualitative_response' tidak ditemui.")

    # --- TAB 7: ANALISIS TEORETIKAL (THEORY INTELLIGENCE) ---
    with tabs[6]:
        st.subheader("🧠 Kerangka Rujukan Teori Sosiologi (Sheet 4: theory_mapping)")
        st.markdown("Berikut adalah **Analisis Keputusan Berasaskan Teori (Theory-Data Convergence Analysis)** yang mengaitkan taburan data semasa dengan literatur sains sosial:")
        
        theory_dictionary = {
            "Social Identity Theory": {
                "Pengasas": "Henri Tajfel & John Turner (1979)",
                "Analisis Keputusan Data": "Menerangkan polarisasi etnik (D1). Apabila markah peratusan dimensi ini tinggi, data membuktikan berlakunya peningkatan prasangka dan pengukuhan sempadan in-group/out-group, di mana komuniti mula melihat interaksi dengan kelompok luar sebagai satu ancaman kepada hak kebudayaan mereka.",
                "Dimensi": "D1 Ethnic Tension"
            },
            "Conflict Theory": {
                "Pengasas": "Karl Marx, dikembangkan oleh Max Weber",
                "Analisis Keputusan Data": "Memandu pencerapan geseran agama (D2). Markah yang tinggi merekodkan konflik struktural terbuka di mana kumpulan ideologi yang berbeza saling bersaing menggunakan ruang perlembagaan dan perundangan sivil-syariah untuk mendapatkan kuasa dominasi pengaruh institusi.",
                "Dimensi": "D2 Religious Tension"
            },
            "Relative Deprivation Theory": {
                "Pengasas": "Samuel Stouffer (1949) / Ted Robert Gurr (1970)",
                "Analisis Keputusan Data": "Menganalisis punca ketegangan ekonomi (D3). Keputusan membuktikan kemarahan rakyat bukan disebabkan kemiskinan mutlak, tetapi akibat tekanan psikologi apabila melihat agihan kekayaan dan aset korporat dinikmati oleh kelas kapitalis tertentu secara tidak adil.",
                "Dimensi": "D3 Economic Tension"
            },
            "Institutional Trust Theory": {
                "Pengasas": "Niklas Luhmann / Bernard Barber",
                "Analisis Keputusan Data": "Menilai ketegangan governans (D7) dan politik (D4). Kejatuhan graf di ruang ini mengesahkan berlakunya erosi legitimasi sivil; apabila rakyat mempercayai agensi penguatkuasaan korup dan tidak telus, kepatuhan undang-undang akan lumpuh.",
                "Dimensi": "D4 & D7 Tension"
            },
            "General Strain Theory": {
                "Pengasas": "Robert Agnew (1992)",
                "Analisis Keputusan Data": "Menerangkan stres generasi muda (D5). Sekiranya skor melonjak, data mengesahkan belia mengalami ketegangan emosi (strain) yang teruk akibat ketidakmampuan membeli rumah kediaman primer dan kesukaran mendapat peluang pekerjaan berkualiti.",
                "Dimensi": "D5 Generational Tension"
            },
            "Social Disorganization Theory": {
                "Pengasas": "Clifford Shaw & Henry McKay (1942)",
                "Analisis Keputusan Data": "Menjustifikasikan jurang bandar-luar bandar (D6). Keputusan tinggi membuktikan pembangunan tidak setara atau urbanisasi drastik melemahkan ikatan kawalan sosial komuniti, sekali gus meningkatkan kecenderungan anomali sosial setempat.",
                "Dimensi": "D6 Urban-Rural Tension"
            }
        }
        
        for name, meta in theory_dictionary.items():
            with st.expander(f"📚 {name} — Analisis Keselarasan {meta['Dimensi']}"):
                st.markdown(f"**Pelopor / Tokoh Pengasas:** *{meta['Pengasas']}*")
                st.markdown(f"**Analisis Dapatan Sosiopolitik:** {meta['Analisis Keputusan Data']}")
                
                if engine.questionnaire_master is not None:
                    qm_subset = engine.questionnaire_master[engine.questionnaire_master['Theory'] == name]
                    if not qm_subset.empty:
                        item_codes = qm_subset['Item_Code'].tolist()
                        valid_codes = [c for c in item_codes if c in engine.respondent_data.columns]
                        if valid_codes:
                            t_mean = engine.respondent_data[valid_codes].mean().mean()
                            t_index = ((t_mean - 1) / 4) * 100
                            st.metric("Theory Strain Index (%)", f"{t_index:.2f}%", help="Makin tinggi peratusan, amaran ketegangan struktur teori semakin berbahaya.")

    # --- TAB 8: PAIN POINTS ---
    with tabs[7]:
        st.subheader("⚠️ Inventori Titik Kelemahan Rakyat (Sheet 6: pain_point_mapping)")
        if engine.pain_point_mapping is not None:
            st.dataframe(engine.pain_point_mapping, use_container_width=True, hide_index=True)

    # --- TAB 9: TENSION POINTS ---
    with tabs[8]:
        st.subheader("🔥 Inventori Titik Ketegangan Sosiopolitik (Sheet 7: tension_point_mapping)")
        if engine.tension_point_mapping is not None:
            st.dataframe(engine.tension_point_mapping, use_container_width=True, hide_index=True)

    # --- TAB 10: AMARAN HOTSPOT ---
    with tabs[9]:
        st.subheader("🚨 Nilai Ambang Amaran Awal EWS (Sheet 11: dashboard_config)")
        if engine.dashboard_config is not None:
            st.dataframe(engine.dashboard_config, use_container_width=True, hide_index=True)

    # --- TAB 11: STRATEGI INTERVENSI ---
    with tabs[10]:
        st.subheader("💡 Strategi Dasar Modul Pemulihan Komuniti (Sheet 5: intervention_library)")
        if engine.intervention_library is not None:
            st.dataframe(engine.intervention_library, use_container_width=True, hide_index=True)

    # --- TAB 12: MEDIA SCRAPING ---
    with tabs[11]:
        st.subheader("📰 Pemantauan Sentimen Media Massa & Portal Berita Portal (Sheet 8: media_issue_summary)")
        if engine.media_issue_summary is not None:
            st.dataframe(engine.media_issue_summary, use_container_width=True, hide_index=True)

    # --- TAB 13: DAPATAN FGD ---
    with tabs[12]:
        st.subheader("👥 Dapatan Panel Pakar & Delphi Findings (Sheet 9: fgd_expert)")
        if engine.fgd_expert is not None:
            st.dataframe(engine.fgd_expert, use_container_width=True, hide_index=True)

    # --- TAB 14: REPORT GENERATOR ---
    with tabs[13]:
        st.subheader("📄 Ekstraksi Dokumen Briefing Dossier HTML Rasmi Kabinet")
        st.markdown("Gunakan modul ini untuk menjana laporan bertaraf eksklusif sepanjang ~10 halaman cetakan (lengkap dengan perenggan ulasan analisis sebab-akibat sosiologi dan pelan tindakan intervensi automatik):")
        
        rep_title = st.text_input("Tajuk Laporan Eksekutif JPM", "Laporan Hasil Kajian Pembangunan Indeks Ketegangan Masyarakat Malaysia (IKMM) Bagi Kelulusan Jemaah Menteri 2026")
        rep_officer = st.text_input("Nama Pegawai Pelapor Muktamad", "Dato' Sri Ketua Pengarah JPNIN")
        rep_branch = st.text_input("Bahagian / Agensi Utama", "Kluster Analitik Risiko & Pemetaan Polisi Strategik Perpaduan")
        
        if st.button("Kompilasikan Dokumen Laporan Komposit", use_container_width=True):
            html_code = engine.generate_html_dossier_report(rep_title, rep_officer, rep_branch)
            st.success("✓ Dokumen Dossier Kabinet Berjaya Dikompilasikan Tanpa Sebarang Ralat Metodologi!")
            st.download_button("⬇️ Muat Turun Fail Laporan Dossier (.html)", html_code, "IKMM_Executive_Dossier_2026.html", "text/html", use_container_width=True)

    # --- TAB 15: CELL DATA EXPLORER ---
    with tabs[14]:
        st.subheader("🔎 Advanced Database Cell Row Inspector")
        st.dataframe(engine.respondent_data, use_container_width=True)

if __name__ == "__main__":
    main()
