# src/callbacks/final_dimension_simulation.py

from dash import Input, Output, State, ALL, callback_context, html, dcc
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.stats import norm, lognorm, gamma, uniform
from src.stores.global_store import dimensions_store
import warnings
warnings.filterwarnings('ignore')

def register_final_dimension_simulation_callback(app):
    
    # Store simulation data for hover handling
    app._final_simulation_data = {}
    
    @app.callback(
        Output("final-dimension-content", "children"),
        Input("run-simulation-btn", "n_clicks"),
        Input({"type": "dim-name", "index": ALL}, "value"),
        Input({"type": "dim-dist", "index": ALL}, "value"),
        Input({"type": "dim-para1", "index": ALL}, "value"),
        Input({"type": "dim-para2", "index": ALL}, "value"),
        Input({"type": "dim-dir", "index": ALL}, "value"),
        State("num-samples-input", "value"),
        State("final-dim-tol-upper", "value"),  # Added final dimension tolerances
        State("final-dim-tol-lower", "value"),  # Added final dimension tolerances
        prevent_initial_call=True
    )
    def update_final_dimension_simulation(n_clicks, names, dists, para1s, para2s, dirs, num_samples, final_upper_tol, final_lower_tol):
        # Check if dimensions are properly set
        if not names or all(v in [None, "", []] for v in names):
            return [
                html.Div(
                    "Please set dimension chain first.",
                    style={
                        "textAlign": "center",
                        "color": "gray",
                        "fontSize": "14px",
                        "padding": "100px 20px",
                        "height": "300px",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center"
                    }
                )
            ]
        
        # Check if simulation button was clicked
        if not n_clicks:
            return [
                html.Div(
                    "Click 'Run Simulation' to generate final dimension distribution.",
                    style={
                        "textAlign": "center",
                        "color": "gray",
                        "fontSize": "14px",
                        "padding": "100px 20px",
                        "height": "300px",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center"
                    }
                )
            ]
        
        # Validate number of samples
        if num_samples is None or num_samples <= 0:
            return [
                html.Div(
                    "Please enter a valid number of samples (positive integer).",
                    style={
                        "textAlign": "center",
                        "color": "red",
                        "fontSize": "14px",
                        "padding": "100px 20px",
                        "height": "300px",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center"
                    }
                )
            ]
        
        try:
            # Run Monte Carlo simulation
            final_samples = run_monte_carlo_simulation(names, dists, para1s, para2s, dirs, num_samples)
            
            if final_samples is None:
                return [
                    html.Div(
                        "Error: Unable to run simulation. Please check dimension parameters.",
                        style={
                            "textAlign": "center",
                            "color": "red",
                            "fontSize": "14px",
                            "padding": "100px 20px",
                            "height": "300px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center"
                        }
                    )
                ]
            
            # Create plot and statistics
            fig, x_data, y_data, cdf_data = create_final_dimension_plot_with_data(final_samples)
            stats_text = calculate_final_dimension_statistics(final_samples, num_samples, final_upper_tol, final_lower_tol, names, dirs)
            
            # Store data for hover handling
            app._final_simulation_data = {
                'x_data': x_data,
                'y_data': y_data,
                'cdf_data': cdf_data
            }
            
            return [
                dcc.Graph(
                    id="final-dimension-plot",
                    figure=fig,
                    style={"height": "400px"}
                ),
                html.Pre(
                    stats_text,
                    style={"whiteSpace": "pre-wrap", "fontSize": "0.9rem", "marginTop": "10px"}
                )
            ]
            
        except Exception as e:
            return [
                html.Div(
                    f"Simulation Error: {str(e)}",
                    style={
                        "textAlign": "center",
                        "color": "red",
                        "fontSize": "14px",
                        "padding": "100px 20px",
                        "height": "300px",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center"
                    }
                )
            ]

    @app.callback(
        Output("final-dimension-plot", "figure"),
        Input("final-dimension-plot", "hoverData"),
        prevent_initial_call=True
    )
    def handle_plot_hover(hover_data):
        """Handle hover on the final dimension plot"""
        if not hover_data or not hasattr(app, '_final_simulation_data'):
            return go.Figure()  # Return empty figure if no data
            
        try:
            # Get stored simulation data
            stored_data = app._final_simulation_data
            x_data = np.array(stored_data['x_data'])
            y_data = np.array(stored_data['y_data'])
            cdf_data = stored_data['cdf_data']
            
            # Get hovered point
            hovered_x = float(hover_data['points'][0]['x'])
            
            # Find indices for fill area (from left edge to hovered point)
            fill_indices = x_data <= hovered_x
            x_fill = x_data[fill_indices]
            y_fill = y_data[fill_indices]
            
            # Create new figure
            fig = go.Figure()
            
            # Add red fill area under the curve
            if len(x_fill) > 0:
                fig.add_trace(go.Scatter(
                    x=np.concatenate([x_fill, [x_fill[-1]], [x_fill[0]]]),
                    y=np.concatenate([y_fill, [0], [0]]),
                    fill="toself",
                    fillcolor="rgba(255, 0, 0, 0.5)",  # Red with 50% transparency
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo="skip"
                ))
            
            # Add main purple curve
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                mode="lines",
                name="Final Dimension Distribution",
                line=dict(width=3, color="purple"),
                hovertemplate="<b>Value:</b> %{x:.4f}<br><b>Density:</b> %{y:.4f}<br><b>CDF:</b> %{customdata:.4f}<extra></extra>",
                customdata=cdf_data
            ))
            
            # Add hover point marker
            hovered_y = np.interp(hovered_x, x_data, y_data)
            hovered_cdf = np.interp(hovered_x, x_data, cdf_data) if cdf_data else 0
            
            fig.add_trace(go.Scatter(
                x=[hovered_x],
                y=[hovered_y],
                mode="markers",
                marker=dict(size=10, color="orange", symbol="circle", line=dict(width=2, color="white")),
                showlegend=False,
                hovertemplate=f"<b>Hovered Point</b><br>Value: {hovered_x:.4f}<br>Density: {hovered_y:.4f}<br>CDF: {hovered_cdf:.4f}<extra></extra>"
            ))
            
            # Update layout
            fig.update_layout(
                title="Monte Carlo Simulation - Final Dimension Distribution",
                margin=dict(l=40, r=20, t=60, b=40),
                xaxis_title="Final Dimension Value",
                yaxis_title="Probability Density",
                height=400,
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                title_font_size=14,
                showlegend=False
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
            
            return fig
            
        except Exception as e:
            print(f"Hover handler error: {e}")
            import traceback
            traceback.print_exc()
            # Return original plot without hover effects
            return create_original_plot_from_stored_data(app._final_simulation_data)

def run_monte_carlo_simulation(names, dists, para1s, para2s, dirs, num_samples):
    """Run Monte Carlo simulation for final dimension chain"""
    try:
        # Generate samples for each dimension
        all_samples = []
        
        for i in range(len(names)):
            if names[i] is None or dists[i] is None or para1s[i] is None or para2s[i] is None:
                continue
                
            # Get parameters from dimensions store or use input values
            dim_key = f"dim_{i}"
            dim_data = dimensions_store.get(dim_key, {})
            
            # Use posterior parameters if Bayesian was applied, else use current parameters
            if dim_data.get("bayes_applied", False):
                para1 = dim_data.get("posterior_para1", para1s[i])
                para2 = dim_data.get("posterior_para2", para2s[i])
            elif dim_data.get("mle_applied", False):
                para1 = dim_data.get("mle_para1", para1s[i])
                para2 = dim_data.get("mle_para2", para2s[i])
            else:
                para1 = para1s[i]
                para2 = para2s[i]
            
            # Convert to float if needed
            try:
                para1 = float(para1)
                para2 = float(para2)
            except:
                continue
            
            # Generate samples based on distribution
            samples = generate_distribution_samples(dists[i], para1, para2, num_samples)
            if samples is None:
                continue
                
            # Apply direction (+ or -)
            direction = dirs[i] if i < len(dirs) else "+"
            if direction == "-":
                samples = -samples
                
            all_samples.append(samples)
        
        if not all_samples:
            return None
            
        # Sum all dimension samples to get final dimension
        final_samples = np.sum(all_samples, axis=0)
        return final_samples
        
    except Exception as e:
        print(f"Monte Carlo simulation error: {e}")
        return None

def generate_distribution_samples(dist_type, para1, para2, num_samples):
    """Generate samples from specified distribution"""
    try:
        if dist_type == "normal":
            if para2 <= 0:
                return None
            return np.random.normal(para1, para2, num_samples)
            
        elif dist_type == "lognormal":
            if para2 <= 0:
                return None
            return np.random.lognormal(para1, para2, num_samples)
            
        elif dist_type == "gamma":
            if para1 <= 0 or para2 <= 0:
                return None
            return np.random.gamma(para1, para2, num_samples)
            
        elif dist_type == "uniform":
            if para2 <= para1:
                return None
            return np.random.uniform(para1, para2, num_samples)
            
        else:
            return None
            
    except Exception as e:
        print(f"Sample generation error for {dist_type}: {e}")
        return None

def create_final_dimension_plot_with_data(final_samples):
    """Create the final dimension distribution plot and return data"""
    try:
        # Calculate histogram for the samples
        n_bins = min(50, max(10, len(final_samples) // 100))
        counts, bin_edges = np.histogram(final_samples, bins=n_bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_widths = bin_edges[1:] - bin_edges[:-1]
        total_area = np.sum(counts * bin_widths)
        densities = counts / total_area
        
        # Create x range for smooth curve
        x_min, x_max = np.min(final_samples), np.max(final_samples)
        x_range = x_max - x_min
        x_min -= x_range * 0.1
        x_max += x_range * 0.1
        x_smooth = np.linspace(x_min, x_max, 500)
        
        # Fit kernel density estimation for smooth curve
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(final_samples)
        y_smooth = kde(x_smooth)
        
        # Calculate CDF for hover information
        cdf_values = []
        for x_val in x_smooth:
            cdf_val = np.sum(final_samples <= x_val) / len(final_samples)
            cdf_values.append(cdf_val)
        
        # Create figure
        fig = go.Figure()
        
        # Add the purple curve with hover information
        fig.add_trace(go.Scatter(
            x=x_smooth,
            y=y_smooth,
            mode="lines",
            name="Final Dimension Distribution",
            line=dict(width=3, color="purple"),
            hovertemplate="<b>Value:</b> %{x:.4f}<br><b>Density:</b> %{y:.4f}<br><b>CDF:</b> %{customdata:.4f}<extra></extra>",
            customdata=cdf_values
        ))
        
        fig.update_layout(
            title="Monte Carlo Simulation - Final Dimension Distribution",
            margin=dict(l=40, r=20, t=60, b=40),
            xaxis_title="Final Dimension Value",
            yaxis_title="Probability Density",
            height=400,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=12),
            title_font_size=14,
            showlegend=False
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
        
        return fig, x_smooth.tolist(), y_smooth.tolist(), cdf_values
        
    except Exception as e:
        print(f"Plot creation error: {e}")
        # Return empty figure with error message
        fig = go.Figure()
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="white",
            margin=dict(l=40, r=40, t=40, b=40),
            height=400
        )
        fig.add_annotation(
            text=f"Error creating plot: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="red"),
            align="center"
        )
        return fig, [], [], []

def create_original_plot_from_stored_data(stored_data):
    """Create original plot from stored data"""
    try:
        x_data = stored_data['x_data']
        y_data = stored_data['y_data']
        cdf_data = stored_data['cdf_data']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode="lines",
            name="Final Dimension Distribution",
            line=dict(width=3, color="purple"),
            hovertemplate="<b>Value:</b> %{x:.4f}<br><b>Density:</b> %{y:.4f}<br><b>CDF:</b> %{customdata:.4f}<extra></extra>",
            customdata=cdf_data
        ))
        
        fig.update_layout(
            title="Monte Carlo Simulation - Final Dimension Distribution",
            margin=dict(l=40, r=20, t=60, b=40),
            xaxis_title="Final Dimension Value",
            yaxis_title="Probability Density",
            height=400,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=12),
            title_font_size=14,
            showlegend=False
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
        
        return fig
        
    except Exception as e:
        print(f"Error creating original plot: {e}")
        return go.Figure()

def calculate_final_dimension_statistics(final_samples, num_samples, final_upper_tol=None, final_lower_tol=None, names=None, dirs=None):
    """Calculate and format statistics for final dimension"""
    try:
        mean_val = np.mean(final_samples)
        std_val = np.std(final_samples, ddof=1)
        min_val = np.min(final_samples)
        max_val = np.max(final_samples)
        p5 = np.percentile(final_samples, 5)
        p95 = np.percentile(final_samples, 95)
        median_val = np.median(final_samples)
        
        stats_text = f"""=== MONTE CARLO SIMULATION RESULTS ===
Sample Size: {num_samples:,}
Mean: {mean_val:.4f}
Std Dev: {std_val:.4f}
Median: {median_val:.4f}
Min: {min_val:.4f}
Max: {max_val:.4f}
5th Percentile: {p5:.4f}
95th Percentile: {p95:.4f}
Range (95%): {p95 - p5:.4f}"""

        # Add process capability indices if tolerances are provided
        if final_upper_tol is not None and final_lower_tol is not None:
            try:
                upper_tol_val = float(final_upper_tol)
                lower_tol_val = float(final_lower_tol)
                
                # Calculate final dimension nominal by summing individual dimension nominals with directions
                final_nominal = 0.0
                
                if names and dirs:
                    for i in range(len(names)):
                        if names[i] is not None:
                            dim_key = f"dim_{i}"
                            dim_data = dimensions_store.get(dim_key, {})
                            
                            # Get nominal value from store
                            nominal = dim_data.get('nominal')
                            if nominal is not None:
                                try:
                                    nominal_val = float(nominal)
                                    # Get direction from dirs parameter
                                    direction = dirs[i] if i < len(dirs) and dirs[i] is not None else "+"
                                    
                                    if direction == '-':
                                        final_nominal -= nominal_val
                                    else:
                                        final_nominal += nominal_val
                                except (ValueError, TypeError):
                                    continue
                
                # Calculate specification limits
                USL = final_nominal + upper_tol_val  # Upper Specification Limit
                LSL = final_nominal + lower_tol_val  # Lower Specification Limit
                
                # Calculate process capability indices
                if std_val > 0:
                    # Cp = (USL - LSL) / (6 * sigma)
                    Cp = (USL - LSL) / (6 * std_val)
                    
                    # Cpk = min((USL - mean)/(3*sigma), (mean - LSL)/(3*sigma))
                    Cpu = (USL - mean_val) / (3 * std_val)  # Upper capability
                    Cpl = (mean_val - LSL) / (3 * std_val)  # Lower capability
                    Cpk = min(Cpu, Cpl)
                    
                    # Add capability indices to the statistics text
                    stats_text += f"\nCp: {Cp:.3f}\nCpk: {Cpk:.3f}"
                else:
                    stats_text += f"\nCp: Cannot calculate (std=0)\nCpk: Cannot calculate (std=0)"
                    
            except (ValueError, TypeError):
                # If there's an error converting tolerances to float
                stats_text += f"\nCp: Error in tolerance values\nCpk: Error in tolerance values"
        else:
            # No tolerances provided
            stats_text += f"\nCp: Please set tolerance in final dimension\nCpk: Please set tolerance in final dimension"
        
        return stats_text
        
    except Exception as e:
        return f"Error calculating statistics: {str(e)}"