# src/callbacks/view_dim_distribution.py

from dash import Input, Output
import plotly.graph_objects as go
import numpy as np
import numexpr as ne
from dash.exceptions import PreventUpdate
from scipy.stats import norm, lognorm, beta, gamma
from src.stores.global_store import dimensions_store


def register_view_dim_distribution_callback(app):
    @app.callback(
        Output("dimension-distribution-plot", "figure"),
        Output("dimension-statistics", "children"),
        Input("select-dim-to-view", "value")
    )
    def update_distribution_view(selected_dim_key):
        if selected_dim_key is None:
            # Return an empty figure and a message if no dimension is selected
            fig = go.Figure()
            fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                plot_bgcolor="white",
                margin=dict(l=40, r=40, t=40, b=40),
                height=350
            )
            fig.add_annotation(
                text="Please select a dimension to view its distribution",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color="gray"),
                align="center"
            )
            return fig, "Please select a dimension first"

        dim = dimensions_store.get(selected_dim_key)
        if dim is None:
            return go.Figure(), "Dimension not found."

        dist_name = dim.get("dist")
        para1 = dim.get("para1")
        para2 = dim.get("para2")

        # Check if distribution type and parameters are provided
        if dist_name is None:
            return go.Figure(), "Please select a distribution type first."
        
        if para1 is None or para2 is None:
            return go.Figure(), "Please provide both parameters."

        # Make sure parameters are numeric expressions
        try:
            if not isinstance(para1, (int, float)):
                para1 = float(ne.evaluate(str(para1)))
            if not isinstance(para2, (int, float)):
                para2 = float(ne.evaluate(str(para2)))
        except Exception as e:
            return go.Figure(), f"Invalid parameters. Must be numeric expressions. Error: {str(e)}"

        x = None
        y = None
        stats = ""
        dim_name = dim.get("name", "Unknown")

        try:
            if dist_name == "normal":
                if para2 <= 0:
                    return go.Figure(), "Standard deviation must be greater than 0 for normal distribution."
                x = np.linspace(para1 - 4 * para2, para1 + 4 * para2, 500)
                y = norm.pdf(x, loc=para1, scale=para2)
                stats = f"Distribution: Normal\nMean (μ): {para1:.3f}\nStd Dev (σ): {para2:.3f}\nVariance: {para2**2:.3f}"

            elif dist_name == "lognormal":
                if para2 <= 0:
                    return go.Figure(), "Shape parameter must be greater than 0 for lognormal distribution."
                x = np.linspace(0.001, np.exp(para1 + 3 * para2), 500)
                y = lognorm.pdf(x, s=para2, scale=np.exp(para1))
                mean = np.exp(para1 + 0.5 * para2**2)
                std = np.sqrt((np.exp(para2**2) - 1) * np.exp(2 * para1 + para2**2))
                stats = f"Distribution: Lognormal\nLocation Parameter: {para1:.3f}\nShape Parameter: {para2:.3f}\nMean: {mean:.3f}\nStd Dev: {std:.3f}"

            elif dist_name == "beta":
                if para1 <= 0 or para2 <= 0:
                    return go.Figure(), "Both parameters must be greater than 0 for Beta distribution."
                x = np.linspace(0.001, 0.999, 500)
                y = beta.pdf(x, a=para1, b=para2)
                mean = para1 / (para1 + para2)
                var = (para1 * para2) / (((para1 + para2)**2) * (para1 + para2 + 1))
                stats = f"Distribution: Beta\nα Parameter: {para1:.3f}\nβ Parameter: {para2:.3f}\nMean: {mean:.3f}\nStd Dev: {np.sqrt(var):.3f}\nVariance: {var:.3f}"

            elif dist_name == "gamma":
                if para1 <= 0 or para2 <= 0:
                    return go.Figure(), "Both parameters must be greater than 0 for Gamma distribution."
                x = np.linspace(0.001, para1 * para2 * 3, 500)
                y = gamma.pdf(x, a=para1, scale=para2)
                mean = para1 * para2
                std = np.sqrt(para1) * para2
                stats = f"Distribution: Gamma\nShape Parameter (k): {para1:.3f}\nScale Parameter (θ): {para2:.3f}\nMean: {mean:.3f}\nStd Dev: {std:.3f}\nVariance: {std**2:.3f}"

            else:
                return go.Figure(), f"Unsupported distribution type: {dist_name}"

            # Create the figure
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x, y=y, 
                mode="lines", 
                name=f"{dim_name} ({dist_name})",
                line=dict(width=3)
            ))
            
            fig.update_layout(
                title=f"Probability Density Function of Dimension '{dim_name}'",
                margin=dict(l=40, r=20, t=60, b=40),
                xaxis_title="Value",
                yaxis_title="Probability Density",
                height=350,
                plot_bgcolor="white",
                paper_bgcolor="white"
            )
            
            # Add grid lines
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

            return fig, stats

        except Exception as e:
            return go.Figure(), f"Error calculating distribution: {str(e)}"