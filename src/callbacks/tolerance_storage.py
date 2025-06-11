# src/callbacks/tolerance_storage.py

from dash import Input, Output, State, callback_context, ALL, no_update
from src.stores.global_store import dimensions_store

def register_tolerance_storage_callback(app):
    @app.callback(
        Output("dummy-output", "children", allow_duplicate=True),
        Input({"type": "dim-nominal", "index": ALL}, "value"),
        Input({"type": "dim-tol-upper", "index": ALL}, "value"),
        Input({"type": "dim-tol-lower", "index": ALL}, "value"),
        prevent_initial_call=True
    )
    def store_tolerance_data(nominals, upper_tols, lower_tols):
        """Store tolerance data for process capability calculations"""
        max_len = max(len(nominals), len(upper_tols), len(lower_tols))
        
        for i in range(max_len):
            dim_key = f"dim_{i}"
            
            # Ensure dimension exists
            if dim_key not in dimensions_store:
                dimensions_store[dim_key] = {
                    "name": f"Dim {i}",
                    "dist": None,
                    "para1": None,
                    "para2": None
                }
            
            # Store tolerance values
            if i < len(nominals) and nominals[i] is not None:
                dimensions_store[dim_key]["nominal"] = nominals[i]
            
            if i < len(upper_tols) and upper_tols[i] is not None:
                dimensions_store[dim_key]["upper_tol"] = upper_tols[i]
                
            if i < len(lower_tols) and lower_tols[i] is not None:
                dimensions_store[dim_key]["lower_tol"] = lower_tols[i]

        return no_update