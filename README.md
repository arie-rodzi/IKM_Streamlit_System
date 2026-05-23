
# Sistem Pintar IKM Nasional — Premium V2

Versi ini membetulkan isu:
- tulisan sidebar tidak nampak
- peratus demografi salah
- calculation hardcoded
- tiada model pengiraan jelas
- tiada perbandingan negeri/daerah
- reka bentuk terlalu kosong

## Struktur Modular
- app.py
- utils/style.py
- utils/data_loader.py
- utils/model_engine.py
- utils/charts.py
- modules/executive.py
- modules/model_page.py
- modules/demografi.py
- modules/comparison.py
- modules/intervensi.py
- modules/indicators.py
- modules/social_media.py
- modules/warning_timeline.py

## Cara Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Nota Model
IKM Survey = Σ(berat indikator × skor indikator)

IKM Komposit Daerah = 0.60(IKM Survey) + 0.30(Risiko Digital) + 0.10(Kadar Hate Speech)


## Premium V3 Update
Tambah analisis demografi terperinci:
- Kaum / etnik
- Kumpulan pendapatan
- Tahap pendidikan
- Pecahan risiko dalam setiap kumpulan
- Profil indikator mengikut kumpulan
- Matriks gabungan demografi seperti etnik × pendapatan dan etnik × pendidikan
