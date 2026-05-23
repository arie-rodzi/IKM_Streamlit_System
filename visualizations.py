
import plotly.express as px
import plotly.graph_objects as go
from styles import COLORWAY, RISK_COLORS, PLOTLY_TEMPLATE

def apply_layout(fig, height=420):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        margin=dict(l=20,r=20,t=55,b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(color="#EAF2F8"),
        colorway=COLORWAY,
        title_font=dict(size=18, color="#FFFFFF"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def bar(df, x, y, color=None, title="", orientation="v", height=420, text=None):
    fig = px.bar(df, x=x, y=y, color=color, orientation=orientation, title=title, text=text, color_discrete_map=RISK_COLORS)
    return apply_layout(fig, height)

def pie(df, names, values, title="", height=380):
    fig = px.pie(df, names=names, values=values, title=title, hole=.48, color=names, color_discrete_map=RISK_COLORS)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return apply_layout(fig, height)

def line(df, x, y, title="", height=420):
    fig = px.line(df, x=x, y=y, title=title, markers=True)
    fig.update_traces(line=dict(width=4), marker=dict(size=8))
    return apply_layout(fig, height)

def heatmap(corr, title="Korelasi Indikator", height=520):
    fig = px.imshow(corr, text_auto=".2f", aspect="auto", title=title, color_continuous_scale="RdYlGn_r")
    return apply_layout(fig, height)

def radar(labels, values, title="Profil Risiko Lokasi", height=430):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill="toself", line=dict(color="#00B4D8", width=3), fillcolor="rgba(0,180,216,.25)"))
    fig.update_layout(polar=dict(bgcolor="rgba(255,255,255,.04)", radialaxis=dict(visible=True, range=[0,100], gridcolor="rgba(255,255,255,.18)")), showlegend=False, title=title)
    return apply_layout(fig, height)

def scatter_social(df, title="Sentimen vs Toksisiti Media Sosial", height=450):
    sample = df.sample(min(7000, len(df)), random_state=7) if len(df) else df
    fig = px.scatter(sample, x="sentiment_score", y="toxicity_score", color="tahap_risiko_digital", size="engagement", hover_data=["negeri","daerah","platform","isu"], title=title, color_discrete_map=RISK_COLORS)
    return apply_layout(fig, height)
