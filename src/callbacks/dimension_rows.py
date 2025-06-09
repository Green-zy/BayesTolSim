# src/callbacks/dimension_rows.py

from dash import Input, Output, State, ctx
from src.components.dimension_row import generate_dimension_row
from src.stores.global_store import dimensions_store


def register_dim_row_callbacks(app):
    @app.callback(
        Output("dimension-form-container", "children"),
        Output("dim-count", "data"),
        Output("select-dim-to-view", "options"),  
        Input("add-dim", "n_clicks"),
        Input("remove-dim", "n_clicks"),
        State("dim-count", "data"),
        State("dimension-form-container", "children")
    )
    def update_dimension_rows(add_clicks, remove_clicks, count, children):
        children = children or []
        count = count or 0

        if ctx.triggered_id == "add-dim":
            children.append(generate_dimension_row(count))
            dimensions_store[f"dim_{count}"] = {
                "name": f"Dim {count}",  
                "dist": None,
                "para1": None,
                "para2": None,
            }
            count += 1

        elif ctx.triggered_id == "remove-dim" and count > 0:
            count -= 1
            children = children[:-1]
            dimensions_store.pop(f"dim_{count}", None)

        dropdown_options = [
            {"label": dimensions_store[k]["name"], "value": k}
            for k in dimensions_store
        ]

        return children, count, dropdown_options

