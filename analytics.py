
import numpy as np
import pandas as pd

INDICATOR_COLS = [
    "skor_ekonomi", "skor_politik", "skor_sosial", "skor_digital", 
    "skor_keselamatan", "skor_defisit_kepercayaan", "skor_risiko_perpaduan"
]

INDICATOR_LABELS = {
    "skor_ekonomi": "Ekonomi",
    "skor_politik": "Politik",
    "skor_sosial": "Sosial",
    "skor_digital": "Digital/Media",
    "skor_keselamatan": "Keselamatan",
    "skor_defisit_kepercayaan": "Defisit Kepercayaan",
    "skor_risiko_perpaduan": "Risiko Perpaduan",
}

def risk_label(score):
    if pd.isna(score): return "-"
    if score < 40: return "Rendah"
    if score < 60: return "Sederhana"
    if score < 75: return "Tinggi"
    return "Kritikal"

def national_kpis(resp, social, district):
    avg_ikm = district["IKM_komposit"].mean() if len(district) else 0
    top_state = district.groupby("negeri")["IKM_komposit"].mean().sort_values(ascending=False).index[0] if len(district) else "-"
    return {
        "avg_ikm": avg_ikm,
        "risk": risk_label(avg_ikm),
        "respondents": len(resp),
        "posts": len(social),
        "districts": district["daerah"].nunique() if len(district) else 0,
        "hotspots": int((district["IKM_komposit"] >= 60).sum()) if len(district) else 0,
        "top_state": top_state,
        "hate_rate": float((social["hate_speech_flag"] == "Ya").mean()*100) if len(social) else 0,
    }

def demographic_summary(resp):
    demos = {}
    for col in ["jantina", "kumpulan_umur", "etnik", "pendidikan", "pendapatan", "lokasi"]:
        if col in resp.columns and len(resp):
            tmp = resp.groupby(col, observed=False).agg(
                bilangan=("respondent_id", "count"),
                purata_IKM=("skor_IKM", "mean")
            ).reset_index().sort_values("purata_IKM", ascending=False)
            tmp["purata_IKM"] = tmp["purata_IKM"].round(2)
            demos[col] = tmp
    return demos

def state_comparison(district):
    if len(district)==0:
        return pd.DataFrame()
    out = district.groupby("negeri", as_index=False).agg(
        bil_daerah=("daerah", "nunique"),
        bil_responden=("bil_responden", "sum"),
        bil_post=("bil_post", "sum"),
        purata_IKM=("IKM_komposit", "mean"),
        max_IKM=("IKM_komposit", "max"),
        hotspot=("IKM_komposit", lambda x: int((x>=60).sum()))
    )
    out["purata_IKM"] = out["purata_IKM"].round(2)
    out["max_IKM"] = out["max_IKM"].round(2)
    out["tahap_risiko"] = out["purata_IKM"].apply(risk_label)
    return out.sort_values("purata_IKM", ascending=False)

def indicator_summary(resp):
    cols = [c for c in INDICATOR_COLS if c in resp.columns]
    if len(resp)==0 or not cols: return pd.DataFrame()
    out = resp[cols].mean().reset_index()
    out.columns = ["indikator", "purata"]
    out["indikator"] = out["indikator"].map(INDICATOR_LABELS)
    out["purata"] = out["purata"].round(2)
    return out.sort_values("purata", ascending=False)

def district_rank(district, top=30):
    if len(district)==0: return district
    cols = ["negeri","daerah","bil_responden","bil_post","IKM_komposit","tahap_risiko","hotspot_keutamaan","purata_toksik","kadar_hate_speech"]
    cols = [c for c in cols if c in district.columns]
    return district.sort_values("IKM_komposit", ascending=False)[cols].head(top)

def monthly_trends(resp, social):
    trend1 = pd.DataFrame()
    if len(resp):
        trend1 = resp.copy()
        trend1["bulan"] = pd.to_datetime(trend1["tarikh_kutipan"]).dt.to_period("M").astype(str)
        trend1 = trend1.groupby("bulan", as_index=False)["skor_IKM"].mean().rename(columns={"skor_IKM":"Survey IKM"})
    trend2 = pd.DataFrame()
    if len(social):
        trend2 = social.copy()
        trend2["bulan"] = pd.to_datetime(trend2["tarikh"]).dt.to_period("M").astype(str)
        trend2 = trend2.groupby("bulan", as_index=False)["risk_signal"].mean().rename(columns={"risk_signal":"Risiko Digital"})
    if len(trend1) and len(trend2):
        return trend1.merge(trend2, on="bulan", how="outer").sort_values("bulan")
    return trend1 if len(trend1) else trend2
