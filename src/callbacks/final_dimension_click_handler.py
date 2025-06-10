# src/callbacks/final_dimension_click_handler.py

from dash import Input, Output, State, callback_context
import plotly.graph_objects as go
import numpy as np
from scipy.stats import gaussian_kde

def register_final_dimension_click_callback(app):
    
    # Store the simulation data globally for click handling
    app._simulation_data = {}
    
    @app.callback(
        Output("final-dimension-plot-interactive", "figure"),
        Input("final-dimension-plot-interactive", "clickData"),
        State("final-dimension-plot-interactive", "figure"),
        prevent_initial_call=True
    )
    def handle_curve_click(click_data, current_figure):
        """Handle clicks on the curve to show shadow fill"""
        if not click_data or not current_figure:
            return current_figure
            
        try:
            # Get clicked point
            clicked_x = click_data['points'][0]['x']
            
            # Get current curve data
            curve_trace = None
            for trace in current_figure['data']:
                if trace.get('mode') == 'lines' and trace.get('name') == 'Final Dimension Distribution':
                    curve_trace = trace
                    break
                    
            if not curve_trace:
                return current_figure
                
            x_data = np.array(curve_trace['x'])
            y_data = np.array(curve_trace['y'])
            
            # Find indices for shadow fill (from left edge to clicked point)
            shadow_indices = x_data <= clicked_x
            x_shadow = x_data[shadow_indices]
            y_shadow = y_data[shadow_indices]
            
            # Create new figure with fills
            fig = go.Figure()
            
            # Add red fill area below the curve (from left to clicked point)
            fig.add_trace(go.Scatter(
                x=np.concatenate([x_shadow, [x_shadow[-1]], [x_shadow[0]]]),
                y=np.concatenate([y_shadow, [0], [0]]),
                fill="toself",
                fillcolor="rgba(255, 0, 0, 0.5)",  # Red with 50% transparency
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip",
                name="Area Under Curve"
            ))
            
            # Add pink shadow - offset slightly to the right and down for shadow effect
            x_offset = (np.max(x_data) - np.min(x_data)) * 0.02  # 2% offset
            y_offset = np.max(y_data) * 0.05  # 5% offset
            x_shadow_offset = x_shadow + x_offset
            y_shadow_offset = y_shadow - y_offset
            
            fig.add_trace(go.Scatter(
                x=x_shadow_offset,
                y=y_shadow_offset,
                mode="lines",
                line=dict(width=3, color="rgba(255, 182, 193, 0.5)"),  # Pink shadow line
                showlegend=False,
                hoverinfo="skip",
                name="Shadow"
            ))
            
            # Add main purple curve
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                mode="lines",
                name="Final Dimension Distribution",
                line=dict(width=3, color="purple"),
                hovertemplate="<b>Value:</b> %{x:.4f}<br><b>Density:</b> %{y:.4f}<br><b>CDF:</b> %{customdata:.4f}<extra></extra>",
                customdata=curve_trace.get('customdata', [])
            ))
            
            # Add click point marker
            clicked_y = np.interp(clicked_x, x_data, y_data)
            fig.add_trace(go.Scatter(
                x=[clicked_x],
                y=[clicked_y],
                mode="markers",
                marker=dict(size=8, color="red", symbol="circle"),
                showlegend=False,
                hovertemplate=f"<b>Clicked Point</b><br>Value: {clicked_x:.4f}<br>Density: {clicked_y:.4f}<extra></extra>"
            ))
            
            # Update layout to match original
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
            print(f"Click handler error: {e}")
            return current_figure