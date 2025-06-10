# src/callbacks/view_dim_distribution.py

from dash import Input, Output, ALL
import plotly.graph_objects as go
import numpy as np
import numexpr as ne
from dash.exceptions import PreventUpdate
from scipy.stats import norm, lognorm, gamma, uniform
from src.stores.global_store import dimensions_store


def register_view_dim_distribution_callback(app):
    def _calculate_cdf(x_values, dist_name, para1, para2):
        """Calculate cumulative distribution function values"""
        try:
            if dist_name == "normal":
                return norm.cdf(x_values, loc=para1, scale=para2)
            elif dist_name == "lognormal":
                return lognorm.cdf(x_values, s=para2, scale=np.exp(para1))
            elif dist_name == "gamma":
                return gamma.cdf(x_values, a=para1, scale=para2)
            elif dist_name == "uniform":
                return uniform.cdf(x_values, loc=para1, scale=para2-para1)
            else:
                return np.zeros_like(x_values)
        except:
            return np.zeros_like(x_values)

    def _calculate_pdf(x_values, dist_name, para1, para2):
        """Calculate probability density function values"""
        try:
            if dist_name == "normal":
                return norm.pdf(x_values, loc=para1, scale=para2)
            elif dist_name == "lognormal":
                return lognorm.pdf(x_values, s=para2, scale=np.exp(para1))
            elif dist_name == "gamma":
                return gamma.pdf(x_values, a=para1, scale=para2)
            elif dist_name == "uniform":
                return uniform.pdf(x_values, loc=para1, scale=para2-para1)
            else:
                return np.zeros_like(x_values)
        except:
            return np.zeros_like(x_values)

    def _get_distribution_range(dist_name, para1, para2):
        """Get appropriate x-range for plotting distribution"""
        try:
            if dist_name == "normal":
                x_min = para1 - 4 * para2
                x_max = para1 + 4 * para2
            elif dist_name == "lognormal":
                p0_5 = lognorm.ppf(0.005, s=para2, scale=np.exp(para1))
                p99_5 = lognorm.ppf(0.995, s=para2, scale=np.exp(para1))
                range_span = p99_5 - p0_5
                x_min = max(0.001, p0_5 - 0.2 * range_span)
                x_max = p99_5 + 0.2 * range_span
            elif dist_name == "gamma":
                p0_5 = gamma.ppf(0.005, a=para1, scale=para2)
                p99_5 = gamma.ppf(0.995, a=para1, scale=para2)
                range_span = p99_5 - p0_5
                x_min = max(0.001, p0_5 - 0.2 * range_span)
                x_max = p99_5 + 0.2 * range_span
            elif dist_name == "uniform":
                x_min = para1 - 0.1*(para2-para1)
                x_max = para2 + 0.1*(para2-para1)
            else:
                x_min, x_max = 0, 1
            return x_min, x_max
        except:
            return 0, 1

    def _format_statistics(dist_name, para1, para2, curve_type=""):
        """Format statistics text for a distribution"""
        try:
            if dist_name == "normal":
                mean = para1
                std = para2
                p5 = norm.ppf(0.05, loc=para1, scale=para2)
                p95 = norm.ppf(0.95, loc=para1, scale=para2)
                stats_text = f"{curve_type}Distribution: Normal\nMean (μ): {para1:.3f}\nStd Dev (σ): {para2:.3f}\n5th Percentile: {p5:.3f}\n95th Percentile: {p95:.3f}"
                
            elif dist_name == "lognormal":
                mean = np.exp(para1 + 0.5 * para2**2)
                std = np.sqrt((np.exp(para2**2) - 1) * np.exp(2 * para1 + para2**2))
                p5 = lognorm.ppf(0.05, s=para2, scale=np.exp(para1))
                p95 = lognorm.ppf(0.95, s=para2, scale=np.exp(para1))
                stats_text = f"{curve_type}Distribution: Lognormal\nLocation Parameter: {para1:.3f}\nShape Parameter: {para2:.3f}\nMean: {mean:.3f}\nStd Dev: {std:.3f}\n5th Percentile: {p5:.3f}\n95th Percentile: {p95:.3f}"
                
            elif dist_name == "gamma":
                mean = para1 * para2
                std = np.sqrt(para1) * para2
                p5 = gamma.ppf(0.05, a=para1, scale=para2)
                p95 = gamma.ppf(0.95, a=para1, scale=para2)
                stats_text = f"{curve_type}Distribution: Gamma\nShape Parameter (k): {para1:.3f}\nScale Parameter (θ): {para2:.3f}\nMean: {mean:.3f}\nStd Dev: {std:.3f}\n5th Percentile: {p5:.3f}\n95th Percentile: {p95:.3f}"
                
            elif dist_name == "uniform":
                mean = (para1 + para2) / 2
                var = (para2 - para1)**2 / 12
                std = np.sqrt(var)
                p5 = uniform.ppf(0.05, loc=para1, scale=para2-para1)
                p95 = uniform.ppf(0.95, loc=para1, scale=para2-para1)
                stats_text = f"{curve_type}Distribution: Uniform\nLower Bound (a): {para1:.3f}\nUpper Bound (b): {para2:.3f}\nMean: {mean:.3f}\nStd Dev: {std:.3f}\n5th Percentile: {p5:.3f}\n95th Percentile: {p95:.3f}"
                
            else:
                stats_text = f"{curve_type}Unsupported distribution: {dist_name}"
                
            return stats_text
        except Exception as e:
            return f"{curve_type}Error calculating statistics: {str(e)}"

    @app.callback(
        Output("dimension-distribution-plot", "figure"),
        Output("dimension-statistics", "children"),
        Input("select-dim-to-view", "value"),
        Input({"type": "dim-para1", "index": ALL}, "value"),
        Input({"type": "dim-para2", "index": ALL}, "value"),
        Input({"type": "dim-dist", "index": ALL}, "value"),
        Input({"type": "dim-mle-status", "index": ALL}, "data"),  # Added to update when MLE is applied
        Input({"type": "dim-bayes-status", "index": ALL}, "data"),  # Added to update when Bayesian is applied
    )
    def update_distribution_view(selected_dim_key, para1_values, para2_values, dist_values, mle_status_values, bayes_status_values):
        if selected_dim_key is None:
            # Return an empty figure and a message if no dimension is selected
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
                text="Please select a dimension",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=12, color="gray"),
                align="center"
            )
            return fig, "Please select a dimension first"

        dim = dimensions_store.get(selected_dim_key)
        if dim is None:
            return go.Figure(), "Dimension not found."

        dist_name = dim.get("dist")
        para1 = dim.get("para1")
        para2 = dim.get("para2")
        
        # Check if MLE or Bayesian analysis was applied
        mle_applied = dim.get("mle_applied", False)
        bayes_applied = dim.get("bayes_applied", False)

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

        dim_name = dim.get("name", "Unknown")
        
        try:
            # Validate distribution parameters
            if dist_name == "normal" and para2 <= 0:
                return go.Figure(), "Standard deviation must be greater than 0 for normal distribution."
            elif dist_name == "lognormal" and para2 <= 0:
                return go.Figure(), "Shape parameter must be greater than 0 for lognormal distribution."
            elif dist_name == "gamma" and (para1 <= 0 or para2 <= 0):
                return go.Figure(), "Both parameters must be greater than 0 for Gamma distribution."
            elif dist_name == "uniform" and para2 <= para1:
                return go.Figure(), "Upper bound (b) must be greater than lower bound (a) for Uniform distribution."

            # Create the figure
            fig = go.Figure()
            
            if bayes_applied:
                # Show prior, likelihood, and posterior curves
                prior_para1 = dim.get("prior_para1")
                prior_para2 = dim.get("prior_para2")
                likelihood_para1 = dim.get("likelihood_para1")
                likelihood_para2 = dim.get("likelihood_para2")
                posterior_para1 = dim.get("posterior_para1")
                posterior_para2 = dim.get("posterior_para2")
                
                # Also show histogram if we have Bayesian data
                bayes_data = dim.get("data", [])
                
                # Determine plotting range based on all three distributions
                x_ranges = []
                if prior_para1 is not None and prior_para2 is not None:
                    x_ranges.append(_get_distribution_range(dist_name, prior_para1, prior_para2))
                if likelihood_para1 is not None and likelihood_para2 is not None:
                    x_ranges.append(_get_distribution_range(dist_name, likelihood_para1, likelihood_para2))
                if posterior_para1 is not None and posterior_para2 is not None:
                    x_ranges.append(_get_distribution_range(dist_name, posterior_para1, posterior_para2))
                
                # Include data range if available
                if bayes_data:
                    data_min, data_max = min(bayes_data), max(bayes_data)
                    x_ranges.append((data_min - (data_max - data_min) * 0.1, data_max + (data_max - data_min) * 0.1))
                
                if x_ranges:
                    x_min = min([r[0] for r in x_ranges])
                    x_max = max([r[1] for r in x_ranges])
                    # Add some padding
                    padding = (x_max - x_min) * 0.1
                    x_min -= padding
                    x_max += padding
                else:
                    x_min, x_max = _get_distribution_range(dist_name, para1, para2)
                
                x = np.linspace(x_min, x_max, 500)
                
                # Add histogram first (so it appears behind curves)
                if bayes_data:
                    # Calculate histogram bins and counts for custom hover info
                    n_bins = min(20, max(5, len(bayes_data) // 3))
                    counts, bin_edges = np.histogram(bayes_data, bins=n_bins)
                    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
                    bin_widths = bin_edges[1:] - bin_edges[:-1]
                    total_area = np.sum(counts * bin_widths)
                    densities = counts / total_area
                    percentages = (counts / len(bayes_data)) * 100
                    
                    # Create custom hover text
                    hover_text = []
                    for i in range(len(counts)):
                        hover_text.append(
                            f"<b>Bin:</b> [{bin_edges[i]:.3f}, {bin_edges[i+1]:.3f})<br>"
                            f"<b>Count:</b> {counts[i]}<br>"
                            f"<b>Percentage:</b> {percentages[i]:.1f}%<br>"
                            f"<b>Density:</b> {densities[i]:.4f}"
                        )
                    
                    fig.add_trace(go.Bar(
                        x=bin_centers,
                        y=densities,
                        width=bin_widths,
                        name="Data Histogram",
                        opacity=0.3,
                        marker=dict(
                            color='rgba(128, 128, 128, 0)',  # No fill
                            line=dict(color='rgba(128, 128, 128, 0.3)', width=1)  # Gray outline with transparency
                        ),
                        hovertemplate="%{customdata}<extra></extra>",
                        customdata=hover_text
                    ))
                
                # Plot prior (blue)
                if prior_para1 is not None and prior_para2 is not None:
                    y_prior = _calculate_pdf(x, dist_name, prior_para1, prior_para2)
                    fig.add_trace(go.Scatter(
                        x=x, y=y_prior,
                        mode="lines",
                        name="Prior",
                        line=dict(width=2, color="blue"),
                        hovertemplate="<b>Prior</b><br>Value: %{x:.4f}<br>Density: %{y:.4f}<extra></extra>"
                    ))
                
                # Plot likelihood (orange)
                if likelihood_para1 is not None and likelihood_para2 is not None:
                    y_likelihood = _calculate_pdf(x, dist_name, likelihood_para1, likelihood_para2)
                    fig.add_trace(go.Scatter(
                        x=x, y=y_likelihood,
                        mode="lines",
                        name="Likelihood",
                        line=dict(width=2, color="orange"),
                        hovertemplate="<b>Likelihood</b><br>Value: %{x:.4f}<br>Density: %{y:.4f}<extra></extra>"
                    ))
                
                # Plot posterior (green with fill)
                if posterior_para1 is not None and posterior_para2 is not None:
                    y_posterior = _calculate_pdf(x, dist_name, posterior_para1, posterior_para2)
                    fig.add_trace(go.Scatter(
                        x=x, y=y_posterior,
                        mode="lines",
                        name="Posterior",
                        line=dict(width=3, color="green"),
                        fill="tozeroy",
                        fillcolor="rgba(0, 128, 0, 0.3)",
                        hovertemplate="<b>Posterior</b><br>Value: %{x:.4f}<br>Density: %{y:.4f}<br>CDF: %{customdata:.4f}<extra></extra>",
                        customdata=_calculate_cdf(x, dist_name, posterior_para1, posterior_para2)
                    ))
                
                # Prepare combined statistics
                stats_text = ""
                if prior_para1 is not None and prior_para2 is not None:
                    stats_text += "=== PRIOR ===\n" + _format_statistics(dist_name, prior_para1, prior_para2) + "\n\n"
                if likelihood_para1 is not None and likelihood_para2 is not None:
                    stats_text += "=== LIKELIHOOD ===\n" + _format_statistics(dist_name, likelihood_para1, likelihood_para2) + "\n\n"
                if posterior_para1 is not None and posterior_para2 is not None:
                    stats_text += "=== POSTERIOR ===\n" + _format_statistics(dist_name, posterior_para1, posterior_para2)
                
                title_text = f"Bayesian Analysis of Dimension '{dim_name}'"
                
            elif mle_applied:
                # Show MLE curve and data histogram
                mle_data = dim.get("mle_data", [])
                mle_para1 = dim.get("mle_para1", para1)
                mle_para2 = dim.get("mle_para2", para2)
                
                # Determine plotting range including data
                x_ranges = [_get_distribution_range(dist_name, mle_para1, mle_para2)]
                if mle_data:
                    data_min, data_max = min(mle_data), max(mle_data)
                    x_ranges.append((data_min - (data_max - data_min) * 0.1, data_max + (data_max - data_min) * 0.1))
                
                x_min = min([r[0] for r in x_ranges])
                x_max = max([r[1] for r in x_ranges])
                padding = (x_max - x_min) * 0.1
                x_min -= padding
                x_max += padding
                
                x = np.linspace(x_min, x_max, 500)
                
                # Add histogram first (so it appears behind the MLE curve)
                if mle_data:
                    # Calculate histogram bins and counts for custom hover info
                    n_bins = min(20, max(5, len(mle_data) // 3))
                    counts, bin_edges = np.histogram(mle_data, bins=n_bins)
                    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
                    bin_widths = bin_edges[1:] - bin_edges[:-1]
                    total_area = np.sum(counts * bin_widths)
                    densities = counts / total_area
                    percentages = (counts / len(mle_data)) * 100
                    
                    # Create custom hover text
                    hover_text = []
                    for i in range(len(counts)):
                        hover_text.append(
                            f"<b>Bin:</b> [{bin_edges[i]:.3f}, {bin_edges[i+1]:.3f})<br>"
                            f"<b>Count:</b> {counts[i]}<br>"
                            f"<b>Percentage:</b> {percentages[i]:.1f}%<br>"
                            f"<b>Density:</b> {densities[i]:.4f}"
                        )
                    
                    fig.add_trace(go.Bar(
                        x=bin_centers,
                        y=densities,
                        width=bin_widths,
                        name="Data Histogram",
                        opacity=0.3,
                        marker=dict(
                            color='rgba(128, 128, 128, 0)',  # No fill
                            line=dict(color='rgba(220, 85, 0, 1)', width=2)  # Orange outline
                        ),
                        hovertemplate="%{customdata}<extra></extra>",
                        customdata=hover_text
                    ))
                
                # Plot MLE curve
                y_mle = _calculate_pdf(x, dist_name, mle_para1, mle_para2)
                fig.add_trace(go.Scatter(
                    x=x, y=y_mle, 
                    mode="lines", 
                    name="MLE Fit",
                    line=dict(width=3, color="blue"),
                    hovertemplate="<b>MLE Fit</b><br>Value: %{x:.4f}<br>Density: %{y:.4f}<br>CDF: %{customdata:.4f}<extra></extra>",
                    customdata=_calculate_cdf(x, dist_name, mle_para1, mle_para2)
                ))
                
                stats_text = "=== MLE FIT ===\n" + _format_statistics(dist_name, mle_para1, mle_para2)
                if mle_data:
                    stats_text += f"\n\n=== DATA SUMMARY ===\nSample Size: {len(mle_data)}\nSample Mean: {np.mean(mle_data):.3f}\nSample Std: {np.std(mle_data, ddof=1):.3f}\nMin: {np.min(mle_data):.3f}\nMax: {np.max(mle_data):.3f}"
                title_text = f"MLE Analysis of Dimension '{dim_name}'"
                
            else:
                # Show only current distribution (default behavior)
                x_min, x_max = _get_distribution_range(dist_name, para1, para2)
                x = np.linspace(x_min, x_max, 500)
                y = _calculate_pdf(x, dist_name, para1, para2)
                
                fig.add_trace(go.Scatter(
                    x=x, y=y, 
                    mode="lines", 
                    name=f"{dim_name} ({dist_name})",
                    line=dict(width=3, color="blue"),
                    hovertemplate="<b>Value:</b> %{x:.4f}<br><b>Density:</b> %{y:.4f}<br><b>CDF:</b> %{customdata:.4f}<extra></extra>",
                    customdata=_calculate_cdf(x, dist_name, para1, para2)
                ))
                
                stats_text = _format_statistics(dist_name, para1, para2)
                title_text = f"Probability Density Function of Dimension '{dim_name}'"
            
            fig.update_layout(
                title=title_text,
                margin=dict(l=40, r=20, t=60, b=40),
                xaxis_title="Value",
                yaxis_title="Probability Density",
                height=450,
                width=600,
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                title_font_size=14,
                showlegend=bayes_applied or mle_applied  # Show legend when showing multiple elements
            )
            
            # Add grid lines
            fig.update_xaxes(
                showgrid=True, 
                gridwidth=0.8, 
                gridcolor='rgba(180,180,180,0.4)',
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='rgba(100,100,100,0.6)'
            )
            fig.update_yaxes(
                showgrid=True, 
                gridwidth=0.8, 
                gridcolor='rgba(180,180,180,0.4)',
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='rgba(100,100,100,0.6)'
            )

            return fig, stats_text

        except Exception as e:
            return go.Figure(), f"Error calculating distribution: {str(e)}"