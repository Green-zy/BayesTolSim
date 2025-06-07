# src/callbacks/dimension_rows.py

from dash import Input, Output, State, ctx
from src.components.dimension_row import generate_dimension_row

def register_dim_row_callbacks(app):
    @app.callback(
        Output("dimension-form-container", "children"),
        Output("dim-count", "data"),
        Input("add-dim", "n_clicks"),
        Input("remove-dim", "n_clicks"),
        State("dim-count", "data"),
        State("dimension-form-container", "children")
    )
    def update_dimension_rows(add_clicks, remove_clicks, count, children):
        if ctx.triggered_id == "add-dim":
            children = children or []
            children.append(generate_dimension_row(count))
            count += 1
        elif ctx.triggered_id == "remove-dim" and count > 0:
            children = (children or [])[:-1]
            count -= 1
        return children, count
