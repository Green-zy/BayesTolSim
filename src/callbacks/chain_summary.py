# src/callbacks/chain_summary.py

from dash import Input, Output, State, ALL
import pandas as pd
import plotly.graph_objects as go

def register_chain_summary_callback(app):
    @app.callback(
        Output("chain-plot", "figure"),
        Input({"type": "dim-name", "index": ALL}, "value"),
        Input({"type": "dim-dir", "index": ALL}, "value"),
        Input({"type": "dim-nominal", "index": ALL}, "value"),
        Input({"type": "dim-dist", "index": ALL}, "value"),
    )
    def update_chain_figure(names, dirs, nominals, dists):
        if not names or all(v in [None, "", []] for v in names):
            fig = go.Figure()
            fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                plot_bgcolor="white",
                margin=dict(l=40, r=40, t=40, b=40),
                height=200
            )
            fig.add_annotation(
                text="Please add dimensions to visualize the chain",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color="gray"),
                align="center"
            )
            return fig

        df = pd.DataFrame({
            "Dimension": names,
            "Direction": dirs,
            "Nominal": nominals,
            "Distribution": dists
        }).fillna("")

        fig = go.Figure()
        x_start = 0
        current_dir = None
        y = 0
        row_height = 0.03
        max_x = 0

        for i, row in df.iterrows():
            try:
                length = float(row["Nominal"])
            except:
                length = 0.0

            direction = row["Direction"]
            name = row["Dimension"] or f"Dim {i}"

            if i == 0:
                y = 0
                current_dir = direction
            elif direction != current_dir:
                y += 1
                current_dir = direction

            y_real = y * row_height
            x_end = x_start + (length if direction == "+" else -length)

            fig.add_trace(go.Scatter(
                x=[x_start, x_end],
                y=[y_real, y_real],
                mode="lines+markers+text",
                text=[name, ""],
                textposition="top center",
                line=dict(width=4, color="blue" if direction == "+" else "red"),
                marker=dict(size=8),
                showlegend=False
            ))

            x_start = x_end
            max_x = max(max_x, abs(x_end))

        max_y = y * row_height + 0.03

        fig.add_shape(type="line", x0=0, x1=0, y0=0, y1=max_y,
                      line=dict(dash="dot", width=1, color="black"))
        fig.add_shape(type="line", x0=x_start, x1=x_start, y0=0, y1=max_y,
                      line=dict(dash="dot", width=1, color="black"))

        y_anno = max_y
        fig.add_annotation(
            x=x_start / 2,
            y=y_anno + 0.015,
            text=f"{round(abs(x_start), 2)} mm",
            showarrow=False,
            font=dict(size=10),
        )
        fig.add_shape(
            type="line",
            x0=0, x1=x_start,
            y0=y_anno, y1=y_anno,
            line=dict(
                color="black",
                width=1.5,
                dash="solid"
            ),
            xref="x", yref="y",
            layer="above"
        )

        fig.update_layout(
            height=min(400, 150 + y * 20),  
            yaxis_visible=False,
            xaxis_title="Dimension (mm)",
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor="white",
        )

        return fig