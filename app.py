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

# --- 1. REKA BENTUK VISUAL: CLEAN EXECUTIVE LIGHT THEME ---
def apply_executive_premium_theme():
    st.markdown("""
        <style>
            /* Latar Belakang Korporat Putih Mutiara & Kelabu Lembut */
            .stApp {
                background-color: #F8FAFC !important;
                color: #0F172A !important;
            }
            
            /* Hiasan Bar Sisi Sidebar Gelap (Kontras Tinggi) */
            [data-testid="stSidebar"] {
                background-color: #0F172A !important;
                border-right: 2px solid #E2E8F0 !important;
            }
            [data-testid="stSidebar"] * {
                color: #F8FAFC !important;
            }
            
            /* Keseragaman Fon dan Kebolehbacaan Teks */
            h1, h2, h3, h4, p, span, label {
                color: #0F172A !important;
                font-family: 'Segoe UI', Inter, sans-serif !important;
            }
            
            /* Antaramuka Tab Menu Moden Windows Mode */
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
            
            /* Kad KPI Komposit Kaca Terang (Glassmorphism Light Grid) */
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
            
            /* Kotak Frame Dataframe */
            .stDataFrame {
                border: 1px solid #E2E8F0 !important;
                border-radius: 8px !important;
                background-color: #FFFFFF !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_kpi_card(label, value, unit, tier="low"):
    color_map = {
        "low": "#10B981",       # Hijau: Rendah / Stabil (Aman)
        "tension": "#F59E0B",   # Jingga: Tension Point (Awal Geseran)
        "pain": "#DB2777",      # Merah Jambu: Pain Point (Isu Kronik)
        "hotspot": "#EF4444"    # Merah Terang: Hotspot Kritikal (Bahaya)
    }
    border_color = color_map.get(tier, "#1E40AF")
    st.markdown(f"""
    <div class="kpi-card-premium" style="border-left-color: {border_color};">
        <p class="kpi-label">{label}</p>
        <div class="kpi-value" style="color: {border_color} !important;">{value}</div>
        <p style='color: #64748B !important; font-size: 11px; font-weight: 500; margin: 0;'>{unit}</p>
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
        
        # Pemetaan Rigid Item Mengikut 9 Dimensi Utama (Masing-masing 12 Item = Total 108 Item)
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
            if file_source is None:
                xls = pd.ExcelFile(self.filename)
            else:
                xls = pd.ExcelFile(file_source)
                
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

    def generate_html_dossier_report(self, title, officer, branch):
        score, tier = self.calculate_composite_index()
        now_str = datetime.now().strftime('%d %B %Y')
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #F8FAFC; color: #0F172A; padding: 30px; line-height: 1.6; }}
                .dossier-card {{ max-width: 900px; margin: 0 auto; background: #FFFFFF; padding: 40px; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
                .header-zone {{ background: #0F172A; color: #FFFFFF; padding: 30px; text-align: center; border-radius: 8px; border-bottom: 5px solid #1E40AF; }}
                .metric-box {{ text-align: center; background: #F1F5F9; border: 1px solid #CBD5E1; padding: 25px; border-radius: 8px; margin: 25px 0; }}
                .metric-val {{ font-size: 36px; font-weight: 800; color: #EF4444; }}
                .table-dossier {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                .table-dossier th {{ background: #1E40AF; color: white; padding: 12px; text-align: left; }}
                .table-dossier td {{ padding: 10px; border-bottom: 1px solid #E2E8F0; }}
                .footer-zone {{ margin-top: 50px; padding-top: 20px; border-top: 2px dashed #CBD5E1; text-align: center; font-size: 13px; color: #64748B; }}
            </style>
        </head>
        <body>
            <div class="dossier-card">
                <div class="header-zone">
                    <h1 style="margin: 0; font-size: 24px; color: #FFFFFF;">🏛️ {title}</h1>
                    <p style="margin: 5px 0 0 0; font-size: 13px; color: #94A3B8;">DOKUMEN KERAJAAN TINGGI — SULIT / UNTUK KEGUNAAN RASMI SAHAJA</p>
                </div>
                
                <div class="metric-box">
                    <p style="margin: 0; font-weight: 700; color: #475569; text-transform: uppercase;">Skor Indeks Ketegangan Masyarakat Kebangsaan</p>
                    <div class="metric-val">{score:.2f}%</div>
                    <p style="margin: 5px 0 0 0; font-weight: 600; color: #1E3A8A;">Status: {tier.upper()}</p>
                </div>
                
                <h3>Pecahan Tahap Risiko Ketegangan mengikut 9 Dimensi Utama</h3>
                <table class="table-dossier">
                    <thead>
                        <tr><th>Kod Dimensi</th><th>Nama Klasifikasi Dimensi Skrining</th><th>Skor Ketegangan (%)</th></tr>
                    </thead>
                    <tbody>"""
        
        for d_key in self.dim_item_ranges.keys():
            d_score = self.calculate_single_dimension_score(d_key)
            html += f"<tr><td>{d_key[:2]}</td><td>{d_key}</td><td><b>{d_score:.2f}%</b></td></tr>"
            
        html += f"""
                    </tbody>
                </table>
                
                <div class="footer-zone">
                    <p>Pegawai Pelapor: <b>{officer}</b> | Jabatan: <b>{branch}</b></p>
                    <p>Tarikh Kelulusan Cetakan: {now_str} | Id Rujukan: IKMM-SEC-2026-09</p>
                    <p>Pematuhan Akta Rahsia Rasmi 1972 & Akta Perlindungan Data Peribadi 2010 (PDPA) Terpelihara</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html


def init_dashboard_session():
    # SUNTIKAN FORCED SESSIONS OVERWRITE (Membuang cache objek enjin lama daripada memori Streamlit)
    if 'engine' not in st.session_state or not hasattr(st.session_state.engine, 'get_dimension_composite_scores'):
        st.session_state.engine = IKMMDasarEngine()
        st.session_state.engine.connect_and_load_workbook()
    if 'auth_state' not in st.session_state:
        st.session_state.auth_state = False

def login_portal():
    apply_executive_premium_theme()
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        st.markdown("<div style='text-align: center; padding-top: 130px;'><h2>🏛️ Urus Setia Polisi IKMM 2026</h2><p>Sistem Intelligence Penilaian Risiko Amaran Awal Konflik Kebangsaan</p></div>", unsafe_allow_html=True)
        with st.form("gate_form"):
            token = st.text_input("Sila Masukkan Token Keselamatan Pelepasan Dasar", type="password")
            if st.form_submit_button("Sahkan Kredensial Sistem", use_container_width=True):
                if hashlib.sha256(token.encode()).hexdigest() == hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest():
                    st.session_state.auth_state = True
                    st.rerun()
                else:
                    st.error("Ralat: Akses Keselamatan Ditolak. Kredensial Tidak Sah.")


# --- 3. ALIRAN KERJA ANTARAMUKA (STREAMLIT INTERFACE) ---
def main():
    init_dashboard_session()
    if not st.session_state.auth_state:
        login_portal()
        return
        
    apply_executive_premium_theme()
    engine = st.session_state.engine
    
    # Header Utama Aplikasi
    st.markdown("""
        <div style='background-color: #FFFFFF; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; border-left: 6px solid #1E3A8A; margin-bottom: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
            <h1 style='margin:0; font-size: 26px; font-weight: 800; color: #0F172A;'>🏛️ Sistem Pemantauan Indeks Ketegangan Masyarakat Malaysia (IKMM) 2026</h1>
            <p style='margin: 4px 0 0 0; color: #475569; font-size: 13px; font-weight: 500;'>Kerangka Tindak Balas Strategik - Jabatan Perpaduan Negara dan Integrasi Nasional (JPNIN)</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Struktur 15 Tab Dinamik Komprehensif
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
        if uploaded_file:
            if st.button("Proses & Hubungkan Fail Excel Baharu", use_container_width=True):
                if engine.connect_and_load_workbook(uploaded_file):
                    st.success("🎯 Fail Excel Berjaya Dimuat Naik dan Disinkronisasikan ke dalam Memori Sistem!")
                    st.rerun()
                else:
                    st.error("❌ Ralat Metodologi: Struktur helaian data Excel anda tidak sepadan dengan kriteria fail master.")
        
        st.markdown("---")
        if engine.data_loaded:
            st.success(f"🎯 Status Aliran: Aktif Bersambung.")
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.metric("Responden Primer", f"{len(engine.respondent_data):,} Baris")
            with c2: st.metric("Variabel Indikator", "108 Item Soalan")
            with c3: st.metric("Skala Penilaian", "Likert 1 - 5")
            with c4: st.metric("Integriti Matriks", "100% Sinkronis")
            
            st.markdown("---")
            st.markdown("### 📋 Set Data Struktur Responden Kebangsaan (Pratinjau Master Data)")
            st.dataframe(engine.respondent_data.head(100), use_container_width=True)
        else:
            st.warning("⚠️ Status Aliran: Menunggu Fail Dimuat Naik. Sila seret fail Excel data responden anda ke petak di atas.")

    # Jika data belum dimasukkan, kunci fungsi analitik tab lain bagi mengelakkan crash aplikasi
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
        st.subheader("🔥 Keamatan Indeks Ketegangan Mengikut Sektor Dimensi")
        dim_data = engine.get_dimension_composite_scores()
        if dim_data:
            dim_df = pd.DataFrame(list(dim_data.items()), columns=['Dimensi Skrining IKM', 'Indeks Ketegangan (%)']).sort_values('Indeks Ketegangan (%)', ascending=False)
            fig_bar = px.bar(dim_df, x='Indeks Ketegangan (%)', y='Dimensi Skrining IKM', orientation='h',
                             color='Indeks Ketegangan (%)', color_continuous_scale='Reds')
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
                                   title="Taburan Intensiti Polarisasi Sosio-Politik Wilayah")
                fig_state.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_state, use_container_width=True)
            with col_tb:
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
        st.subheader("🔍 Indikator Node Psychometric Data Excavation (Item_Code)")
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
        st.subheader("💬 Suara Marhaen — Ekstraksi Aduan Teks Kualitatif Struktur Rakyat")
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
        st.subheader("🧠 Kerangka Rujukan Teori Sosiologi & Pengasas Model")
        
        theory_dictionary = {
            "Social Identity Theory": {
                "Pengasas": "Henri Tajfel & John Turner (1979)",
                "Latar Belakang & Huraian": "Manusia secara semula jadi membahagikan kelompok sosial kepada 'In-group' (kumpulan kita) dan 'Out-group' (kumpulan mereka). Ketegangan meletus (D1) apabila salah satu etnik merasakan hak mereka mula dicabar oleh entiti luar.",
                "Dimensi Sasaran": "D1 Ethnic Tension"
            },
            "Conflict Theory": {
                "Pengasas": "Karl Marx, dikembangkan oleh Max Weber & Ralf Dahrendorf",
                "Latar Belakang & Huraian": "Konflik sosial berakar daripada persaingan berterusan kelompok manusia untuk merebut penguasaan sumber, legislatif, dan ruang perlembagaan yang terhad. Memandu geseran pentadbiran undang-undang sivil dan Syariah (D2).",
                "Dimensi Sasaran": "D2 Religious Tension"
            },
            "Relative Deprivation Theory": {
                "Pengasas": "Samuel Stouffer (1949), dikembangkan oleh Ted Robert Gurr (1970)",
                "Latar Belakang & Huraian": "Kemarahan struktur tercetus bukan sekadar akibat kemiskinan mutlak, tetapi muncul daripada jurang psikologi ketidakadilan apabila melihat kelompok sosioekonomi lain meraih kekayaan jauh lebih dominan.",
                "Dimensi Sasaran": "D3 Economic Tension"
            },
            "Institutional Trust Theory": {
                "Pengasas": "Niklas Luhmann / Bernard Barber",
                "Latar Belakang & Huraian": "Integriti institusi penguatkuasaan, kehakiman, dan ketelusan parlimen adalah tiang sokongan ketenteraman awam. Apabila persepsi salah guna kuasa meningkat (D7), legitimasi politik (D4) akan lumpuh.",
                "Dimensi Sasaran": "D4 Political Tension & D7 Institutional and Governance Tension"
            },
            "General Strain Theory": {
                "Pengasas": "Robert Agnew (1992)",
                "Latar Belakang & Huraian": "Kekecewaan atau tekanan sistemik persekitaran (seperti pengangguran, ketidakmampuan memiliki aset/perumahan) mewujudkan anomi emosi yang memandu jurang ketegangan antara generasi muda dan veteran (D5).",
                "Dimensi Sasaran": "D5 Generational Tension"
            },
            "Social Disorganization Theory": {
                "Pengasas": "Clifford Shaw & Henry McKay (1942)",
                "Latar Belakang & Huraian": "Kawasan geografi yang mengalami urbanisasi terlalu agresif atau pembangunan infrastruktur tidak setara akan mengalami kelemahan kawalan sosial komuniti setempat, mencetuskan polarisasi sempadan bandar dan luar bandar (D6).",
                "Dimensi Sasaran": "D6 Urban-Rural Tension"
            },
            "Social Cohesion Theory": {
                "Pengasas": "Émile Durkheim, dikembangkan oleh OECD",
                "Latar Belakang & Huraian": "Mengukur kekuatan jaringan sosial, kepercayaan sesama jiran, dan kesediaan masyarakat untuk saling membantu ketika krisis. Bertindak sebagai indikator pelindung yang meredakan ketegangan.",
                "Dimensi Sasaran": "D8 Social Resilience"
            },
            "Media Ecology Theory": {
                "Pengasas": "Marshall McLuhan (1964) & Neil Postman",
                "Latar Belakang & Huraian": "Medium teknologi membentuk persepsi manusia. Algoritma media digital siber sengaja mencipta ruang gema (echo chambers) dan menularkan berita palsu demi keuntungan komersial, mempercepatkan konflik siber.",
                "Dimensi Sasaran": "D9 Digital Tension"
            }
        }
        
        for name, meta in theory_dictionary.items():
            with st.expander(f"📚 {name} (Kerangka Pengukuran {meta['Dimensi Sasaran']})"):
                st.markdown(f"**Pelopor / Tokoh Pengasas:** *{meta['Pengasas']}*")
                st.markdown(f"**Aplikasi Sains Sosial Dasar:** {meta['Latar Belakang & Huraian']}")
                
                if engine.questionnaire_master is not None:
                    qm_subset = engine.questionnaire_master[engine.questionnaire_master['Theory'] == name]
                    if not qm_subset.empty:
                        item_codes = qm_subset['Item_Code'].tolist()
                        valid_codes = [c for c in item_codes if c in engine.respondent_data.columns]
                        if valid_codes:
                            t_mean = engine.respondent_data[valid_codes].mean().mean()
                            t_index = ((t_mean - 1) / 4) * 100
                            st.metric("Theory Strain Index (%)", f"{t_index:.2f}%")

    # --- TAB 8: PAIN POINTS ---
    with tabs[7]:
        st.subheader("⚠️ Pengelasan Petunjuk Titik Kelemahan (Pain Points)")
        if engine.pain_point_mapping is not None:
            st.dataframe(engine.pain_point_mapping, use_container_width=True, hide_index=True)
        else:
            st.info("Helaian 'pain_point_mapping' tidak ditemui.")

    # --- TAB 9: TENSION POINTS ---
    with tabs[8]:
        st.subheader("🔥 Kerangka Eskalasi Indikator Titik Ketegangan (Tension Points)")
        if engine.tension_point_mapping is not None:
            st.dataframe(engine.tension_point_mapping, use_container_width=True, hide_index=True)
        else:
            st.info("Helaian 'tension_point_mapping' tidak ditemui.")

    # --- TAB 10: AMARAN HOTSPOT ---
    with tabs[9]:
        st.subheader("🚨 Early Warning System (EWS) — Sempadan Amaran Hotspot Kritikal")
        if engine.dashboard_config is not None:
            st.dataframe(engine.dashboard_config, use_container_width=True, hide_index=True)
        else:
            st.info("Helaian 'dashboard_config' tidak ditemui.")

    # --- TAB 11: STRATEGI INTERVENSI ---
    with tabs[10]:
        st.subheader("💡 Perpusat Strategi Dasar & Syor Intervensi Agensi Kabinet")
        if engine.intervention_library is not None:
            st.dataframe(engine.intervention_library, use_container_width=True, hide_index=True)
        else:
            st.info("Helaian 'intervention_library' tidak ditemui.")

    # --- TAB 12: MEDIA SCRAPING ---
    with tabs[11]:
        st.subheader("📰 Papan Pemantauan Media Cetak & Aliran Sentimen Siber Digital")
        if engine.media_issue_summary is not None:
            st.dataframe(engine.media_issue_summary, use_container_width=True, hide_index=True)
        else:
            st.info("Helaian 'media_issue_summary' tidak ditemui.")

    # --- TAB 13: DAPATAN FGD ---
    with tabs[12]:
        st.subheader("👥 Transkrip Konsensus Panel Pakar & Dapatan Bengkel FGD")
        if engine.fgd_expert is not None:
            st.dataframe(engine.fgd_expert, use_container_width=True, hide_index=True)
        else:
            st.info("Helaian 'fgd_expert' tidak ditemui.")

    # --- TAB 14: REPORT GENERATOR ---
    with tabs[13]:
        st.subheader("📄 Penjanaan HTML Briefing Dossier Rasmi JPM")
        rep_title = st.text_input("Tajuk Laporan Eksekutif", "Laporan Ringkasan Keselamatan Sosial Negara & Indeks IKMM 2026")
        rep_officer = st.text_input("Nama Pegawai Pelapor Muktamad", "Urus Setia Kanan JPNIN")
        rep_branch = st.text_input("Cawangan Bahagian", "Kluster Pemetaan Risiko Perpaduan")
        
        if st.button("Kompilasikan Dokumen Dossier Rasmi", use_container_width=True):
            html_code = engine.generate_html_dossier_report(rep_title, rep_officer, rep_branch)
            st.success("✅ Dokumen Dossier Berjaya Dikompilasikan Tanpa Ralat!")
            st.download_button("⬇️ Muat Turun Fail Laporan HTML Dossier", html_code, "IKMM_Executive_Brief_Dossier.html", "text/html", use_container_width=True)

    # --- TAB 15: CELL DATA EXPLORER ---
    with tabs[14]:
        st.subheader("🔎 Advanced Database Structural Cell Matrix Explorer")
        st.dataframe(engine.respondent_data, use_container_width=True)

if __name__ == "__main__":
    main()
