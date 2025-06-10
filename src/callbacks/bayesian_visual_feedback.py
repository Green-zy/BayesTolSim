# src/callbacks/bayesian_visual_feedback.py

from dash import Input, Output, MATCH, html
import dash_bootstrap_components as dbc

def register_bayesian_visual_feedback_callback(app):
    @app.callback(
        Output({"type": "dim-bayes-display", "index": MATCH}, "children"),
        Output({"type": "dim-bayes", "index": MATCH}, "style"),
        Input({"type": "dim-bayes-status", "index": MATCH}, "data"),
        Input({"type": "dim-bayes-error", "index": MATCH}, "data"),
        prevent_initial_call=True
    )
    def update_bayesian_visual_feedback(bayes_success, error_message):
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
        elif bayes_success:
            # Bayesian update was successful - blue background with Bayesian icon
            return [
                html.Span("⚡", style={"color": "white", "fontWeight": "bold", "marginRight": "5px"}),
                "Bayes Applied"
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