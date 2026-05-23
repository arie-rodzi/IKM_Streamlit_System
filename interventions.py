
import pandas as pd

def classify_alert(score, toxic=0, hate=0):
    if score >= 75 or toxic >= 70 or hate >= 12:
        return "Merah", "Tindakan segera dalam 72 jam"
    if score >= 60 or toxic >= 55 or hate >= 8:
        return "Jingga", "Intervensi keutamaan dalam 30 hari"
    if score >= 45:
        return "Kuning", "Pantauan rapi dan engagement berkala"
    return "Hijau", "Kekalkan program komuniti berkala"

def recommend(row):
    drivers = {
        "Ekonomi": row.get("purata_ekonomi", 0),
        "Politik": row.get("purata_politik", 0),
        "Sosial": row.get("purata_sosial", 0),
        "Digital/Media": row.get("purata_digital", 0),
        "Toksisiti Media Sosial": row.get("purata_toksik", 0),
        "Risiko Digital": row.get("purata_risiko_digital", 0),
        "Hate Speech": row.get("kadar_hate_speech", 0) * 100 if pd.notna(row.get("kadar_hate_speech", None)) else 0,
    }
    top = sorted(drivers.items(), key=lambda x: x[1], reverse=True)[:3]
    score = row.get("IKM_komposit", 0)
    toxic = row.get("purata_toksik", 0)
    hate = row.get("kadar_hate_speech", 0) * 100 if pd.notna(row.get("kadar_hate_speech", None)) else 0
    alert, sla = classify_alert(score, toxic, hate)
    actions = []
    for driver, val in top:
        if driver in ["Digital/Media", "Toksisiti Media Sosial", "Risiko Digital", "Hate Speech"]:
            actions.append(("Digital Response Cell", "Pemantauan media sosial harian, counter-narrative, fact-checking, pengesanan influencer/akaun pemacu isu dan laporan sentimen mingguan."))
        elif driver == "Ekonomi":
            actions.append(("Dialog Ekonomi Komuniti", "Libat urus isu kos sara hidup, bantuan bersasar, komunikasi dasar setempat dan pemetaan kumpulan rentan."))
        elif driver == "Politik":
            actions.append(("Mediation & Depolarisation", "Dialog rentas komuniti, neutral briefing, kawalan naratif sensitif dan pengesanan isu politik berulang."))
        elif driver == "Sosial":
            actions.append(("Program Kohesi Sosial", "Aktiviti komuniti bersama, mediator akar umbi, program silang komuniti dan engagement belia."))
        else:
            actions.append(("Keselamatan Komuniti", "Koordinasi agensi, saluran aduan pantas, rondaan komuniti dan pencegahan insiden setempat."))
    # dedupe by title
    seen=[]; clean=[]
    for t,d in actions:
        if t not in seen:
            clean.append((t,d)); seen.append(t)
    return alert, sla, top, clean[:4]

def build_intervention_table(district):
    rows=[]
    for _, r in district.iterrows():
        alert, sla, top, actions = recommend(r)
        rows.append({
            "negeri": r.get("negeri"),
            "daerah": r.get("daerah"),
            "IKM_komposit": r.get("IKM_komposit"),
            "amaran": alert,
            "SLA_tindakan": sla,
            "pencetus_utama": ", ".join([x[0] for x in top]),
            "intervensi_utama": actions[0][0] if actions else "Pemantauan berkala"
        })
    return pd.DataFrame(rows).sort_values("IKM_komposit", ascending=False)
