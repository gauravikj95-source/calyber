import streamlit as st
import plotly.graph_objects as go
import pandas as pd

COLORS = {
    "bg": "#FFFFFF",
    "surface": "#F8FAFC",
    "card": "#FFFFFF",
    "border": "#E5E7EB",
    "text": "#0F172A",
    "text_secondary": "#64748B",
    "text_muted": "#94A3B8",
    "accent": "#EF4444",
    "success": "#059669",
    "warning": "#D97706",
    "danger": "#DC2626",
}

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#64748B", size=12),
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(showgrid=False, zeroline=False, color="#94A3B8", linecolor="#E5E7EB"),
    yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False, color="#94A3B8", linecolor="#E5E7EB"),
)


def hero_header(brand, tagline, description):
    html = (
        '<div style="text-align: center; padding: 56px 24px 40px 24px;">'
        '<div style="font-family: Inter, sans-serif; font-size: 56px; font-weight: 900; color: #0F172A; letter-spacing: 0.18em; line-height: 1; margin-bottom: 20px;">' + brand + '</div>'
        '<div style="font-family: Inter, sans-serif; font-size: 18px; font-weight: 500; color: #475569; margin-bottom: 24px; letter-spacing: 0.01em;">' + tagline + '</div>'
        '<div style="font-family: Inter, sans-serif; font-size: 15px; color: #64748B; max-width: 640px; margin: 0 auto; line-height: 1.65;">' + description + '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def hero_card(label, headline, description):
    html = (
        '<div style="background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 16px; padding: 48px 44px; margin-bottom: 32px;">'
        '<div style="color: #64748B; font-size: 11px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 16px;">' + label + '</div>'
        '<div style="font-family: Inter, sans-serif; font-size: 48px; font-weight: 900; color: #0F172A; line-height: 1.08; letter-spacing: -0.03em; margin-bottom: 20px; max-width: 800px;">' + headline + '</div>'
        '<div style="font-family: Inter, sans-serif; font-size: 15px; color: #64748B; line-height: 1.65; max-width: 640px;">' + description + '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def section_label(text):
    html = '<div style="color: #64748B; font-size: 11px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 12px;">' + text + '</div>'
    st.markdown(html, unsafe_allow_html=True)


def section_header(title, subtitle=None):
    sub_html = ""
    if subtitle:
        sub_html = '<div style="color: #64748B; font-size: 15px; margin-top: 8px; line-height: 1.5;">' + subtitle + '</div>'
    html = (
        '<div style="margin: 48px 0 28px 0;">'
        '<div style="color: #0F172A; font-size: 32px; font-weight: 800; letter-spacing: -0.025em; line-height: 1.15;">' + title + '</div>'
        + sub_html +
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def kpi_card(label, value, subtext=None, color=None):
    accent = color or COLORS["text"]
    sub_html = ""
    if subtext:
        sub_html = '<div style="color: #94A3B8; font-size: 13px; margin-top: 8px;">' + subtext + '</div>'
    html = (
        '<div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 24px 26px; height: 100%;">'
        '<div style="color: #64748B; font-size: 13px; font-weight: 500; margin-bottom: 12px;">' + label + '</div>'
        '<div style="color: ' + accent + '; font-size: 34px; font-weight: 800; line-height: 1; font-family: Inter, sans-serif; letter-spacing: -0.02em;">' + str(value) + '</div>'
        + sub_html +
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def kpi_row(items):
    cols = st.columns(len(items), gap="medium")
    for col, item in zip(cols, items):
        with col:
            kpi_card(
                item.get("label", ""),
                item.get("value", ""),
                item.get("subtext"),
                item.get("color")
            )


def card_label(label):
    html = '<div style="color: #64748B; font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px;">' + label + '</div>'
    st.markdown(html, unsafe_allow_html=True)


def result_card(label, value, subtext=None, value_color=None):
    color = value_color or COLORS["text"]
    sub_html = ""
    if subtext:
        sub_html = '<div style="color: #94A3B8; font-size: 13px; margin-top: 10px;">' + subtext + '</div>'
    html = (
        '<div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 24px 26px; height: 100%;">'
        '<div style="color: #64748B; font-size: 13px; font-weight: 500; margin-bottom: 12px;">' + label + '</div>'
        '<div style="color: ' + color + '; font-size: 32px; font-weight: 800; line-height: 1; font-family: Inter, sans-serif; letter-spacing: -0.02em;">' + str(value) + '</div>'
        + sub_html +
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def comparison_card(left_title, left_value, right_title, right_value, savings=None):
    html = (
        '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">'
        '<div style="background: #FEF2F2; border: 1px solid #FECACA; border-radius: 14px; padding: 28px;">'
        '<div style="color: #991B1B; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px;">' + left_title + '</div>'
        '<div style="color: #DC2626; font-size: 36px; font-weight: 800; font-family: Inter, sans-serif; letter-spacing: -0.02em;">' + str(left_value) + '</div>'
        '</div>'
        '<div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 14px; padding: 28px;">'
        '<div style="color: #065F46; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px;">' + right_title + '</div>'
        '<div style="color: #059669; font-size: 36px; font-weight: 800; font-family: Inter, sans-serif; letter-spacing: -0.02em;">' + str(right_value) + '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

    if savings and savings > 0:
        savings_html = (
            '<div style="background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 14px; padding: 18px 24px; margin-top: 20px; text-align: center;">'
            '<span style="color: #64748B; font-size: 13px; font-weight: 500;">You save</span>'
            '<span style="color: #059669; font-size: 24px; font-weight: 800; margin-left: 12px; font-family: Inter, sans-serif;">Rs ' + str(savings) + '</span>'
            '</div>'
        )
        st.markdown(savings_html, unsafe_allow_html=True)


def fairness_badge(grade, label, color):
    html = (
        '<div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 16px; padding: 44px; text-align: center;">'
        '<div style="color: #64748B; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 20px;">Fairness Grade</div>'
        '<div style="color: ' + color + '; font-size: 112px; font-weight: 900; line-height: 1; font-family: Inter, sans-serif; letter-spacing: -0.04em;">' + grade + '</div>'
        '<div style="color: ' + color + '; font-size: 15px; font-weight: 700; margin-top: 18px; letter-spacing: 0.1em; text-transform: uppercase;">' + label + '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def metric_row(items):
    html = '<div style="display: grid; grid-template-columns: repeat(' + str(len(items)) + ', 1fr); gap: 20px;">'
    for item in items:
        color = item.get("color", COLORS["text"])
        html += (
            '<div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 24px 26px;">'
            '<div style="color: #64748B; font-size: 13px; font-weight: 500; margin-bottom: 12px;">' + item["label"] + '</div>'
            '<div style="color: ' + color + '; font-size: 32px; font-weight: 800; font-family: Inter, sans-serif; letter-spacing: -0.02em;">' + str(item["value"]) + '</div>'
            '</div>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def callout(title, text, color=None):
    accent = color or "#0F172A"
    html = (
        '<div style="background: #F8FAFC; border-left: 4px solid ' + accent + '; border-radius: 10px; padding: 24px 28px; margin: 24px 0;">'
        '<div style="color: ' + accent + '; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 10px;">' + title + '</div>'
        '<div style="color: #334155; font-size: 15px; line-height: 1.65;">' + text + '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def bar_chart(data, x, y, color=None, height=300):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data[x], y=data[y],
        marker_color=color or "#0F172A",
        marker_line_width=0,
        text=data[y].apply(lambda v: f"{v:.2f}"),
        textposition="outside",
        textfont=dict(color="#0F172A", size=11),
    ))
    layout = dict(CHART_LAYOUT)
    layout["height"] = height
    layout["showlegend"] = False
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def line_chart(data, x, y, color=None, height=300):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data[x], y=data[y],
        mode="lines+markers",
        line=dict(color=color or "#0F172A", width=2.5),
        marker=dict(size=6, color=color or "#0F172A"),
    ))
    layout = dict(CHART_LAYOUT)
    layout["height"] = height
    layout["showlegend"] = False
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def donut_chart(data, labels, values, height=300):
    colors = ["#059669", "#2563EB", "#D97706", "#EA580C", "#DC2626"]
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=data[labels], values=data[values],
        hole=0.65,
        marker=dict(colors=colors[:len(data)]),
        textinfo="percent",
        textfont=dict(color="#FFFFFF", size=12),
    ))
    layout = dict(CHART_LAYOUT)
    layout["height"] = height
    layout["showlegend"] = True
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def dual_bar_chart(data, x, y1, y2, label1="Baseline", label2="Calyber", height=300):
    fig = go.Figure()
    fig.add_trace(go.Bar(name=label1, x=data[x], y=data[y1], marker_color="#DC2626", marker_line_width=0))
    fig.add_trace(go.Bar(name=label2, x=data[x], y=data[y2], marker_color="#059669", marker_line_width=0))
    layout = dict(CHART_LAYOUT)
    layout["height"] = height
    layout["barmode"] = "group"
    layout["showlegend"] = True
    layout["legend"] = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#64748B", size=11))
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def centered_container():
    """Returns a context for centered content."""
    return st.container()
