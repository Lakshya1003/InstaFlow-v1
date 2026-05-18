"""
Insta Flow — Chart Builder Module
Plotly charts with retro-compatible theming: visible text, white backgrounds, dark axes.
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

COLORS = ['#3a6ea5', '#e8832a', '#2d8b4e', '#c23b22', '#7c3aed',
          '#0d9488', '#d97706', '#6366f1', '#ec4899', '#14b8a6']

LAYOUT_DEFAULTS = dict(
    font=dict(family="'IBM Plex Mono', Courier, monospace", size=11, color="#1a1a1a"),
    paper_bgcolor='#faf5ee',
    plot_bgcolor='#ffffff',
    margin=dict(l=45, r=15, t=45, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=10, color="#1a1a1a")),
    hoverlabel=dict(bgcolor="#faf5ee", font_size=11,
                    font_family="'IBM Plex Mono', monospace",
                    bordercolor="#1a1a1a"),
)

def _apply_layout(fig, title=""):
    fig.update_layout(**LAYOUT_DEFAULTS,
        title=dict(text=title, font=dict(size=13, color="#1a1a1a", family="'VT323', monospace")))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e8e0d4',
                     linecolor='#1a1a1a', linewidth=1,
                     tickfont=dict(size=10, color="#4a3728"))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e8e0d4',
                     linecolor='#1a1a1a', linewidth=1,
                     tickfont=dict(size=10, color="#4a3728"))
    return fig

def bar_chart(df, x, y, title="", color=None):
    fig = px.bar(df, x=x, y=y, color=color, color_discrete_sequence=COLORS,
                 title=title, barmode='group')
    return _apply_layout(fig, title)

def line_chart(df, x, y, title="", color=None):
    fig = px.line(df, x=x, y=y, color=color, color_discrete_sequence=COLORS,
                  title=title, markers=True)
    fig.update_traces(line=dict(width=2.5))
    return _apply_layout(fig, title)

def area_chart(df, x, y, title="", color=None):
    fig = px.area(df, x=x, y=y, color=color, color_discrete_sequence=COLORS, title=title)
    fig.update_traces(line=dict(width=2))
    return _apply_layout(fig, title)

def pie_chart(df, names, values, title=""):
    fig = px.pie(df, names=names, values=values, color_discrete_sequence=COLORS, title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      textfont=dict(size=11, color="#1a1a1a"),
                      hoverinfo='label+percent+value')
    fig.update_layout(**LAYOUT_DEFAULTS,
        title=dict(text=title, font=dict(size=13, color="#1a1a1a", family="'VT323', monospace")))
    return fig

def donut_chart(df, names, values, title=""):
    fig = px.pie(df, names=names, values=values, hole=0.45,
                 color_discrete_sequence=COLORS, title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      textfont=dict(size=11, color="#1a1a1a"))
    fig.update_layout(**LAYOUT_DEFAULTS,
        title=dict(text=title, font=dict(size=13, color="#1a1a1a", family="'VT323', monospace")))
    return fig

def scatter_plot(df, x, y, title="", color=None):
    fig = px.scatter(df, x=x, y=y, color=color, color_discrete_sequence=COLORS,
                     title=title, opacity=0.7)
    return _apply_layout(fig, title)

def stacked_bar(df, x, y, color, title=""):
    fig = px.bar(df, x=x, y=y, color=color, color_discrete_sequence=COLORS,
                 title=title, barmode='stack')
    return _apply_layout(fig, title)

def histogram(df, x, title="", nbins=30):
    fig = px.histogram(df, x=x, nbins=nbins, color_discrete_sequence=[COLORS[0]], title=title)
    fig.update_traces(marker_line_color='#1a1a1a', marker_line_width=0.5)
    return _apply_layout(fig, title)

def heatmap(corr_matrix, title="Correlation Heatmap"):
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.index,
        colorscale='RdBu_r', zmin=-1, zmax=1,
        text=np.round(corr_matrix.values, 2), texttemplate='%{text}',
        textfont=dict(size=10, color="#1a1a1a")))
    return _apply_layout(fig, title)

CHART_REGISTRY = {
    'Bar Chart': bar_chart, 'Line Chart': line_chart, 'Area Chart': area_chart,
    'Pie Chart': pie_chart, 'Donut Chart': donut_chart, 'Scatter Plot': scatter_plot,
    'Stacked Bar Chart': stacked_bar, 'Histogram': histogram, 'Heatmap': heatmap,
}
