# src/callbacks/param_placeholder.py

from dash import Input, Output, MATCH

def register_param_placeholder_callback(app):
    @app.callback(
        Output({"type": "dim-para1", "index": MATCH}, "placeholder"),
        Output({"type": "dim-para2", "index": MATCH}, "placeholder"),
        Input({"type": "dim-dist", "index": MATCH}, "value"),
        prevent_initial_call=True
    )
    def update_param_placeholders(distribution):
        if distribution == "normal":
            return "μ (mu)", "σ (sigma)"
        elif distribution == "lognormal":
            return "μ (location)", "σ (shape)"
        elif distribution == "gamma":
            return "k (shape)", "θ (scale)"
        elif distribution == "uniform":
            return "a (lower)", "b (upper)"
        else:
            return "Para1", "Para2"