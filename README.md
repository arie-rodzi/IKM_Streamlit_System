# Sistem Pintar IKM Nasional — Premium Modular Version

Versi ini dipecahkan kepada beberapa fail `.py` untuk presentation yang lebih kemas dan mudah dikembangkan.

## Fail Utama
- `app.py` — aplikasi utama
- `styles.py` — tema premium, CSS, warna, KPI card
- `data_loader.py` — upload/load Excel dan filter data
- `analytics.py` — pengiraan KPI, demografi, indikator, trend
- `visualizations.py` — semua chart Plotly
- `interventions.py` — logic amaran awal dan cadangan intervensi
- `pages.py` — paparan dashboard mengikut modul
- `IKM_Simulation_Data_Malaysia.xlsx` — data simulasi

## Cara Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Modul Dashboard
1. Executive dashboard
2. Analisis demografi
3. Perbandingan lokasi dan intervensi
4. Analisis indikator dan korelasi
5. Analisis media sosial / big data
6. Amaran awal
7. Milestone 18 bulan

## Nota
Data dalam fail Excel ialah data sintetik/simulasi sahaja untuk tujuan prototype.
