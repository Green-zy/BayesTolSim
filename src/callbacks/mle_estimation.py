# src/callbacks/mle_estimation.py

from dash import Input, Output, State, MATCH, callback_context
import pandas as pd
import numpy as np
from scipy import stats
import base64
import io
from src.stores.global_store import dimensions_store

def register_mle_callback(app):
    @app.callback(
        Output({"type": "dim-para1", "index": MATCH}, "value", allow_duplicate=True),
        Output({"type": "dim-para2", "index": MATCH}, "value", allow_duplicate=True),
        Input({"type": "dim-mle", "index": MATCH}, "contents"),
        State({"type": "dim-mle", "index": MATCH}, "filename"),
        State({"type": "dim-name", "index": MATCH}, "value"),
        State({"type": "dim-dist", "index": MATCH}, "value"),
        prevent_initial_call=True
    )
    def process_mle_upload(contents, filename, dim_name, distribution):
        if contents is None or distribution is None or dim_name is None:
            return "", ""
            
        try:
            # Parse the uploaded file
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            
            # Read CSV
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            else:
                print(f"Invalid file format: {filename}")
                return "", ""
                
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
                print(f"No matching column found for dimension '{dim_name}'")
                return "", ""
                
            print(f"Found matching column: '{column_name}'")
                
            # Extract data points
            data = df[column_name].dropna().values
            print(f"Data points: {len(data)}, Range: [{np.min(data):.3f}, {np.max(data):.3f}]")
            
            if len(data) < 2:
                print("Insufficient data points for MLE")
                return "", ""
                
            # Perform MLE based on distribution type
            para1_mle, para2_mle = calculate_mle_parameters(data, distribution)
            
            if para1_mle is not None and para2_mle is not None:
                print(f"MLE successful: para1={para1_mle:.6f}, para2={para2_mle:.6f}")
                return f"{para1_mle:.6f}", f"{para2_mle:.6f}"
            else:
                print("MLE calculation failed")
                return "", ""
                
        except Exception as e:
            print(f"MLE upload processing error: {e}")
            return "", ""

def calculate_mle_parameters(data, distribution):
    """Calculate MLE parameters for different distributions"""
    try:
        print(f"Calculating MLE for {distribution} with {len(data)} data points")
        
        if distribution == "normal":
            # MLE for normal distribution
            mu_mle = np.mean(data)
            sigma_mle = np.std(data, ddof=0)  # MLE uses population std (ddof=0)
            print(f"Normal MLE: mu={mu_mle:.6f}, sigma={sigma_mle:.6f}")
            return mu_mle, sigma_mle
            
        elif distribution == "lognormal":
            # Ensure all data points are positive
            if np.any(data <= 0):
                print(f"Lognormal MLE failed: data contains non-positive values (min={np.min(data)})")
                return None, None
            
            # For lognormal, we fit to log(data) which should be normal
            log_data = np.log(data)
            mu_mle = np.mean(log_data)
            sigma_mle = np.std(log_data, ddof=0)
            
            # Validate parameters to avoid overflow
            if sigma_mle <= 0 or sigma_mle > 5:  # Limit sigma to reasonable range
                print(f"Lognormal MLE: sigma out of range ({sigma_mle}), using fallback")
                sigma_mle = min(sigma_mle, 1.0)
            
            print(f"Lognormal MLE: mu={mu_mle:.6f}, sigma={sigma_mle:.6f}")
            return mu_mle, sigma_mle
            
        elif distribution == "uniform":
            # MLE for uniform distribution - simple min/max
            a_mle = np.min(data)
            b_mle = np.max(data)
            
            # Add small buffer to ensure proper uniform distribution
            range_buffer = (b_mle - a_mle) * 0.001
            a_mle -= range_buffer
            b_mle += range_buffer
            
            print(f"Uniform MLE: a={a_mle:.6f}, b={b_mle:.6f}")
            return a_mle, b_mle
            
        elif distribution == "gamma":
            # Ensure all data points are positive
            if np.any(data <= 0):
                print(f"Gamma MLE failed: data contains non-positive values (min={np.min(data)})")
                return None, None
            
            # Method of moments for gamma distribution
            sample_mean = np.mean(data)
            sample_var = np.var(data, ddof=0)
            
            if sample_var <= 0:
                print(f"Gamma MLE failed: no variance in data")
                return None, None
                
            # Method of moments: shape = mean²/var, scale = var/mean
            shape_mle = (sample_mean ** 2) / sample_var
            scale_mle = sample_var / sample_mean
            
            # Ensure reasonable parameter ranges
            if shape_mle <= 0 or scale_mle <= 0:
                print(f"Gamma MLE failed: invalid parameters (shape={shape_mle}, scale={scale_mle})")
                return None, None
            
            print(f"Gamma MLE: shape={shape_mle:.6f}, scale={scale_mle:.6f}")
            return shape_mle, scale_mle
            
        else:
            print(f"Unknown distribution: {distribution}")
            return None, None
            
    except Exception as e:
        print(f"MLE parameter calculation error for {distribution}: {e}")
        import traceback
        traceback.print_exc()
        return None, None