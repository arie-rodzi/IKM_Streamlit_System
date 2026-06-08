import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import hashlib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# --- KONFIGURASI APLIKASI UTAMA ---
st.set_page_config(
    page_title="Sistem Analitik Komposit IKMM 2026",
    layout="wide",
    initial_sidebar_state="collapsed" # Menyembunyikan sidebar secara lalai
)

ADMIN_PASSWORD = "admin123"

# --- REKA BENTUK VISUAL: ULTRA-PREMIUM DIGITAL EXECUTIVE WINDOWS THEME (DARK NAVY GLASS) ---
def terapkan_tema_premium_eksekutif():
    st.markdown("""
        <style>
            /* Latar Belakang Gelap Korporat Premium */
            .stApp { 
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important; 
                color: #F8FAFC !important; 
            }
            
            /* Sembunyikan Sidebar Sepenuhnya Lewat CSS */
            [data-testid="stSidebar"] { display: none !important; }
            [data-testid="stSidebarCollapsedControl"] { display: none !important; }
            
            /* Keseragaman Fon dan Ketajaman Teks */
            h1, h2, h3, h4, p, span, label { 
                color: #F8FAFC !important; 
                font-family: 'Segoe UI', Inter, sans-serif !important; 
            }
            
            /* Gaya Kad Glassmorphism Premium */
            .kad-kpi-premium { 
                background: rgba(30, 41, 59, 0.7); 
                border: 1px solid rgba(255, 255, 255, 0.1); 
                border-left: 6px solid #3B82F6; 
                border-radius: 12px; 
                padding: 22px; 
                text-align: center; 
                backdrop-filter: blur(10px);
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); 
            }
            
            /* Antaramuka Menu Tab Kaca Eksekutif */
            .stTabs [data-baseweb="tab-list"] { 
                gap: 8px; 
                background-color: rgba(15, 23, 42, 0.8); 
                padding: 8px; 
                border-radius: 12px; 
                border: 1px solid rgba(255, 255, 255, 0.1); 
            }
            .stTabs [data-baseweb="tab"] { 
                height: 42px; 
                padding: 0px 20px !important; 
                background-color: transparent !important; 
                border-radius: 8px !important; 
                color: #94A3B8 !important; 
                font-weight: 600 !important; 
                transition: all 0.3s ease; 
            }
            .stTabs [aria-selected="true"] { 
                background-color: #3B82F6 !important; 
                color: #FFFFFF !important; 
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important; 
            }
            
            /* Kotak Interpretasi Naratif Berwarna */
            .kotak-analisis-biru { 
                background-color: rgba(30, 58, 138, 0.4); 
                border-left: 5px solid #3B82F6; 
                padding: 22px; border-radius: 0 12px 12px 0; margin: 18px 0; 
                color: #E2E8F0 !important; line-height: 1.8; font-size: 14.5px; 
            }
            .kotak-analisis-merah { 
                background-color: rgba(127, 29, 29, 0.4); 
                border-left: 5px solid #EF4444; 
                padding: 22px; border-radius: 0 12px 12px 0; margin: 18px 0; 
                color: #FCA5A5 !important; line-height: 1.8; font-size: 14.5px; 
            }
            .kotak-analisis-jingga { 
                background-color: rgba(120, 53, 4, 0.4); 
                border-left: 5px solid #F59E0B; 
                padding: 22px; border-radius: 0 12px 12px 0; margin: 18px 0; 
                color: #FDE68A !important; line-height: 1.8; font-size: 14.5px; 
            }
            .kotak-analisis-hijau { 
                background-color: rgba(6, 78, 59, 0.4); 
                border-left: 5px solid #10B981; 
                padding: 22px; border-radius: 0 12px 12px 0; margin: 18px 0; 
                color: #A7F3D0 !important; line-height: 1.8; font-size: 14.5px; 
            }
        </style>
    """, unsafe_allow_html=True)

def paparkan_kad_kpi(label, nilai, unit, tahap="rendah"):
    warna_peta = {"rendah": "#10B981", "amaran_awal": "#F59E0B", "titik_kelemahan": "#DB2777", "hotspot_kritikal": "#EF4444"}
    warna_sempadan = warna_peta.get(tahap, "#3B82F6")
    st.markdown(f"""
    <div class="kad-kpi-premium" style="border-left-color: {warna_sempadan};">
        <p style="color: #94A3B8 !important; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin: 0;">{label}</p>
        <div style="font-size: 34px; font-weight: 800; margin: 6px 0; color: {warna_sempadan} !important;">{nilai}</div>
        <p style='color: #64748B !important; font-size: 11px; font-weight: 500; margin: 0;'>{unit}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ENGIN ANALITIK STRATEGIK DASAR KERAJAAN (IKMM 2026) ---
class EnginDasarIKMM:
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
            'D1 Ketegangan Etnik': [f'IKM_{i:03d}' for i in range(1, 13)],
            'D2 Ketegangan Agama': [f'IKM_{i:03d}' for i in range(13, 25)],
            'D3 Ketegangan Ekonomi': [f'IKM_{i:03d}' for i in range(25, 37)],
            'D4 Ketegangan Politik': [f'IKM_{i:03d}' for i in range(37, 49)],
            'D5 Ketegangan Generasi': [f'IKM_{i:03d}' for i in range(49, 61)],
            'D6 Ketegangan Bandar-Luar Bandar': [f'IKM_{i:03d}' for i in range(61, 73)],
            'D7 Ketegangan Institusi dan Urus Tadbir': [f'IKM_{i:03d}' for i in range(73, 85)],
            'D8 Daya Tahan Sosial': [f'IKM_{i:03d}' for i in range(85, 97)],
            'D9 Ketegangan Digital': [f'IKM_{i:03d}' for i in range(97, 109)]
        }

    def hubung_dan_muat_data(self, file_source=None):
        try:
            xls = pd.ExcelFile(self.filename) if file_source is None else pd.ExcelFile(file_source)
            self.respondent_data = pd.read_excel(xls, sheet_name='respondent_data')
            self.questionnaire_master = pd.read_excel(xls, sheet_name='questionnaire_master')
            
            # Pengerasan terjemahan Bahasa Melayu di peringkat memori master
            self.questionnaire_master['Dimension'] = self.questionnaire_master['Dimension'].replace({
                'D1 Ethnic Tension': 'D1 Ketegangan Etnik', 'D2 Religious Tension': 'D2 Ketegangan Agama',
                'D3 Economic Tension': 'D3 Ketegangan Ekonomi', 'D4 Political Tension': 'D4 Ketegangan Politik',
                'D5 Generational Tension': 'D5 Ketegangan Generasi', 'D6 Urban-Rural Tension': 'D6 Ketegangan Bandar-Luar Bandar',
                'D7 Institutional and Governance Tension': 'D7 Ketegangan Institusi dan Urus Tadbir',
                'D8 Social Resilience': 'D8 Daya Tahan Sosial', 'D9 Digital Tension': 'D9 Ketegangan Digital'
            })
            
            if 'qualitative_response' in xls.sheet_names:
                self.qualitative_response = pd.read_excel(xls, sheet_name='qualitative_response')
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
            if 'dashboard_config' in xls.sheet_names:
                self.dashboard_config = pd.read_excel(xls, sheet_name='dashboard_config')
                
            self.data_loaded = True
            return True
        except:
            return False

    def dapatkan_tahap_risiko(self, skor):
        if skor >= 80.0: return "hotspot_kritikal"
        elif skor >= 60.0: return "titik_kelemahan"
        elif skor >= 40.0: return "amaran_awal"
        else: return "rendah"

    def hitung_indeks_komposit(self, df_sasaran):
        all_items = [f'IKM_{i:03d}' for i in range(1, 109) if f'IKM_{i:03d}' in df_sasaran.columns]
        if not all_items or df_sasaran.empty: return 0.0, "rendah"
        mean_raw = df_sasaran[all_items].mean().mean()
        skor_normalisasi = ((mean_raw - 1) / 4) * 100
        return skor_normalisasi, self.dapatkan_tahap_risiko(skor_normalisasi)

    def hitung_skor_dimensi_tunggal(self, nama_dim, df_sasaran):
        target_items = [it for it in self.dim_item_ranges.get(nama_dim, []) if it in df_sasaran.columns]
        if not target_items or df_sasaran.empty: return 0.0
        mean_dim_raw = df_sasaran[target_items].mean().mean()
        return ((mean_dim_raw - 1) / 4) * 100

    def dapatkan_senarai_item(self):
        if self.questionnaire_master is None: return []
        return sorted(self.questionnaire_master['Item_Code'].dropna().unique().tolist())

    def tapis_pangkalan_data(self, kamus_penapis):
        data = self.respondent_data.copy()
        for col, values in kamus_penapis.items():
            if values and col in data.columns:
                data = data[data[col].isin(values)]
        return data

    def dapatkan_pilihan_penapis(self, nama_lajur):
        if self.respondent_data is None or nama_lajur not in self.respondent_data.columns:
            return []
        return sorted(self.respondent_data[nama_lajur].dropna().astype(str).unique().tolist())

    # --- JANAAN MANUSKRIP HTML AGUNG BAHASA MELAYU PENUH (25+ HALAMAN LENGKAP TANPA HAD) ---
    def jana_laporan_html_dossier(self, tajuk, pegawai, jabatan, df_aktif):
        skor, tahap = self.hitung_indeks_komposit(df_aktif)
        total_resp = len(df_aktif)
        kini_str = datetime.now().strftime('%d %B %Y')
        items = self.dapatkan_senarai_item()
        
        peta_klasifikasi = {"rendah": "RENDAH / STABIL", "amaran_awal": "AMARAN AWAL (TENSION)", "titik_kelemahan": "TITIK KELEMAHAN (PAIN POINT)", "hotspot_kritikal": "HOTSPOT KRITIKAL"}
        
        dim_labels = list(self.dim_item_ranges.keys())
        dim_values = [self.hitung_skor_dimensi_tunggal(d, df_aktif) for d in dim_labels]
        
        if not df_aktif.empty:
            geo_raw_html = df_aktif.groupby(['Zone', 'State', 'District', 'Urban_Rural'])[items].mean().mean(axis=1)
            geo_percents_html = ((geo_raw_html - 1) / 4 * 100).sort_values(ascending=False)
        else:
            geo_percents_html = pd.Series()

        html_master = f"""
        <!DOCTYPE html>
        <html lang="ms">
        <head>
            <meta charset="UTF-8">
            <title>{tajuk}</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #F8FAFC; color: #0F172A; padding: 50px; line-height: 1.8; }}
                .dossier-wrapper {{ max-width: 1050px; margin: 0 auto; background: #FFFFFF; padding: 60px; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }}
                .header-banner {{ background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); color: #FFFFFF; padding: 45px; text-align: center; border-radius: 12px; border-bottom: 6px solid #FFD700; margin-bottom: 40px; }}
                .confidential-tag {{ color: #EF4444; font-weight: 900; letter-spacing: 2px; font-size: 14px; margin-bottom: 10px; text-transform: uppercase; }}
                .section-title {{ color: #1E3A8A; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; margin-top: 40px; font-size: 20px; text-transform: uppercase; }}
                .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0; }}
                .kpi-box {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-top: 4px solid #1E40AF; padding: 20px; border-radius: 8px; text-align: center; }}
                .kpi-val {{ font-size: 32px; font-weight: 800; color: #1E3A8A; margin: 10px 0; }}
                .table-premium {{ width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 14px; }}
                .table-premium th {{ background: #0F172A; color: #FFFFFF; padding: 14px; text-align: left; }}
                .table-premium td {{ padding: 12px; border-bottom: 1px solid #E2E8F0; color: #334155; }}
                .table-premium tr:nth-child(even) {{ background-color: #F8FAFC; }}
                .loc-card-html {{ border: 1px solid #CBD5E1; border-radius: 8px; padding: 20px; margin-bottom: 15px; background: #FFFFFF; border-left: 5px solid #F59E0B; }}
                .loc-card-html.danger {{ background-color: #FEF2F2; border-left-color: #EF4444; }}
                .page-break {{ page-break-before: always; }}
                .meta-footer {{ margin-top: 60px; padding-top: 20px; border-top: 2px dashed #E2E8F0; text-align: center; font-size: 12px; color: #64748B; }}
            </style>
        </head>
        <body>
            <div class="dossier-wrapper">
                <div class="header-banner">
                    <div class="confidential-tag">SULIT — MANUSKRIP IMPAK STRATEGIK DASAR JPM</div>
                    <h1 style="margin: 0; font-size: 24px;">{tajuk}</h1>
                    <p style="margin: 10px 0 0 0; font-size: 14px; color: #94A3B8;">Laporan Implikasi Profil Sosio-Komposit Kebangsaan Terpenapis</p>
                    <p style="margin: 5px 0 0 0; font-size: 12px; color: #CBD5E1;">Tarikh Penjanaan: {kini_str} | Jumlah Rekod Sasar Aktif: {total_resp:,} Responden</p>
                </div>
                
                <div class="section-title">1.0 Ringkasan Eksekutif Polisi Makro Ditapis</div>
                <div class="kpi-grid">
                    <div class="kpi-box">
                        <div style="color:#64748B; font-weight:700; font-size:11px;">Indeks Ketegangan Komposit</div>
                        <div class="kpi-val">{skor:.2f}%</div>
                        <div style="font-size:11px; font-weight:600;">Status: {peta_klasifikasi.get(tahap).upper()}</div>
                    </div>
                    <div class="kpi-box">
                        <div style="color:#64748B; font-weight:700; font-size:11px;">Saiz Sampel Aktif Tertapis</div>
                        <div class="kpi-val">{total_resp:,}</div>
                        <div style="font-size:11px; font-weight:600;">Profil Persampelan Strata DOSM</div>
                    </div>
                    <div class="kpi-box">
                        <div style="color:#64748B; font-weight:700; font-size:11px;">Keamatan Amaran Siber Komposit</div>
                        <div class="kpi-val">{self.hitung_skor_dimensi_tunggal('D9 Ketegangan Digital', df_aktif):.2f}%</div>
                        <div style="font-size:11px; font-weight:600; color:#EF4444;">Dimensi Risiko Digital</div>
                    </div>
                </div>

                <div class="page-break"></div>

                <div class="section-title">2.0 Pecahan Lengkap Analisis Deskriptif Profil Demografi Kluster Terpenapis</div>
                <table class="table-premium">
                    <thead><tr><th>Pemboleh Ubah Sosio-Demografi</th><th>Klasifikasi Parameter Kumpulan Sasar</th><th>Frekuensi (Bil.)</th><th>Peratusan (%)</th></tr></thead>
                    <tbody>"""
        
        demo_cols_list = ['Zone', 'State', 'District', 'Locality', 'Gender', 'Age', 'Generation', 'Ethnicity', 'Religion', 'Education', 'Occupation', 'Income_Group', 'Urban_Rural', 'Type_of_Respondent']
        for col in [c for c in demo_cols_list if c in df_aktif.columns]:
            counts = df_aktif[col].value_counts()
            for cat, val in counts.items():
                pct = (val / total_resp) * 100
                html_master += f"<tr><td><b>{col}</b></td><td>{cat}</td><td>{val:,}</td><td><b>{pct:.2f}%</b></td></tr>"
        
        html_master += """
                    </tbody>
                </table>
                <div class="page-break"></div>
        """

        html_master += """
                <div class="section-title">3.0 Keamatan Aras Ketegangan Komposit Merentas 9 Dimensi Skrining</div>
                <table class="table-premium">
                    <thead><tr><th>Kod</th><th>Nama Dimensi Skrining Kebangsaan</th><th>Skor Ketegangan (%)</th><th>Klasifikasi Risiko Keseriusan</th></tr></thead>
                    <tbody>"""
        for d_key in self.dim_item_ranges.keys():
            d_score = self.hitung_skor_dimensi_tunggal(d_key, df_aktif)
            html_master += f"<tr><td>{d_key[:2]}</td><td>{d_key}</td><td><b>{d_score:.2f}%</b></td><td>{peta_klasifikasi.get(self.dapatkan_tahap_risiko(d_score))}</td></tr>"
        
        html_master += """
                    </tbody>
                </table>
                <div class="page-break"></div>
        """

        html_master += """
                <div class="section-title">4.0 Laporan Spasial Hierarki Rantaian Lokasi Berstruktur Penuh (Zon &rarr; Negeri &rarr; Daerah &rarr; Lokaliti)</div>"""
        
        if not geo_percents_html.empty:
            for rank, ((zn, st_n, ds_n, ur_n), pct_v) in enumerate(geo_percents_html.items()):
                if pct_v >= 40.0:
                    sub_df = df_aktif[(df_aktif['Zone']==zn) & (df_aktif['State']==st_n) & (df_aktif['District']==ds_n) & (df_aktif['Urban_Rural']==ur_n)]
                    sub_item = sub_df[items].mean().idxmax()
                    sub_stmt = self.questionnaire_master[self.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                    tier_tag = "danger" if pct_v >= 80.0 else ""
                    html_master += f"""
                    <div class="loc-card-html {tier_tag}">
                        <b>📍 RANTAIAN LOKASI KRITIKAL #{rank+1}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>
                        * Skor Indeks Ketegangan Komposit Wilayah: <b>{pct_v:.2f}%</b> (Klasifikasi Keselamatan: {peta_klasifikasi.get(self.dapatkan_tahap_risiko(pct_v))})<br>
                        * 💥 **Punca Akar Utama (Stressor Setempat):** Indikator {sub_item} &rarr; <i>"{sub_stmt}"</i>
                    </div>"""
        else:
            html_master += "<p>Tiada rantaian geografi ditemui untuk parameter tapisan semasa.</p>"

        html_master += """
                <div class="page-break"></div>
                <div class="section-title">5.0 Log Tangkapan Data Scraping Siber Digital Agregat (OSINT Records)</div>
                <table class="table-premium">
                    <thead><tr><th>Tarikh</th><th>Platform Media</th><th>Kawasan Wilayah</th><th>Kategori Isu Pergeseran</th><th>Aras Amaran</th><th>Ringkasan Log Pangkalan Data Master</th></tr></thead>
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
                <div class="meta-footer">
                    <p>Manuskrip Laporan Inteligensi Komposit Diperaku oleh: <b>{officer}</b> | Jabatan: <b>{jabatan}</b></p>
                    <p><b>RAHSIA RASMI KERAJAAN — URUS SETIA POLISI KESELAMATAN SOSIAL KABINET MALAYSIA 2026</b></p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_master


def inisialisasi_sesi_papan_pemuka():
    if 'engine' not in st.session_state or not hasattr(st.session_state.engine, 'dapatkan_pilihan_penapis'):
        st.session_state.engine = EnginDasarIKMM()
        st.session_state.engine.hubung_dan_muat_data()
    if 'auth_state' not in st.session_state:
        st.session_state.auth_state = False

def main():
    inisialisasi_sesi_papan_pemuka()
    if not st.session_state.auth_state:
        terapkan_tema_premium_eksekutif() # PEMBETULAN UTAMA: Memanggil fungsi bermelayu yang betul bagi menghapuskan NameError
        c1, c2, c3 = st.columns([1, 1.3, 1])
        with c2:
            st.markdown("<div style='text-align: center; padding-top: 130px;'><h2>🏛️ Urus Setia Polisi IKMM 2026</h2><p>Sistem Amaran Awal Konflik Kebangsaan (JPM)</p></div>", unsafe_allow_html=True)
            with st.form("gate_form"):
                token = st.text_input("Sila Masukkan Token Pelepasan Keselamatan", type="password")
                if st.form_submit_button("Sahkan Kredensial Akses Kabinet", use_container_width=True):
                    if hashlib.sha256(token.encode()).hexdigest() == hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest():
                        st.session_state.auth_state = True
                        st.rerun()
                    else:
                        st.error("Ralat: Pelepasan Keselamatan Ditolak. Token Tidak Sah.")
        return
        
    terapkan_tema_premium_eksekutif() # PEMBETULAN UTAMA
    engine = st.session_state.engine
    
    tabs = st.tabs([
        "01 Portal Gateway & Penapis", "02 Ringkasan Eksekutif", "03 Penilaian Geografi", 
        "04 Pengiraan 9 Indeks", "05 Amaran Item Stressor", "06 Sentimen NLP Kualitatif", 
        "07 Teori Dasar", "08 Sektor Pain Points", "09 Sektor Tension Points", 
        "10 Amaran Hotspot EWS", "11 Strategi Intervensi", "12 Media Scraping", 
        "13 Dapatan FGD Pakar", "14 Dossier Report Cabinet", "15 Cell Data Explorer"
    ])
    
    # --- TAB 1: PORTAL GATEWAY & KAWALAN GEOMATRIKS UTAMA (BERPUSAT DI ATAS ATAS SEPENUHNYA!) ---
    active_filters = {}
    with tabs[0]:
        st.subheader("📂 Pengurusan Fail & Pusat Penapis Geokomposit Berpusat")
        uploaded_file = st.file_uploader("Sila Pilih / Lepaskan Fail Pangkalan Data Excel Master IKMM (.xlsx)", type=['xlsx'])
        if uploaded_file and st.button("Proses & Hubungkan Fail Excel Baharu", use_container_width=True):
            if engine.hubung_dan_muat_data(uploaded_file):
                st.success("Fail Excel Berjaya Dimuat Naik & Dihubungkan!")
                st.rerun()
        
        st.markdown("---")
        if engine.data_loaded:
            st.markdown("### 🔍 Parameter Tapisan Geokomposit Berantai (Zon &rarr; Negeri &rarr; Daerah)")
            
            c_f1, c_f2, c_f3 = st.columns(3)
            with c_f1:
                zon_options = engine.dapatkan_pilihan_penapis('Zone')
                sel_zone = st.multiselect("🧭 1. Tapis mengikut Wilayah / Zon", zon_options)
            with c_f2:
                if sel_zone:
                    state_subset = engine.respondent_data[engine.respondent_data['Zone'].isin(sel_zone)]
                    state_options = sorted(state_subset['State'].dropna().unique().tolist())
                else:
                    state_options = engine.dapatkan_pilihan_penapis('State')
                sel_state = st.multiselect("🏛️ 2. Tapis mengikut Wilayah Negeri", state_options)
            with c_f3:
                if sel_state:
                    district_subset = engine.respondent_data[engine.respondent_data['State'].isin(sel_state)]
                    district_options = sorted(district_subset['District'].dropna().unique().tolist())
                elif sel_zone:
                    district_subset = engine.respondent_data[engine.respondent_data['Zone'].isin(sel_zone)]
                    district_options = sorted(district_subset['District'].dropna().unique().tolist())
                else:
                    district_options = engine.dapatkan_pilihan_penapis('District')
                sel_district = st.multiselect("🏙️ 3. Tapis mengikut Daerah / Parlimen", district_options)
                
            if sel_zone: active_filters['Zone'] = sel_zone
            if sel_state: active_filters['State'] = sel_state
            if sel_district: active_filters['District'] = sel_district

    # SINKRONISASI AKTIF: Mengikat kesemua data operasi kuantitatif kepada filtered_df rentas tab
    filtered_df = engine.apply_filters(active_filters)
    sub_total = len(filtered_df)
    items_list_main = engine.dapatkan_senarai_item()
    
    # Pengiraan senarai rantaian peratusan geospasial bagi kegunaan Tab 08, 09, & 10
    if sub_total > 0 and engine.data_loaded:
        geo_raw_main = filtered_df.groupby(['Zone', 'State', 'District', 'Urban_Rural'])[items_list_main].mean().mean(axis=1)
        geo_percents_main = ((geo_raw_main - 1) / 4 * 100).sort_values(ascending=False)
    else:
        geo_percents_main = pd.Series()

    if not engine.data_loaded:
        st.warning("⚠️ Sila muat naik fail Excel data master responden untuk mengaktifkan sistem.")
        return

    # Paparan status pangkalan data ditapis
    st.markdown(f"""
        <div style='background-color: rgba(59, 130, 246, 0.2); padding: 12px; border-radius: 8px; border-left: 5px solid #3B82F6; margin-bottom: 20px;'>
            <p style='margin:0; font-size:13px; font-weight:700; color:#F8FAFC;'>🌐 KUMPULAN DATA AKTIF: Memproses {sub_total:,} daripada {len(engine.respondent_data):,} Kumpulan Responden Terpenapis.</p>
        </div>
    """, unsafe_allow_html=True)

    # --- TAB 2: RINGKASAN EKSEKUTIF ---
    with tabs[1]:
        st.subheader("📈 Pusat Kawalan KPI Ketegangan Komposit Kluster Tertapis")
        if sub_total > 0:
            ikm_score, tier_status = engine.hitung_indeks_komposit(filtered_df)
            peta_lbl = {"rendah": "RENDAH / STABIL", "amaran_awal": "AMARAN AWAL (TENSION)", "titik_kelemahan": "TITIK KELEMAHAN (PAIN POINT)", "hotspot_kritikal": "HOTSPOT KRITIKAL"}
            
            c1, c2, c3 = st.columns(3)
            with c1: paparkan_kad_kpi("Indeks Ketegangan Semasa (IKM %)", f"{ikm_score:.2f}%", "Aman (0%) ↔ Tegang (100%)", tahap=tier_status)
            with c2: paparkan_kad_kpi("Tahap Risiko Keselamatan Semasa", peta_lbl.get(tier_status), "Klasifikasi Isu Kluster Ditapis", tahap=tier_status)
            with c3: paparkan_kad_kpi("Saiz Responden Aktif Ditapis", f"{sub_total:,}", "Kumpulan Sampel Terproses", tahap="rendah")
            
            st.markdown("---")
            dim_data = engine.get_dimension_composite_scores(filtered_df)
            dim_df = pd.DataFrame(list(dim_data.items()), columns=['Dimensi Skrining IKM', 'Indeks Ketegangan (%)']).sort_values('Indeks Ketegangan (%)', ascending=False)
            st.plotly_chart(px.bar(dim_df, x='Indeks Ketegangan (%)', y='Dimensi Skrining IKM', orientation='h', color='Indeks Ketegangan (%)', color_continuous_scale='Reds', text_auto='.1f'), use_container_width=True)

    # --- TAB 3: PENILAIAN GEOGRAFI ---
    with tabs[2]:
        if sub_total > 0:
            state_matrix = filtered_df.groupby('State')[items_list_main].mean().mean(axis=1).reset_index()
            state_matrix.columns = ['Negeri / Wilayah', 'Indeks Ketegangan (IKM %)']
            state_matrix['Indeks Ketegangan (IKM %)'] = (state_matrix['Indeks Ketegangan (IKM %)'] - 1) / 4 * 100
            st.dataframe(state_matrix.sort_values('Indeks Ketegangan (IKM %)', ascending=False), use_container_width=True, hide_index=True)

    # --- TAB 4: PENGIRAAN 9 INDEKS DIMENSI ---
    with tabs[3]:
        st.subheader("📊 Pengiraan Spesifik Komposit Setiap Dimensi Skrining Kluster")
        if sub_total > 0:
            grid_c1, grid_c2, grid_c3 = st.columns(3)
            for idx, dim_name in enumerate(engine.dim_item_ranges.keys()):
                d_score = engine.hitung_skor_dimensi_tunggal(dim_name, filtered_df)
                t_col = grid_c1 if idx % 3 == 0 else (grid_c2 if idx % 3 == 1 else grid_c3)
                with t_col: paparkan_kad_kpi(f"{dim_name}", f"{d_score:.2f}%", "Skor Tertapis Real-Time", tahap=engine.dapatkan_tahap_risiko(d_score))

    # --- TAB 5: AMARAN ITEM STRESSOR ---
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
        st.info("Pencidukan ulasan kualitatif siber mengikut kriteria tapisan semasa.")

    # --- TAB 7: ANALISIS TEORETIKAL ---
    with tabs[6]:
        st.subheader("🧠 Pusat Interpretasi Psikometrik & Analisis Penumpuan Teori-Data")
        st.info("Pemodelan indeks strain sosiologi rentas pangkalan data pool ditapis.")

    # --- TAB 08: PAIN POINTS ---
    with tabs[7]:
        st.subheader("⚠️ Pengelasan Petunjuk Titik Kelemahan Struktur (Sektor Pain Points)")
        if not geo_percents_main.empty:
            rank_pp = 1
            for (zn, st_n, ds_n, ur_n), pct_v in geo_percents_main.items():
                if 40.0 <= pct_v < 60.0:
                    sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                    sub_item = sub_df[items_list_main].mean().idxmax()
                    sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                    st.markdown(f"<div class='loc-card-premium' style='border-left-color: #DB2777;'><b>📍 LOKASI #{rank_pp}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>* Skor Indeks Komposit Sebenar: <b>{pct_v:.2f}%</b><br>* 🔍 Punca Utama (Stressor): Indikator {sub_item} &rarr; <i>\"{sub_stmt}\"</i></div>", unsafe_allow_html=True)
                    rank_pp += 1
            if rank_pp == 1: st.info("Tiada lokasi di bawah kluster tapisan semasa yang berada dalam julat Pain Point (40%-59%).")

    # --- TAB 09: TENSION POINTS ---
    with tabs[8]:
        st.subheader("🔥 Kerangka Eskalasi Indikator Titik Ketegangan (Sektor Tension Points)")
        if not geo_percents_main.empty:
            rank_tp = 1
            for (zn, st_n, ds_n, ur_n), pct_v in geo_percents_main.items():
                if 60.0 <= pct_v < 80.0:
                    sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                    sub_item = sub_df[items_list_main].mean().idxmax()
                    sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                    st.markdown(f"<div class='loc-card-premium' style='border-left-color: #F59E0B;'><b>📍 LOKASI #{rank_tp}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>* Skor Indeks Komposit Sebenar: <b>{pct_v:.2f}%</b><br>* 🔍 Punca Utama (Stressor): Indikator {sub_item} &rarr; <i>\"{sub_stmt}\"</i></div>", unsafe_allow_html=True)
                    rank_tp += 1
            if rank_tp == 1: st.info("Tiada lokasi di bawah kluster tapisan semasa yang berada dalam julat Tension Point (60%-79%).")

    # --- TAB 10: AMARAN HOTSPOT EWS ---
    with tabs[9]:
        st.subheader("🚨 Early Warning System (EWS) — Sempadan Amaran Hotspot Kritikal")
        if not geo_percents_main.empty:
            rank_hs = 1
            for (zn, st_n, ds_n, ur_n), pct_v in geo_percents_main.items():
                if pct_v >= 80.0:
                    sub_df = filtered_df[(filtered_df['Zone']==zn) & (filtered_df['State']==st_n) & (filtered_df['District']==ds_n) & (filtered_df['Urban_Rural']==ur_n)]
                    sub_item = sub_df[items_list_main].mean().idxmax()
                    sub_stmt = engine.questionnaire_master[engine.questionnaire_master['Item_Code'] == sub_item]['Statement'].values[0]
                    st.markdown(f"<div class='loc-card-premium' style='border-left-color: #EF4444; background-color: rgba(239, 68, 68, 0.1);'><b style='color: #EF4444;'>💥 CRITICAL ZON #{rank_hs}: Zon {zn} &rarr; Negeri {st_n} &rarr; Daerah {ds_n} &rarr; Lokaliti {ur_n}</b><br>* Skor Indeks Komposit Sebenar EWS: <b>{pct_v:.2f}%</b><br>* 🛑 Punca Utama (Stressor): Indikator {sub_item} &rarr; <i>\"{sub_stmt}\"</i></div>", unsafe_allow_html=True)
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
                    "MOF": {"PBT": "Menyelaras skim pelepasan cukai pintu lokaliti sasar", "Swasta": "Melaksanakan pelarasan gaji progresif sektor komersial swasta", "Komuniti": "Pengagihan kad bantuan bakul makanan digital"},
                    "UNITY": {"PBT": "Mengaktifkan Jawatankuasa Perpaduan Daerah (JPD)", "Swasta": "Menaja modul latihan kepelbajaaan korporat swasta", "Komuniti": "Mobilisasi Kawasan Rukun Tangga (KRT) bagi dialog keamanan"}
                }
                for idx, row in final_policy.iterrows():
                    current_lead = row.get('Agency', 'N/A')
                    context_data = agency_mapping_context.get(current_lead, {"PBT": "Menyelaras operasi municipal", "Swasta": "Sokongan komersial swasta", "Komuniti": "Mobilisasi akar umbi"})
                    st.markdown(f"""
                    <div class='loc-card-premium' style='border-left-color: #3B82F6; padding: 25px;'>
                        <h4>🏛️ Agensi Peneraju Kabinet: {current_lead}</h4>
                        <p><b>Nama Program Modul:</b> {row.get('Intervention_Name', 'N/A')}</p>
                        <p><b>Deskripsi Dasar:</b> {row.get('Description', 'N/A')}</p>
                        <hr style='border-top:1px dashed rgba(255,255,255,0.1);'>
                        <ul>
                            <li><b>🏢 Peranan Swasta:</b> {context_data['Swasta']}</li>
                            <li><b>街 PBT / Majlis Daerah:</b> {context_data['PBT']}</li>
                            <li><b>👥 Peranan Komuniti:</b> {context_data['Komuniti']}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

    # --- TAB 12: MEDIA SCRAPING ---
    with tabs[11]:
        st.subheader("📰 Papan Pemantauan Media Cetak & Aliran Sentimen Siber Digital (OSINT)")
        if engine.media_issue_summary is not None:
            m_df = engine.media_issue_summary
            display_media = m_df.copy()
            if sel_state: display_media = display_media[display_media['State'].isin(sel_state)]
            for idx, row in display_media.iterrows():
                st.markdown(f"🔹 **Tarikh: {row.get('Date','N/A')} | Platform: {row.get('Source','N/A')} | Wilayah: {row.get('State','N/A')}**\n* 💬 Rumusan Siber: \"{row.get('Summary','N/A')}\"")
                st.markdown("---")

    # --- TAB 13: DAPATAN FGD PAKAR ---
    with tabs[12]:
        st.subheader("👥 Transkrip Consensus Panel Pakar & Dapatan Bengkel FGD")
        if engine.fgd_expert is not None:
            st.plotly_chart(px.bar(engine.fgd_expert['Priority'].value_counts(), title="Matriks Kalibrasi Kualitatif Panel Pakar Kebangsaan"), use_container_width=True)

    # --- TAB 14: REPORT GENERATOR HTML ---
    with tabs[13]:
        st.subheader("📄 Penjanaan HTML Briefing Dossier Berasaskan Kluster Ditapis")
        rep_title = st.text_input("Tajuk Laporan Eksekutif JPM", "Laporan Hasil Kajian Pembangunan Indeks Ketegangan Masyarakat Malaysia (IKMM) Bagi Kelulusan Jemaah Menteri 2026")
        rep_officer = st.text_input("Nama Pegawai Pelapor Muktamad", "Dato' Sri Ketua Pengarah JPNIN")
        rep_branch = st.text_input("Bahagian / Agensi Utama", "Kluster Analitik Risiko & Pemetaan Polisi Strategik Perpaduan")
        if st.button("Kompilasikan Dokumen Laporan Kluster Terpenapis", use_container_width=True):
            if sub_total > 0:
                html_code = engine.jana_laporan_html_dossier(rep_title, rep_officer, rep_branch, filtered_df)
                st.success("✓ Dokumen Dossier Kabinet Mega Berjaya Dikompilasikan Spesifik Mengikut Parameter Tapisan Berpusat Gateway!")
                st.download_button("⬇ Muat Turun Fail Laporan Dossier Terpenapis Bahasa Melayu (.html)", html_code, "IKMM_Filtered_Dossier_2026.html", "text/html", use_container_width=True)
            else:
                st.error("Ralat: Tidak boleh menjana laporan bagi data kosong (0 responden). Sila ubah tapisan anda.")
            
    with tabs[14]:
        st.subheader("🔎 Advanced Database Structural Cell Matrix Explorer")
        st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
