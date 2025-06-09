# src/callbacks/param_display.py

from dash import Input, Output, State, callback_context, ALL, no_update
import dash
import numexpr as ne
from src.stores.global_store import dimensions_store


def register_param_display_callback(app):
    @app.callback(
        Output("dummy-output", "children", allow_duplicate=True),  # Dummy output for triggering storage updates
        Input({"type": "dim-name", "index": ALL}, "value"),
        Input({"type": "dim-dist", "index": ALL}, "value"),
        Input({"type": "dim-para1", "index": ALL}, "value"),
        Input({"type": "dim-para2", "index": ALL}, "value"),
        prevent_initial_call=True
    )
    def store_dimension_data(names, dists, values1, values2):
        """Update dimension data in global storage"""
        for i in range(max(len(names), len(dists), len(values1), len(values2))):
            dim_key = f"dim_{i}"
            
            # Ensure dimension exists
            if dim_key not in dimensions_store:
                dimensions_store[dim_key] = {
                    "name": f"Dim {i}",
                    "dist": None,
                    "para1": None,
                    "para2": None
                }
            
            # Update name
            if i < len(names) and names[i]:
                dimensions_store[dim_key]["name"] = names[i]
            
            # Update distribution type
            if i < len(dists) and dists[i]:
                dimensions_store[dim_key]["dist"] = dists[i]
            
            # Update parameters (store directly if numeric, otherwise keep as string)
            if i < len(values1) and values1[i] is not None and values1[i] != "":
                if isinstance(values1[i], (int, float)):
                    dimensions_store[dim_key]["para1"] = values1[i]
                else:
                    # Try to evaluate expression
                    try:
                        evaluated = float(ne.evaluate(str(values1[i])))
                        dimensions_store[dim_key]["para1"] = evaluated
                    except:
                        dimensions_store[dim_key]["para1"] = values1[i]
            
            if i < len(values2) and values2[i] is not None and values2[i] != "":
                if isinstance(values2[i], (int, float)):
                    dimensions_store[dim_key]["para2"] = values2[i]
                else:
                    # Try to evaluate expression
                    try:
                        evaluated = float(ne.evaluate(str(values2[i])))
                        dimensions_store[dim_key]["para2"] = evaluated
                    except:
                        dimensions_store[dim_key]["para2"] = values2[i]

        return no_update