# src/callbacks/param_display.py

from dash import Input, Output, State, MATCH, html, dcc
import numpy as np

def register_param_display_callback(app):
    @app.callback(
        Output({"type": "dim-params", "index": MATCH}, "children"),
        Input({"type": "dim-dist", "index": MATCH}, "value"),
        State({"type": "dim-nominal", "index": MATCH}, "value"),
        State({"type": "dim-tol", "index": MATCH}, "value"),
        prevent_initial_call=True
    )
    def update_param_fields(dist_type, nominal, tol):
        default_1 = ""
        default_2 = ""

        if dist_type == "normal" and nominal is not None and tol is not None:
            default_1 = nominal
            default_2 = round(tol / 6, 4)

        elif dist_type == "lognormal" and nominal is not None and tol is not None:
            mean = np.log(nominal)
            std = np.log(1 + (tol / nominal) / 6)  # rough estimate
            default_1 = round(mean, 4)
            default_2 = round(std, 4)

        elif dist_type == "beta":
            default_1, default_2 = "", ""
        elif dist_type == "gamma":
            default_1, default_2 = "", ""

        return html.Div([
            dcc.Input(type="number", value=default_1, placeholder="Param 1", className="form-control", style={"width": "48%", "display": "inline-block", "marginRight": "4%"}),
            dcc.Input(type="number", value=default_2, placeholder="Param 2", className="form-control", style={"width": "48%", "display": "inline-block"})
        ])
