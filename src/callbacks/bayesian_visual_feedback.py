# src/callbacks/bayesian_visual_feedback.py

from dash import Input, Output, MATCH, html, callback_context
import dash_bootstrap_components as dbc
from src.stores.global_store import dimensions_store

def register_bayesian_visual_feedback_callback(app):
    @app.callback(
        Output({"type": "dim-bayes-display", "index": MATCH}, "children"),
        Output({"type": "dim-bayes", "index": MATCH}, "style"),
        Input({"type": "dim-bayes-status", "index": MATCH}, "data"),
        Input({"type": "dim-bayes-error", "index": MATCH}, "data"),
        prevent_initial_call=True
    )
    def update_bayesian_visual_feedback(bayes_success, error_message):
        # Get the dimension index from callback context
        if callback_context.triggered:
            prop_id = callback_context.triggered[0]['prop_id']
            if '"index":' in prop_id:
                index = prop_id.split('"index":')[1].split(',')[0]
            else:
                index = "0"
        else:
            index = "0"
            
        # Get iteration count from store
        dim_key = f"dim_{index}"
        stored_dim = dimensions_store.get(dim_key, {})
        bayes_iterations = stored_dim.get('bayes_iterations', 0)
        
        # Only show error state if there's an actual error message (not empty string)
        if error_message and error_message.strip():
            # Show error state - red background
            return [
                html.Span("⚠", style={"color": "white", "fontWeight": "bold", "marginRight": "5px"}),
                "Error"
            ], {
                "border": "2px solid #dc3545", 
                "backgroundColor": "#dc3545",
                "color": "white",
                "padding": "5px", 
                "textAlign": "center",
                "borderRadius": "4px",
                "transition": "all 0.3s ease",
                "fontWeight": "bold"
            }
        elif bayes_success and bayes_iterations > 0:
            # Bayesian update was successful - blue background with iteration count
            iteration_text = f"{bayes_iterations} Bayes Applied" if bayes_iterations > 1 else "1 Bayes Applied"
            return [
                html.Span("⚡", style={"color": "white", "fontWeight": "bold", "marginRight": "5px"}),
                iteration_text
            ], {
                "border": "2px solid #007bff", 
                "backgroundColor": "#007bff",
                "color": "white",
                "padding": "5px", 
                "textAlign": "center",
                "borderRadius": "4px",
                "transition": "all 0.3s ease",
                "fontWeight": "bold"
            }
        else:
            # Default state - normal appearance
            return "Bayes Data", {
                "border": "1px dashed gray", 
                "padding": "5px", 
                "textAlign": "center",
                "transition": "all 0.3s ease"
            }
    
    @app.callback(
        Output({"type": "dim-error-alert", "index": MATCH}, "is_open"),
        Output({"type": "dim-error-alert", "index": MATCH}, "children"),
        Input({"type": "dim-bayes-error", "index": MATCH}, "data"),
        prevent_initial_call=True
    )
    def show_error_alert(error_message):
        # Only show alert if there's an actual error message (not empty string)
        if error_message and error_message.strip() and error_message != "":
            return True, [
                html.Strong("Bayesian Update Error: "),
                error_message
            ]
        return False, ""