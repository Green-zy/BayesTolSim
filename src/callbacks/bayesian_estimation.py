# src/callbacks/bayesian_estimation.py

from dash import Input, Output, State, MATCH, callback_context, no_update
import pandas as pd
import numpy as np
import base64
import io
from src.stores.global_store import dimensions_store
from src.utils.bayesian_calculations import (
    calculate_prior_parameters, 
    bayesian_update_normal,
    bayesian_update_gamma, 
    bayesian_update_lognormal,
    bayesian_update_uniform,
    calculate_likelihood_params
)

def register_bayesian_callback(app):
    @app.callback(
        Output({"type": "dim-para1", "index": MATCH}, "value", allow_duplicate=True),
        Output({"type": "dim-para2", "index": MATCH}, "value", allow_duplicate=True),
        Output({"type": "dim-bayes-status", "index": MATCH}, "data"),
        Output({"type": "dim-bayes-error", "index": MATCH}, "data"),
        Input({"type": "dim-bayes", "index": MATCH}, "contents"),
        State({"type": "dim-bayes", "index": MATCH}, "filename"),
        State({"type": "dim-name", "index": MATCH}, "value"),
        State({"type": "dim-dist", "index": MATCH}, "value"),
        State({"type": "dim-nominal", "index": MATCH}, "value"),
        State({"type": "dim-tol-upper", "index": MATCH}, "value"),
        State({"type": "dim-tol-lower", "index": MATCH}, "value"),
        State({"type": "dim-mle-status", "index": MATCH}, "data"),
        prevent_initial_call=True
    )
    def process_bayesian_upload(contents, filename, dim_name, distribution, nominal, 
                              upper_tol, lower_tol, mle_status):
        
        # Check if MLE was already applied
        if mle_status:
            error_msg = "Error: MLE has already been applied to this dimension. Please remove and re-create the dimension to use Bayesian updating."
            return "", "", False, error_msg
            
        # Check if all required tolerance inputs are provided
        if nominal is None or upper_tol is None or lower_tol is None:
            error_msg = "Error: Please provide nominal, upper tolerance, and lower tolerance values before uploading Bayesian data."
            return "", "", False, error_msg
            
        if contents is None or distribution is None or dim_name is None:
            return no_update, no_update, no_update, no_update
            
        try:
            # Parse the uploaded file
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            
            # Read CSV
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            else:
                error_msg = f"Invalid file format: {filename}. Please upload a CSV file."
                return "", "", False, error_msg
                
            print(f"CSV loaded successfully. Columns: {list(df.columns)}")
            print(f"Looking for dimension: '{dim_name}' in distribution: '{distribution}'")
                
            # Find the column that matches the dimension name
            column_name = None
            for col in df.columns:
                if col.strip().lower() == dim_name.strip().lower():
                    column_name = col
                    break
                    
            if column_name is None:
                # If exact match not found, try partial match
                for col in df.columns:
                    if dim_name.strip().lower() in col.strip().lower() or col.strip().lower() in dim_name.strip().lower():
                        column_name = col
                        break
                        
            if column_name is None:
                error_msg = f"No matching column found for dimension '{dim_name}' in the uploaded data."
                return "", "", False, error_msg
                
            print(f"Found matching column: '{column_name}'")
                
            # Extract data points
            data = df[column_name].dropna().values
            print(f"Data points: {len(data)}, Range: [{np.min(data):.3f}, {np.max(data):.3f}]")
            
            if len(data) < 2:
                error_msg = "Insufficient data points for Bayesian updating. Please provide at least 2 data points."
                return "", "", False, error_msg
                
            # Calculate prior parameters from tolerances
            prior_params, error = calculate_prior_parameters(distribution, nominal, upper_tol, lower_tol)
            if prior_params is None:
                error_msg = f"Error calculating prior parameters: {error or 'Invalid tolerance values'}"
                return "", "", False, error_msg
                
            # Perform Bayesian updating
            para1_post, para2_post = perform_bayesian_update(data, distribution, prior_params)
            
            if para1_post is not None and para2_post is not None:
                # Store additional information for plotting
                index = callback_context.triggered[0]['prop_id'].split('"index":')[1].split(',')[0]
                dim_key = f"dim_{index}"
                
                # Calculate likelihood parameters for plotting
                like_para1, like_para2 = calculate_likelihood_params(data, distribution)
                
                # Store all parameters in dimensions store
                if dim_key not in dimensions_store:
                    dimensions_store[dim_key] = {}
                    
                dimensions_store[dim_key].update({
                    'bayes_applied': True,
                    'prior_para1': prior_params.get('mu_prior', prior_params.get('k_prior', prior_params.get('a_prior'))),
                    'prior_para2': prior_params.get('sigma_prior', prior_params.get('theta_prior', prior_params.get('b_prior'))),
                    'likelihood_para1': like_para1,
                    'likelihood_para2': like_para2,
                    'posterior_para1': para1_post,
                    'posterior_para2': para2_post,
                    'prior_params_full': prior_params,
                    'data': data.tolist()  # Store data for plotting
                })
                
                print(f"Bayesian updating successful: para1={para1_post:.6f}, para2={para2_post:.6f}")
                return f"{para1_post:.6f}", f"{para2_post:.6f}", True, ""
            else:
                error_msg = "Bayesian updating calculation failed. Please check your data and distribution."
                return "", "", False, error_msg
                
        except Exception as e:
            error_msg = f"Error processing Bayesian data: {str(e)}"
            print(f"Bayesian upload processing error: {e}")
            import traceback
            traceback.print_exc()
            return "", "", False, error_msg

def perform_bayesian_update(data, distribution, prior_params):
    """Perform Bayesian updating based on distribution type"""
    try:
        if distribution == "normal":
            return bayesian_update_normal(data, prior_params)
        elif distribution == "gamma":
            return bayesian_update_gamma(data, prior_params)
        elif distribution == "lognormal":
            return bayesian_update_lognormal(data, prior_params)
        elif distribution == "uniform":
            return bayesian_update_uniform(data, prior_params)
        else:
            print(f"Unsupported distribution for Bayesian updating: {distribution}")
            return None, None
    except Exception as e:
        print(f"Error in Bayesian updating for {distribution}: {e}")
        import traceback
        traceback.print_exc()
        return None, None