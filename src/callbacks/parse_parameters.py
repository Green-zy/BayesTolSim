# src/callbacks/parse_parameters.py

from dash import Input, Output, State, MATCH, ctx, no_update
import numexpr as ne
from src.stores.global_store import dimensions_store

def register_param_parse_callback(app):
    @app.callback(
        Output({"type": "dim-para1", "index": MATCH}, "value"),
        Output({"type": "dim-para2", "index": MATCH}, "value"),
        Input({"type": "dim-para1", "index": MATCH}, "n_submit"),
        Input({"type": "dim-para2", "index": MATCH}, "n_submit"),
        State({"type": "dim-para1", "index": MATCH}, "value"),
        State({"type": "dim-para2", "index": MATCH}, "value"),
        prevent_initial_call=True
    )
    def update_inputs(n1, n2, val1, val2):
        triggered_id = ctx.triggered_id
        if triggered_id is None:
            return no_update, no_update
            
        index = triggered_id["index"]
        dim_key = f"dim_{index}"
        
        # Ensure dimension exists in store
        if dim_key not in dimensions_store:
            dimensions_store[dim_key] = {"name": f"Dim {index}", "dist": None, "para1": None, "para2": None}
        
        # Process parameter 1 - convert to numerical value and display it
        val1_eval = val1
        if val1 is not None and val1 != "":
            try:
                val1_eval = float(ne.evaluate(str(val1)))
                dimensions_store[dim_key]["para1"] = val1_eval
                # Format the displayed value to show 6 decimal places for precision
                val1_eval = f"{val1_eval:.6f}"
            except Exception as e:
                val1_eval = val1  # Keep original value if calculation fails
                
        # Process parameter 2 - convert to numerical value and display it        
        val2_eval = val2
        if val2 is not None and val2 != "":
            try:
                val2_eval = float(ne.evaluate(str(val2)))
                dimensions_store[dim_key]["para2"] = val2_eval
                # Format the displayed value to show 6 decimal places for precision
                val2_eval = f"{val2_eval:.6f}"
            except Exception as e:
                val2_eval = val2  # Keep original value if calculation fails
            
        return val1_eval, val2_eval