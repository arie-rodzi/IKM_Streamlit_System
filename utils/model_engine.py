
import numpy as np
import pandas as pd

DOMAIN_MAP = {
    "Ekonomi": "skor_ekonomi",
    "Politik": "skor_politik",
    "Sosial": "skor_sosial",
    "Digital/Media": "skor_digital",
    "Keselamatan": "skor_keselamatan",
    "Defisit Kepercayaan": "skor_defisit_kepercayaan",
    "Risiko Perpaduan": "skor_risiko_perpaduan",
}

def risk_label(score):
    if pd.isna(score):
        return "-"
    if score < 40:
        return "Rendah"
    if score < 60:
        return "Sederhana"
    if score < 75:
        return "Tinggi"
    return "Kritikal"

def risk_color(label):
    return {
        "Rendah": "#0F9D58",
        "Sederhana": "#D6A437",
        "Tinggi": "#F29900",
        "Kritikal": "#D93025",
        "-": "#6B7C8F"
    }.get(label, "#0B2E59")

def normalise_weights(weights_df):
    w = weights_df.copy()
    if "berat_simulasi" not in w.columns:
        raise ValueError("Sheet parameter_weighting mesti ada kolum berat_simulasi.")
    total = float(w["berat_simulasi"].sum())
    if total == 0:
        w["berat_normal"] = 0
    else:
        w["berat_normal"] = w["berat_simulasi"] / total
    return w

def calculate_survey_ikm(df, weights_df):
    weights = normalise_weights(weights_df)
    out = df.copy()
    score = np.zeros(len(out), dtype=float)
    contribution_cols = []
    for _, row in weights.iterrows():
        domain = row["domain"]
        col = DOMAIN_MAP.get(domain)
        if col in out.columns:
            contrib_col = f"contrib_{domain}"
            out[contrib_col] = out[col].fillna(0) * float(row["berat_normal"])
            contribution_cols.append(contrib_col)
            score += out[contrib_col].values
    out["IKM_survey_model"] = np.round(score, 2)
    out["tahap_risiko_model"] = out["IKM_survey_model"].apply(risk_label)
    return out, contribution_cols, weights

def build_district_model(respondent, social, weights_df):
    resp_model, _, weights = calculate_survey_ikm(respondent, weights_df)

    survey_summary = resp_model.groupby(["negeri", "daerah"], as_index=False).agg(
        bil_responden=("respondent_id", "count"),
        IKM_survey=("IKM_survey_model", "mean"),
        ekonomi=("skor_ekonomi", "mean"),
        politik=("skor_politik", "mean"),
        sosial=("skor_sosial", "mean"),
        digital=("skor_digital", "mean"),
        keselamatan=("skor_keselamatan", "mean"),
        defisit_kepercayaan=("skor_defisit_kepercayaan", "mean"),
        risiko_perpaduan=("skor_risiko_perpaduan", "mean")
    )

    if len(social) > 0:
        social_summary = social.groupby(["negeri", "daerah"], as_index=False).agg(
            bil_post=("post_id", "count"),
            risiko_digital=("risk_signal", "mean"),
            sentimen=("sentiment_score", "mean"),
            toksik=("toxicity_score", "mean"),
            kadar_hate_speech=("hate_speech_flag", lambda x: (x.astype(str).str.lower() == "ya").mean() * 100)
        )
    else:
        social_summary = pd.DataFrame(columns=["negeri","daerah","bil_post","risiko_digital","sentimen","toksik","kadar_hate_speech"])

    model = survey_summary.merge(social_summary, on=["negeri","daerah"], how="left")
    model["bil_post"] = model["bil_post"].fillna(0)
    model["risiko_digital"] = model["risiko_digital"].fillna(model["digital"])
    model["sentimen"] = model["sentimen"].fillna(50)
    model["toksik"] = model["toksik"].fillna(0)
    model["kadar_hate_speech"] = model["kadar_hate_speech"].fillna(0)

    # Correct clear model formula
    model["IKM_komposit_model"] = (
        0.60 * model["IKM_survey"] +
        0.30 * model["risiko_digital"] +
        0.10 * model["kadar_hate_speech"]
    ).round(2)
    model["tahap_risiko_model"] = model["IKM_komposit_model"].apply(risk_label)
    model["keutamaan_intervensi"] = np.select(
        [
            model["IKM_komposit_model"] >= 75,
            model["IKM_komposit_model"] >= 60,
            model["IKM_komposit_model"] >= 45
        ],
        ["Segera", "Keutamaan", "Pantau"],
        default="Normal"
    )

    for c in model.select_dtypes(include="number").columns:
        model[c] = model[c].round(2)
    return model, resp_model, weights

def percentage_table(df, col):
    if col not in df.columns or len(df) == 0:
        return pd.DataFrame(columns=[col, "bilangan", "peratus"])
    tab = df[col].fillna("Tidak diketahui").astype(str).value_counts(dropna=False).reset_index()
    tab.columns = [col, "bilangan"]
    total = tab["bilangan"].sum()
    tab["peratus"] = (tab["bilangan"] / total * 100).round(2) if total else 0
    return tab

def demographic_cross(df, demo_col, value_col="IKM_survey_model"):
    if len(df) == 0 or demo_col not in df.columns:
        return pd.DataFrame()
    out = df.groupby(demo_col, as_index=False).agg(
        bilangan=("respondent_id", "count"),
        purata_ikm=(value_col, "mean")
    )
    out["peratus"] = (out["bilangan"] / out["bilangan"].sum() * 100).round(2)
    out["purata_ikm"] = out["purata_ikm"].round(2)
    return out.sort_values("bilangan", ascending=False)

def top_drivers(row):
    fields = {
        "Ekonomi": row.get("ekonomi", 0),
        "Politik": row.get("politik", 0),
        "Sosial": row.get("sosial", 0),
        "Digital/Media": row.get("digital", 0),
        "Keselamatan": row.get("keselamatan", 0),
        "Defisit Kepercayaan": row.get("defisit_kepercayaan", 0),
        "Risiko Perpaduan": row.get("risiko_perpaduan", 0),
        "Toksik Media Sosial": row.get("toksik", 0),
        "Hate Speech": row.get("kadar_hate_speech", 0),
    }
    return sorted(fields.items(), key=lambda x: x[1], reverse=True)[:4]

def intervention_plan(row):
    drivers = top_drivers(row)
    actions = []
    for name, val in drivers:
        if name in ["Digital/Media", "Toksik Media Sosial", "Hate Speech"]:
            actions.append(("Digital & Naratif", "Pemantauan media sosial, counter-narrative, fact-checking dan laporan sentimen mingguan."))
        elif name == "Ekonomi":
            actions.append(("Ekonomi Komuniti", "Libat urus isu kos sara hidup, bantuan bersasar, penerangan dasar dan pemetaan kumpulan rentan."))
        elif name == "Politik":
            actions.append(("Dialog & Stabiliti", "Dialog rentas komuniti, mediator setempat dan pengurusan naratif politik sensitif."))
        elif name == "Sosial":
            actions.append(("Kohesi Sosial", "Aktiviti komuniti bersama, forum kejiranan dan program kepercayaan antara kumpulan."))
        elif name == "Keselamatan":
            actions.append(("Keselamatan Komuniti", "Koordinasi agensi keselamatan, saluran aduan pantas dan pemantauan kawasan risiko."))
        else:
            actions.append(("Kepercayaan Institusi", "Townhall, komunikasi dasar yang jelas dan mekanisme maklum balas komuniti."))
    # remove duplicates preserving order
    seen = set()
    unique = []
    for a in actions:
        if a[0] not in seen:
            unique.append(a); seen.add(a[0])
    return drivers, unique[:4]

def explain_model_text():
    return {
        "survey": "IKM Survey = Σ (berat indikator × skor indikator). Semua pemberat dinormalisasi supaya jumlah pemberat = 1.",
        "komposit": "IKM Komposit Daerah = 0.60(IKM Survey) + 0.30(Risiko Digital Media Sosial) + 0.10(Kadar Hate Speech).",
        "risk": "Tahap risiko: Rendah <40, Sederhana 40–59.99, Tinggi 60–74.99, Kritikal ≥75."
    }
