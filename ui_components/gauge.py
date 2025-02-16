import plotly.graph_objects as go
import streamlit as st


def plot_gauge(indicator_value, indicator_color, indicator_title, max_bound):
    fig = go.Figure(
        go.Indicator(
            value=indicator_value,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "font.size": 48,
                "font.color": indicator_color
            },
            title={
                "text": indicator_title,
                "font": {"size": 20},
            },
            gauge={
                "axis": {
                    "range": [0, max_bound],
                    "tickwidth": 1,
                    "tickmode": "array",
                    "tickvals": [0, indicator_value, max_bound],
                },
                "bar": {"color": indicator_color},
                'bgcolor': "cyan",
                "threshold": {
                    "line": {"color": indicator_color, "width": 4},
                    "thickness": 0.75,
                    "value": indicator_value
                },
                'borderwidth': 2,
                'bordercolor': "gray",
                # 'steps': [{'range': [0, max_bound], 'color': 'cyan'}],

            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=150,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)
