import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

COLORS = {
    "bg": "#FFFFFF",
    "surface": "#F8FAFC",
    "surface_elevated": "#F1F5F9",
    "border": "#E2E8F0",
    "primary": "#0F172A",
    "accent": "#2563EB",
    "success": "#059669",
    "warning": "#D97706",
    "danger": "#DC2626",
    "text": "#0F172A",
    "text_secondary": "#64748B",
    "text_muted": "#94A3B8",
}

# Base layout WITHOUT showlegend
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#64748B", size=12),
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis=dict(showgrid=False, zeroline=False, color="#64748B"),
    yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False, color="#64748B"),
)


def hero_header(brand, tagline, description):
    html = (
        '<div class="hero-header">'
        '<div class="hero-brand">' + brand + '</div>'
        '<div class="hero-tagline">' + tagline + '</div>'
        '<div class="hero-description">' + description + '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def kpi_card(label, value, subtext=None, color=None):
    accent = color or COLORS["text"]
    sub_html = ""
    if subtext:
        sub_html = '<div style="color: ' + COLORS["text_muted"] + '; font-size: 12px; margin-top: 6px;">' + subtext + '</div>'
    html = (
        '<div style="background: ' + COLORS["surface"] + '; border: 1px solid ' + COLORS["border"] + '; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px;">'
        '<div style="color: ' + COLORS["text_secondary"] + '; font-size: 11px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 10px;">' + label + '</div>'
        '<div style="color: ' + accent + '; font-size: 32px; font-weight: 700; line-height: 1.1; font-family: JetBrains Mono, monospace;">' + str(value) + '</div>'
        + sub_html +
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def kpi_row(items):
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        with col:
            kpi_card(
                item.get("label", ""),
                item.get("value", ""),
                item.get("subtext"),
                item.get("color")
            )


def comparison_card(left_title, left_value, right_title, right_value, savings=None):
    html = (
        '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">'
        '<div style="background: #FEF2F2; border: 1px solid #FECACA; border-radius: 12px; padding: 24px;">'
        '<div style="color: #991B1B; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;">' + left_title + '</div>'
        '<div style="color: ' + COLORS["danger"] + '; font-size: 32px; font-weight: 700; margin-top: 10px; font-family: JetBrains Mono, monospace;">' + str(left_value) + '</div>'
        '</div>'
        '<div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 12px; padding: 24px;">'
        '<div style="color: #065F46; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;">' + right_title + '</div>'
        '<div style="color: ' + COLORS["success"] + '; font-size: 32px; font-weight: 700; margin-top: 10px; font-family: JetBrains Mono, monospace;">' + str(right_value) + '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

    if savings and savings > 0:
        savings_html = (
            '<div style="background: ' + COLORS["surface"] + '; border: 1px solid ' + COLORS["border"] + '; border-radius: 12px; padding: 14px 20px; margin-top: 16px; text-align: center;">'
            '<span style="color: ' + COLORS["text_secondary"] + '; font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em;">You save</span>'
            '<span style="color: ' + COLORS["success"] + '; font-size: 22px; font-weight: 700; margin-left: 10px; font-family: JetBrains Mono, monospace;">₹' + str(savings) + '</span>'
            '</div>'
        )
        st.markdown(savings_html, unsafe_allow_html=True)


def fairness_badge(grade, label, color):
    html = (
        '<div style="background: ' + COLORS["surface"] + '; border: 1px solid ' + COLORS["border"] + '; border-radius: 16px; padding: 40px; text-align: center;">'
        '<div style="color: ' + COLORS["text_secondary"] + '; font-size: 11px; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 16px; font-weight: 500;">Fairness Grade</div>'
        '<div style="color: ' + color + '; font-size: 104px; font-weight: 800; line-height: 1; font-family: JetBrains Mono, monospace;">' + grade + '</div>'
        '<div style="color: ' + color + '; font-size: 16px; font-weight: 600; margin-top: 16px; letter-spacing: 0.08em; text-transform: uppercase;">' + label + '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def metric_row(items):
    html = '<div style="display: flex; gap: 40px; padding: 16px 0;">'
    for item in items:
        color = item.get("color", COLORS["text"])
        html += (
            '<div>'
            '<div style="color: ' + COLORS["text_secondary"] + '; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 500;">' + item["label"] + '</div>'
            '<div style="color: ' + color + '; font-size: 22px; font-weight: 700; margin-top: 6px; font-family: JetBrains Mono, monospace;">' + str(item["value"]) + '</div>'
            '</div>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def callout(title, text, color=None):
    accent = color or COLORS["text"]
    html = (
        '<div style="background: ' + COLORS["surface"] + '; border-left: 4px solid ' + accent + '; border-radius: 8px; padding: 24px 28px; margin: 20px 0;">'
        '<div style="color: ' + accent + '; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px;">' + title + '</div>'
        '<div style="color: ' + COLORS["text"] + '; font-size: 15px; line-height: 1.65;">' + text + '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def section_header(title, subtitle=None):
    sub_html = ""
    if subtitle:
        sub_html = '<div style="color: ' + COLORS["text_secondary"] + '; font-size: 14px; margin-top: 4px;">' + subtitle + '</div>'
    html = (
        '<div style="margin: 40px 0 24px 0;">'
        '<div style="color: ' + COLORS["text"] + '; font-size: 24px; font-weight: 700; letter-spacing: -0.02em;">' + title + '</div>'
        + sub_html +
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def bar_chart(data, x, y, color=None, height=300):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data[x],
        y=data[y],
        marker_color=color or COLORS["text"],
        marker_line_width=0,
        text=data[y].apply(lambda v: f"{v:.2f}"),
        textposition="outside",
        textfont=dict(color=COLORS["text"], size=11),
    ))
    layout = dict(CHART_LAYOUT)
    layout["height"] = height
    layout["showlegend"] = False
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def line_chart(data, x, y, color=None, height=300):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data[x],
        y=data[y],
        mode="lines+markers",
        line=dict(color=color or COLORS["text"], width=2.5),
        marker=dict(size=6, color=color or COLORS["text"]),
        fill="tozeroy",
        fillcolor="rgba(15, 23, 42, 0.06)",
    ))
    layout = dict(CHART_LAYOUT)
    layout["height"] = height
    layout["showlegend"] = False
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def donut_chart(data, labels, values, height=300):
    colors = [COLORS["success"], COLORS["accent"], COLORS["warning"], "#EA580C", COLORS["danger"]]
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=data[labels],
        values=data[values],
        hole=0.65,
        marker=dict(colors=colors[:len(data)]),
        textinfo="percent",
        textfont=dict(color="#FFFFFF", size=12),
        hovertemplate="<b>%{label}</b><br>%{value} trips<br>%{percent}<extra></extra>",
    ))
    layout = dict(CHART_LAYOUT)
    layout["height"] = height
    layout["showlegend"] = False
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def dual_bar_chart(data, x, y1, y2, label1="Baseline", label2="Calyber", height=300):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=label1,
        x=data[x],
        y=data[y1],
        marker_color=COLORS["danger"],
        marker_line_width=0,
    ))
    fig.add_trace(go.Bar(
        name=label2,
        x=data[x],
        y=data[y2],
        marker_color=COLORS["success"],
        marker_line_width=0,
    ))
    layout = dict(CHART_LAYOUT)
    layout["height"] = height
    layout["barmode"] = "group"
    layout["showlegend"] = True
    layout["legend"] = dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color=COLORS["text_secondary"], size=11),
    )
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
