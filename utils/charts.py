
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

RISK_COLORS = {"Rendah":"#0F9D58", "Sederhana":"#D6A437", "Tinggi":"#F29900", "Kritikal":"#D93025", "-":"#6B7C8F"}

def bar_compare(df, x, y, color=None, title="", orientation="v", height=430):
    fig = px.bar(
        df, x=x, y=y, color=color,
        color_discrete_map=RISK_COLORS,
        orientation=orientation,
        text_auto=".2f",
        title=title
    )
    fig.update_traces(marker_line_width=0, textposition="outside", cliponaxis=False)
    fig.update_layout(
        height=height,
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#102030"),
        title=dict(font=dict(size=20, color="#061A33")),
        margin=dict(l=20,r=20,t=60,b=40)
    )
    return fig

def donut(df, names, values, title=""):
    fig = px.pie(df, names=names, values=values, hole=.55, title=title)
    fig.update_traces(textinfo="percent+label", marker=dict(line=dict(color="white", width=2)))
    fig.update_layout(height=390, paper_bgcolor="rgba(255,255,255,0)", title=dict(font=dict(size=18, color="#061A33")))
    return fig

def radar(labels, values, title=""):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill="toself", name="Skor"))
    fig.update_layout(
        title=title,
        height=440,
        polar=dict(radialaxis=dict(visible=True, range=[0,100])),
        paper_bgcolor="rgba(255,255,255,0)",
        showlegend=False
    )
    return fig

def heatmap_corr(df, title="Matriks Korelasi"):
    fig = px.imshow(df.corr(numeric_only=True), text_auto=".2f", aspect="auto", title=title, color_continuous_scale="RdBu_r")
    fig.update_layout(height=520, paper_bgcolor="rgba(255,255,255,0)", title=dict(font=dict(size=18, color="#061A33")))
    return fig
