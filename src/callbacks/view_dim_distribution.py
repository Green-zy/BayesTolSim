# src/callbacks/view_dim_distribution.py

from dash import Input, Output, ALL
import plotly.graph_objects as go
import numpy as np
import numexpr as ne
from dash.exceptions import PreventUpdate
from scipy.stats import norm, lognorm, beta, gamma, uniform
from src.stores.global_store import dimensions_store


def register_view_dim_distribution_callback(app):
    def _calculate_cdf(x_values, dist_name, para1, para2):
        """Calculate cumulative distribution function values"""
        try:
            if dist_name == "normal":
                return norm.cdf(x_values, loc=para1, scale=para2)
            elif dist_name == "lognormal":
                return lognorm.cdf(x_values, s=para2, scale=np.exp(para1))
            elif dist_name == "beta":
                return beta.cdf(x_values, a=para1, b=para2)
            elif dist_name == "gamma":
                return gamma.cdf(x_values, a=para1, scale=para2)
            elif dist_name == "uniform":
                return uniform.cdf(x_values, loc=para1, scale=para2-para1)
            else:
                return np.zeros_like(x_values)
        except:
            return np.zeros_like(x_values)

    @app.callback(
        Output("dimension-distribution-plot", "figure"),
        Output("dimension-statistics", "children"),
        Input("select-dim-to-view", "value"),
        Input({"type": "dim-para1", "index": ALL}, "value"),  # Added to update plot when parameters change
        Input({"type": "dim-para2", "index": ALL}, "value"),  # Added to update plot when parameters change
        Input({"type": "dim-dist", "index": ALL}, "value"),   # Added to update plot when distribution changes
    )
    def update_distribution_view(selected_dim_key, para1_values, para2_values, dist_values):
        if selected_dim_key is None:
            # Return an empty figure and a message if no dimension is selected
            fig = go.Figure()
            fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                plot_bgcolor="white",
                margin=dict(l=40, r=40, t=40, b=40),
                height=450,  # Increased height
                width=600    # Reduced width
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
            fig = go.Figure()
            fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                plot_bgcolor="white",
                margin=dict(l=40, r=40, t=40, b=40),
                height=450,
                width=600
            )
            fig.add_annotation(
                text="Please select a distribution type first",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color="gray"),
                align="center"
            )
            return fig, "Please select a distribution type first."
        
        if para1 is None or para2 is None:
            fig = go.Figure()
            fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                plot_bgcolor="white",
                margin=dict(l=40, r=40, t=40, b=40),
                height=450,
                width=600
            )
            fig.add_annotation(
                text="Please provide both parameters",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color="gray"),
                align="center"
            )
            return fig, "Please provide both parameters."

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
                p5 = norm.ppf(0.05, loc=para1, scale=para2)
                p95 = norm.ppf(0.95, loc=para1, scale=para2)
                stats = f"Distribution: Normal\nMean (μ): {para1:.3f}\nStd Dev (σ): {para2:.3f}\n5th Percentile: {p5:.3f}\n95th Percentile: {p95:.3f}"

            elif dist_name == "lognormal":
                if para2 <= 0:
                    return go.Figure(), "Shape parameter must be greater than 0 for lognormal distribution."
                
                # Calculate meaningful range for lognormal (from 0.5th to 99.5th percentile with more padding)
                p0_5 = lognorm.ppf(0.005, s=para2, scale=np.exp(para1))
                p99_5 = lognorm.ppf(0.995, s=para2, scale=np.exp(para1))
                range_span = p99_5 - p0_5
                x_min = max(0.001, p0_5 - 0.2 * range_span)
                x_max = p99_5 + 0.2 * range_span
                
                x = np.linspace(x_min, x_max, 500)
                y = lognorm.pdf(x, s=para2, scale=np.exp(para1))
                mean = np.exp(para1 + 0.5 * para2**2)
                std = np.sqrt((np.exp(para2**2) - 1) * np.exp(2 * para1 + para2**2))
                p5 = lognorm.ppf(0.05, s=para2, scale=np.exp(para1))
                p95 = lognorm.ppf(0.95, s=para2, scale=np.exp(para1))
                stats = f"Distribution: Lognormal\nLocation Parameter: {para1:.3f}\nShape Parameter: {para2:.3f}\nMean: {mean:.3f}\nStd Dev: {std:.3f}\n5th Percentile: {p5:.3f}\n95th Percentile: {p95:.3f}"

            elif dist_name == "beta":
                if para1 <= 0 or para2 <= 0:
                    return go.Figure(), "Both parameters must be greater than 0 for Beta distribution."
                x = np.linspace(0.001, 0.999, 500)
                y = beta.pdf(x, a=para1, b=para2)
                mean = para1 / (para1 + para2)
                var = (para1 * para2) / (((para1 + para2)**2) * (para1 + para2 + 1))
                p5 = beta.ppf(0.05, a=para1, b=para2)
                p95 = beta.ppf(0.95, a=para1, b=para2)
                stats = f"Distribution: Beta\nα Parameter: {para1:.3f}\nβ Parameter: {para2:.3f}\nMean: {mean:.3f}\nStd Dev: {np.sqrt(var):.3f}\n5th Percentile: {p5:.3f}\n95th Percentile: {p95:.3f}"

            elif dist_name == "gamma":
                if para1 <= 0 or para2 <= 0:
                    return go.Figure(), "Both parameters must be greater than 0 for Gamma distribution."
                
                # Calculate meaningful range for gamma (from 0.5th to 99.5th percentile with more padding)
                p0_5 = gamma.ppf(0.005, a=para1, scale=para2)
                p99_5 = gamma.ppf(0.995, a=para1, scale=para2)
                range_span = p99_5 - p0_5
                x_min = max(0.001, p0_5 - 0.2 * range_span)
                x_max = p99_5 + 0.2 * range_span
                
                x = np.linspace(x_min, x_max, 500)
                y = gamma.pdf(x, a=para1, scale=para2)
                mean = para1 * para2
                std = np.sqrt(para1) * para2
                p5 = gamma.ppf(0.05, a=para1, scale=para2)
                p95 = gamma.ppf(0.95, a=para1, scale=para2)
                stats = f"Distribution: Gamma\nShape Parameter (k): {para1:.3f}\nScale Parameter (θ): {para2:.3f}\nMean: {mean:.3f}\nStd Dev: {std:.3f}\n5th Percentile: {p5:.3f}\n95th Percentile: {p95:.3f}"

            elif dist_name == "uniform":
                if para2 <= para1:
                    return go.Figure(), "Upper bound (b) must be greater than lower bound (a) for Uniform distribution."
                x = np.linspace(para1 - 0.1*(para2-para1), para2 + 0.1*(para2-para1), 500)
                y = uniform.pdf(x, loc=para1, scale=para2-para1)
                mean = (para1 + para2) / 2
                var = (para2 - para1)**2 / 12
                std = np.sqrt(var)
                p5 = uniform.ppf(0.05, loc=para1, scale=para2-para1)
                p95 = uniform.ppf(0.95, loc=para1, scale=para2-para1)
                stats = f"Distribution: Uniform\nLower Bound (a): {para1:.3f}\nUpper Bound (b): {para2:.3f}\nMean: {mean:.3f}\nStd Dev: {std:.3f}\n5th Percentile: {p5:.3f}\n95th Percentile: {p95:.3f}"

            else:
                return go.Figure(), f"Unsupported distribution type: {dist_name}"

            # Create the figure with adjusted dimensions and custom hover template
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x, y=y, 
                mode="lines", 
                name=f"{dim_name} ({dist_name})",
                line=dict(width=3),
                hovertemplate="<b>Value:</b> %{x:.4f}<br><b>Density:</b> %{y:.4f}<br><b>CDF:</b> %{customdata:.4f}<extra></extra>",
                customdata=_calculate_cdf(x, dist_name, para1, para2)
            ))
            
            fig.update_layout(
                title=f"Probability Density Function of Dimension '{dim_name}'",
                margin=dict(l=40, r=20, t=60, b=40),
                xaxis_title="Value",
                yaxis_title="Probability Density",
                height=450,  # Increased height
                width=600,   # Reduced width
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                title_font_size=14
            )
            
            # Add more comfortable grid lines with better styling
            fig.update_xaxes(
                showgrid=True, 
                gridwidth=0.8, 
                gridcolor='rgba(180,180,180,0.4)',
                minor=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(200,200,200,0.2)'
                ),
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='rgba(100,100,100,0.6)'
            )
            fig.update_yaxes(
                showgrid=True, 
                gridwidth=0.8, 
                gridcolor='rgba(180,180,180,0.4)',
                minor=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(200,200,200,0.2)'
                ),
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='rgba(100,100,100,0.6)'
            )

            return fig, stats

        except Exception as e:
            return go.Figure(), f"Error calculating distribution: {str(e)}"