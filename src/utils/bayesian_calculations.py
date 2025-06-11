# src/utils/bayesian_calculations.py

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import warnings

def calculate_prior_parameters(distribution, nominal, upper_tol, lower_tol):
    """Calculate prior distribution parameters from tolerance specifications"""
    print(f"=== FUNCTION START: calculate_prior_parameters ===")
    print(f"Inputs: dist={distribution}, nominal={nominal}, upper={upper_tol}, lower={lower_tol}")
    
    try:
        # Input validation
        if nominal is None or upper_tol is None or lower_tol is None:
            print("ERROR: One or more inputs is None")
            return None, "One or more inputs is None"
        
        print("Converting to float...")
        nominal_f = float(nominal)
        upper_tol_f = float(upper_tol)
        lower_tol_f = float(lower_tol)
        print(f"Converted: nominal={nominal_f}, upper={upper_tol_f}, lower={lower_tol_f}")
        
        tolerance_range = upper_tol_f - lower_tol_f
        print(f"Tolerance range: {tolerance_range}")
        
        if tolerance_range <= 0:
            print("ERROR: Invalid tolerance range")
            return None, "Upper tolerance must be greater than lower tolerance"
        
        print(f"Processing distribution: {distribution}")
        
        if distribution == "normal":
            print("NORMAL DISTRIBUTION PROCESSING")
            mu_prior = nominal_f
            sigma_mu = tolerance_range / 12
            sigma_prior = tolerance_range / 6
            alpha = 2.5
            beta = (alpha - 1) * sigma_prior**2
            
            result_params = {
                'mu_prior': mu_prior,
                'sigma_mu': sigma_mu,
                'alpha': alpha,
                'beta': beta,
                'sigma_prior': sigma_prior
            }
            result = (result_params, None)
            print(f"NORMAL RESULT: {result}")
            return result
            
        elif distribution == "gamma":
            print("GAMMA DISTRIBUTION PROCESSING")
            target_mean = nominal_f if nominal_f > 0 else 1.0
            target_std = tolerance_range / 6
            
            if target_std > 0 and target_mean > 0:
                k_prior = (target_mean / target_std) ** 2
                theta_prior = target_std ** 2 / target_mean
                alpha_k = 2.0
                beta_k = 2.0 / k_prior
                alpha_theta = 2.0
                beta_theta = theta_prior
                
                result_params = {
                    'k_prior': k_prior,
                    'theta_prior': theta_prior,
                    'alpha_k': alpha_k,
                    'beta_k': beta_k,
                    'alpha_theta': alpha_theta,
                    'beta_theta': beta_theta
                }
                result = (result_params, None)
                print(f"GAMMA RESULT: {result}")
                return result
            else:
                print("ERROR: Invalid gamma parameters")
                return None, "Invalid target mean or standard deviation for Gamma distribution"
        
        elif distribution == "lognormal":
            print("LOGNORMAL DISTRIBUTION PROCESSING")
            lower_bound = nominal_f + lower_tol_f
            upper_bound = nominal_f + upper_tol_f
            
            if lower_bound <= 0:
                shift = abs(lower_bound) + 0.01
                lower_bound += shift
                upper_bound += shift
                nominal_shifted = nominal_f + shift
            else:
                nominal_shifted = nominal_f
                shift = 0
                
            log_nominal = np.log(nominal_shifted)
            log_range = np.log(upper_bound) - np.log(lower_bound)
            
            mu_prior = log_nominal
            sigma_mu = log_range / 12
            sigma_prior = log_range / 6
            alpha = 2.5
            beta = (alpha - 1) * sigma_prior**2
            
            result_params = {
                'mu_prior': mu_prior,
                'sigma_mu': sigma_mu,
                'alpha': alpha,
                'beta': beta,
                'sigma_prior': sigma_prior,
                'shift': shift
            }
            result = (result_params, None)
            print(f"LOGNORMAL RESULT: {result}")
            return result
            
        elif distribution == "uniform":
            print("UNIFORM DISTRIBUTION PROCESSING")
            a_prior = nominal_f + lower_tol_f - tolerance_range * 0.1
            b_prior = nominal_f + upper_tol_f + tolerance_range * 0.1
            sigma_a = tolerance_range / 12
            sigma_b = tolerance_range / 12
            
            result_params = {
                'a_prior': a_prior,
                'b_prior': b_prior,
                'sigma_a': sigma_a,
                'sigma_b': sigma_b
            }
            result = (result_params, None)
            print(f"UNIFORM RESULT: {result}")
            return result
            
        else:
            print(f"ERROR: Unsupported distribution: {distribution}")
            return None, f"Unsupported distribution type: {distribution}"
            
    except Exception as e:
        print(f"EXCEPTION in calculate_prior_parameters: {e}")
        import traceback
        traceback.print_exc()
        return None, f"Exception in prior calculation: {str(e)}"
    
    print("=== FUNCTION END (should not reach here) ===")
    return None, "Function ended unexpectedly"

def bayesian_update_normal(data, prior_params):
    """Analytical Bayesian update for Normal distribution"""
    n = len(data)
    x_bar = np.mean(data)
    
    mu_prior = prior_params['mu_prior']
    sigma_mu = prior_params['sigma_mu']
    alpha = prior_params['alpha']
    beta = prior_params['beta']
    
    # Update parameters for μ (assuming σ² known initially)
    # First, estimate σ² from data
    s_squared = np.var(data, ddof=1) if n > 1 else prior_params['sigma_prior']**2
    
    # Posterior for μ
    precision_prior = 1 / sigma_mu**2
    precision_data = n / s_squared
    
    mu_posterior = (precision_prior * mu_prior + precision_data * x_bar) / (precision_prior + precision_data)
    sigma_mu_posterior = 1 / np.sqrt(precision_prior + precision_data)
    
    # Posterior for σ²
    alpha_posterior = alpha + n / 2
    beta_posterior = beta + 0.5 * np.sum((data - mu_posterior)**2)
    
    # Point estimates
    sigma_posterior = np.sqrt(beta_posterior / (alpha_posterior - 1))
    
    return mu_posterior, sigma_posterior

def bayesian_update_gamma(data, prior_params):
    """Analytical Bayesian update for Gamma distribution"""
    n = len(data)
    sum_data = np.sum(data)
    
    k_prior = prior_params['k_prior']
    theta_prior = prior_params['theta_prior']
    alpha_k = prior_params['alpha_k']
    beta_k = prior_params['beta_k']
    alpha_theta = prior_params['alpha_theta']
    beta_theta = prior_params['beta_theta']
    
    print(f"=== GAMMA BAYESIAN UPDATE DEBUG ===")
    print(f"Prior: k={k_prior:.6f}, θ={theta_prior:.6f}, mean={k_prior*theta_prior:.6f}")
    
    # Calculate MLE from data for comparison
    sample_mean = np.mean(data)
    sample_var = np.var(data, ddof=1) if n > 1 else sample_mean
    
    if sample_var > 0 and sample_mean > 0:
        k_mle = sample_mean**2 / sample_var
        theta_mle = sample_var / sample_mean
        print(f"Data MLE: k={k_mle:.6f}, θ={theta_mle:.6f}, mean={k_mle*theta_mle:.6f}")
        print(f"Data stats: mean={sample_mean:.6f}, std={np.sqrt(sample_var):.6f}")
        
        # Method 1: Simple weighted average (current implementation)
        prior_weight = 1.0
        data_weight = n
        total_weight = prior_weight + data_weight
        
        k_posterior_method1 = (prior_weight * k_prior + data_weight * k_mle) / total_weight
        theta_posterior_method1 = (prior_weight * theta_prior + data_weight * theta_mle) / total_weight
        
        print(f"Method 1 (current): k={k_posterior_method1:.6f}, θ={theta_posterior_method1:.6f}, mean={k_posterior_method1*theta_posterior_method1:.6f}")
        
        # Method 2: Proper conjugate updating (more accurate)
        # For Gamma likelihood with known shape parameter k:
        # If we fix k to be close to the data's shape, update θ using conjugate prior
        
        # Use a compromise shape parameter between prior and data
        k_posterior_method2 = (2 * k_prior + n * k_mle) / (2 + n)  # Slightly favor data
        
        # Given this k, update θ using conjugate relationship
        # θ | data ~ InverseGamma(α_θ + n*k, β_θ + Σx_i)
        alpha_theta_post = alpha_theta + n * k_posterior_method2
        beta_theta_post = beta_theta + sum_data
        theta_posterior_method2 = beta_theta_post / (alpha_theta_post - 1)
        
        print(f"Method 2 (improved): k={k_posterior_method2:.6f}, θ={theta_posterior_method2:.6f}, mean={k_posterior_method2*theta_posterior_method2:.6f}")
        
        # Method 3: Preserve mean, adjust shape conservatively
        target_mean = (prior_weight * k_prior * theta_prior + data_weight * sample_mean) / total_weight
        
        # Use a shape parameter that's a conservative update
        k_posterior_method3 = (prior_weight * k_prior + data_weight * k_mle) / total_weight
        theta_posterior_method3 = target_mean / k_posterior_method3
        
        print(f"Method 3 (mean-preserving): k={k_posterior_method3:.6f}, θ={theta_posterior_method3:.6f}, mean={k_posterior_method3*theta_posterior_method3:.6f}")
        
        # Choose Method 3 for better mean preservation
        return k_posterior_method3, theta_posterior_method3
        
    else:
        # Fallback to prior if data is insufficient
        return k_prior, theta_prior

def bayesian_update_lognormal(data, prior_params):
    """Analytical Bayesian update for Lognormal distribution (via log-transform)"""
    # Check if data needs shifting
    shift = prior_params.get('shift', 0)
    if shift > 0:
        data_shifted = data + shift
    else:
        data_shifted = data
    
    # Ensure all data is positive
    if np.any(data_shifted <= 0):
        min_val = np.min(data_shifted)
        shift_additional = abs(min_val) + 0.01
        data_shifted = data_shifted + shift_additional
        shift += shift_additional
    
    # Transform to log space
    log_data = np.log(data_shifted)
    
    # Use normal conjugate updates on log data
    mu_posterior, sigma_posterior = bayesian_update_normal(log_data, prior_params)
    
    return mu_posterior, sigma_posterior

def bayesian_update_uniform(data, prior_params):
    """MCMC-based Bayesian update for Uniform distribution"""
    # Simple MCMC implementation
    n_samples = 1000
    burn_in = 200
    
    # Data constraints
    data_min = np.min(data)
    data_max = np.max(data)
    
    # Initialize
    a_current = min(prior_params['a_prior'], data_min - 0.01)
    b_current = max(prior_params['b_prior'], data_max + 0.01)
    
    a_samples = []
    b_samples = []
    
    # Proposal standard deviations
    prop_sd_a = prior_params['sigma_a'] * 0.5
    prop_sd_b = prior_params['sigma_b'] * 0.5
    
    for i in range(n_samples + burn_in):
        # Update a
        a_prop = np.random.normal(a_current, prop_sd_a)
        if a_prop < data_min and a_prop < b_current:
            # Calculate acceptance probability
            log_ratio = (
                stats.norm.logpdf(a_prop, prior_params['a_prior'], prior_params['sigma_a']) -
                stats.norm.logpdf(a_current, prior_params['a_prior'], prior_params['sigma_a'])
            )
            if np.log(np.random.rand()) < log_ratio:
                a_current = a_prop
        
        # Update b
        b_prop = np.random.normal(b_current, prop_sd_b)
        if b_prop > data_max and b_prop > a_current:
            log_ratio = (
                stats.norm.logpdf(b_prop, prior_params['b_prior'], prior_params['sigma_b']) -
                stats.norm.logpdf(b_current, prior_params['b_prior'], prior_params['sigma_b'])
            )
            if np.log(np.random.rand()) < log_ratio:
                b_current = b_prop
        
        if i >= burn_in:
            a_samples.append(a_current)
            b_samples.append(b_current)
    
    # Posterior estimates
    a_posterior = np.mean(a_samples)
    b_posterior = np.mean(b_samples)
    
    return a_posterior, b_posterior

def calculate_likelihood_params(data, distribution):
    """Calculate likelihood parameters from data using MLE"""
    try:
        if distribution == "normal":
            mu_mle = np.mean(data)
            sigma_mle = np.std(data, ddof=0)
            return mu_mle, sigma_mle
            
        elif distribution == "gamma":
            # Method of moments for gamma
            sample_mean = np.mean(data)
            sample_var = np.var(data, ddof=0)
            
            if sample_var > 0:
                k_mle = sample_mean**2 / sample_var
                theta_mle = sample_var / sample_mean
                return k_mle, theta_mle
            else:
                return None, None
                
        elif distribution == "lognormal":
            if np.any(data <= 0):
                return None, None
            log_data = np.log(data)
            mu_mle = np.mean(log_data)
            sigma_mle = np.std(log_data, ddof=0)
            return mu_mle, sigma_mle
            
        elif distribution == "uniform":
            a_mle = np.min(data)
            b_mle = np.max(data)
            buffer = (b_mle - a_mle) * 0.001
            return a_mle - buffer, b_mle + buffer
            
    except Exception as e:
        print(f"Error calculating likelihood parameters: {e}")
        return None, None
    
    return None, None

def create_prior_from_posterior(distribution, post_para1, post_para2):
    """Create prior parameters from previous posterior for sequential updating"""
    try:
        if distribution == "normal":
            # For sequential Normal updates, use the posterior as the new prior
            # Assume same uncertainty level as original prior
            mu_prior = post_para1
            sigma_mu = post_para2 * 0.1  # Use 10% of posterior std as prior uncertainty
            sigma_prior = post_para2
            
            alpha = 2.5
            beta = (alpha - 1) * sigma_prior**2
            
            return {
                'mu_prior': mu_prior,
                'sigma_mu': sigma_mu,
                'alpha': alpha,
                'beta': beta,
                'sigma_prior': sigma_prior
            }
            
        elif distribution == "gamma":
            # For sequential Gamma updates
            k_prior = post_para1
            theta_prior = post_para2
            
            # Set reasonable hyperpriors for sequential update
            alpha_k = 2.0
            beta_k = 2.0 / k_prior
            alpha_theta = 2.0
            beta_theta = theta_prior
            
            return {
                'k_prior': k_prior,
                'theta_prior': theta_prior,
                'alpha_k': alpha_k,
                'beta_k': beta_k,
                'alpha_theta': alpha_theta,
                'beta_theta': beta_theta
            }
            
        elif distribution == "lognormal":
            # For sequential Lognormal updates
            mu_prior = post_para1
            sigma_mu = post_para2 * 0.1  # Use 10% as uncertainty
            sigma_prior = post_para2
            
            alpha = 2.5
            beta = (alpha - 1) * sigma_prior**2
            
            return {
                'mu_prior': mu_prior,
                'sigma_mu': sigma_mu,
                'alpha': alpha,
                'beta': beta,
                'sigma_prior': sigma_prior,
                'shift': 0  # Assume no shift for sequential updates
            }
            
        elif distribution == "uniform":
            # For sequential Uniform updates
            a_prior = post_para1
            b_prior = post_para2
            range_val = b_prior - a_prior
            sigma_a = range_val * 0.05  # 5% uncertainty
            sigma_b = range_val * 0.05
            
            return {
                'a_prior': a_prior,
                'b_prior': b_prior,
                'sigma_a': sigma_a,
                'sigma_b': sigma_b
            }
            
        else:
            return None
            
    except Exception as e:
        print(f"Error creating prior from posterior: {e}")
        return None