# src/callbacks/tolerance_to_params.py

from dash import Input, Output, State, MATCH
import numpy as np

def register_tolerance_to_params_callback(app):
    @app.callback(
        Output({"type": "dim-para1", "index": MATCH}, "value", allow_duplicate=True),
        Output({"type": "dim-para2", "index": MATCH}, "value", allow_duplicate=True),
        Input({"type": "dim-dist", "index": MATCH}, "value"),
        State({"type": "dim-nominal", "index": MATCH}, "value"),
        State({"type": "dim-tol-upper", "index": MATCH}, "value"),
        State({"type": "dim-tol-lower", "index": MATCH}, "value"),
        prevent_initial_call=True
    )
    def calculate_default_params(distribution, nominal, upper_tol, lower_tol):
        # Always recalculate when distribution changes
        # Need all tolerance inputs to calculate defaults
        if nominal is None or upper_tol is None or lower_tol is None or distribution is None:
            return "", ""
            
        # Ensure numeric values
        try:
            nominal = float(nominal)
            upper_tol = float(upper_tol)
            lower_tol = float(lower_tol)
        except (ValueError, TypeError):
            return "", ""
            
        # Calculate distribution parameters based on tolerance analysis principles
        tolerance_range = upper_tol - lower_tol
        
        if distribution == "normal":
            # Normal: μ = nominal, σ = tolerance_range/6 (6-sigma rule)
            mu = nominal
            sigma = tolerance_range / 6
            return f"{mu:.6f}", f"{sigma:.6f}"
            
        elif distribution == "uniform":
            # Uniform: a = nominal + lower_tolerance, b = nominal + upper_tolerance
            a = nominal + lower_tol
            b = nominal + upper_tol
            return f"{a:.6f}", f"{b:.6f}"
            
        elif distribution == "lognormal":
            # Lognormal: Set so that exp(μ + σ²/2) ≈ nominal
            # Use method of moments approximation
            lower_bound = nominal + lower_tol
            upper_bound = nominal + upper_tol
            
            if lower_bound <= 0:
                # Shift to ensure positive values
                shift = abs(lower_bound) + 0.01
                lower_bound += shift
                upper_bound += shift
                nominal += shift
                
            # Approximate lognormal parameters
            mean_approx = nominal
            std_approx = tolerance_range / 6
            
            if mean_approx > 0 and std_approx > 0:
                cv = std_approx / mean_approx  # coefficient of variation
                sigma_ln = np.sqrt(np.log(1 + cv**2))
                mu_ln = np.log(mean_approx) - 0.5 * sigma_ln**2
                return f"{mu_ln:.6f}", f"{sigma_ln:.6f}"
            else:
                return "0.000000", "0.100000"
                
        elif distribution == "gamma":
            # Gamma: Use method of moments
            # Set mean ≈ nominal, shape parameters based on tolerance
            target_mean = nominal if nominal > 0 else 1.0
            target_std = tolerance_range / 6
            
            if target_std > 0 and target_mean > 0:
                # Method of moments: shape = (mean/std)², scale = std²/mean
                shape = (target_mean / target_std) ** 2
                scale = target_std ** 2 / target_mean
                return f"{shape:.6f}", f"{scale:.6f}"
            else:
                return "1.000000", "1.000000"
                
        else:
            return "", ""