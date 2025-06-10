# src/callbacks/mle_visual_feedback.py

from dash import Input, Output, MATCH, html

def register_mle_visual_feedback_callback(app):
    @app.callback(
        Output({"type": "dim-mle-display", "index": MATCH}, "children"),
        Output({"type": "dim-mle", "index": MATCH}, "style"),
        Input({"type": "dim-mle-status", "index": MATCH}, "data"),
        prevent_initial_call=True
    )
    def update_mle_visual_feedback(mle_success):
        if mle_success:
            # MLE was successful - show green background with checkmark
            return [
                html.Span("✓", style={"color": "white", "fontWeight": "bold", "marginRight": "5px"}),
                "MLE Applied"
            ], {
                "border": "2px solid #28a745", 
                "backgroundColor": "#28a745",
                "color": "white",
                "padding": "5px", 
                "textAlign": "center",
                "borderRadius": "4px",
                "transition": "all 0.3s ease",
                "fontWeight": "bold"
            }
        else:
            # Default state - normal appearance
            return "MLE Data", {
                "border": "1px dashed gray", 
                "padding": "5px", 
                "textAlign": "center",
                "transition": "all 0.3s ease"
            }