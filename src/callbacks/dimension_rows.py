# src/callbacks/dimension_rows.py

from dash import Input, Output, State, ctx, ALL
from src.components.dimension_row import generate_dimension_row
from src.stores.global_store import dimensions_store


def register_dim_row_callbacks(app):
    @app.callback(
        Output("dimension-form-container", "children"),
        Output("dim-count", "data"),
        Output("select-dim-to-view", "options"),  
        Input("add-dim", "n_clicks"),
        Input("remove-dim", "n_clicks"),
        Input({"type": "dim-name", "index": ALL}, "value"),  # Added to update dropdown when names change
        State("dim-count", "data"),
        State("dimension-form-container", "children")
    )
    def update_dimension_rows(add_clicks, remove_clicks, names, count, children):
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

        # Update dimension names in store when names change
        if names:
            for i, name in enumerate(names):
                dim_key = f"dim_{i}"
                if dim_key in dimensions_store and name:
                    dimensions_store[dim_key]["name"] = name

        # Create dropdown options using actual dimension names
        dropdown_options = []
        for k in dimensions_store:
            dim_name = dimensions_store[k]["name"]
            if dim_name:  # Only add if name is not empty
                dropdown_options.append({"label": dim_name, "value": k})

        return children, count, dropdown_options