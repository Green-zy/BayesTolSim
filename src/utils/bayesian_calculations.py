# src/utils/bayesian_calculations.py

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import warnings

def calculate_prior_parameters(distribution, nominal, upper_tol, lower_tol):
    """Calculate prior distribution parameters from tolerance specifications"""
    try:
        nominal = float(nominal)
        upper_tol = float(upper_tol)
        lower_tol = float(lower_tol)
    except (ValueError, TypeError):
        return None, None
        
    tolerance_range = upper_tol - lower_tol
    
    if distribution == "normal":
        # Prior: μ ~ N(nominal, σ_μ²), σ² ~ IG(α, β)
        mu_prior = nominal
        sigma_mu = tolerance_range / 12  # Prior uncertainty on mean
        sigma_prior = tolerance_range / 6  # Prior estimate of std dev
        
        # Inverse-Gamma parameters for σ²
        alpha = 2.5
        beta = (alpha - 1) * sigma_prior**2
        
        return {
            'mu_prior': mu_prior,
            'sigma_mu': sigma_mu,
            'alpha': alpha,
            'beta': beta,
            'sigma_prior': sigma_prior
        }, None
        
    elif distribution == "gamma":
        # Prior: k ~ Gamma(α_k, β_k), θ ~ IG(α_θ, β_θ)
        target_mean = nominal if nominal > 0 else 1.0
        target_std = tolerance_range / 6
        
        if target_std > 0 and target_mean > 0:
            # Method of moments: k = mean²/var, θ = var/mean
            k_prior = (target_mean / target_std) ** 2
            theta_prior = target_std ** 2 / target_mean
            
            # Set reasonable hyperpriors that don't dominate the data
            alpha_k = 2.0  # Weak prior on shape
            beta_k = 2.0 / k_prior  # Scale to center around k_prior
            alpha_theta = 2.0  # Weak prior on scale
            beta_theta = theta_prior  # Scale to center around theta_prior
            
            return {
                'k_prior': k_prior,
                'theta_prior': theta_prior,
                'alpha_k': alpha_k,
                'beta_k': beta_k,
                'alpha_theta': alpha_theta,
                'beta_theta': beta_theta
            }, None
        else:
            return None, None
            
    elif distribution == "lognormal":
        # Transform to log space and use normal conjugate updates
        lower_bound = nominal + lower_tol
        upper_bound = nominal + upper_tol
        
        if lower_bound <= 0:
            # Shift to ensure positive values
            shift = abs(lower_bound) + 0.01
            lower_bound += shift
            upper_bound += shift
            nominal_shifted = nominal + shift
        else:
            nominal_shifted = nominal
            
        # Work in log space
        log_nominal = np.log(nominal_shifted)
        log_range = np.log(upper_bound) - np.log(lower_bound)
        
        mu_prior = log_nominal
        sigma_mu = log_range / 12
        sigma_prior = log_range / 6
        
        alpha = 2.5
        beta = (alpha - 1) * sigma_prior**2
        
        return {
            'mu_prior': mu_prior,
            'sigma_mu': sigma_mu,
            'alpha': alpha,
            'beta': beta,
            'sigma_prior': sigma_prior,
            'shift': shift if lower_bound <= 0 else 0
        }, None
        
    elif distribution == "uniform":
        # Non-conjugate case - will need MCMC
        a_prior = nominal + lower_tol - tolerance_range * 0.1
        b_prior = nominal + upper_tol + tolerance_range * 0.1
        sigma_a = tolerance_range / 12
        sigma_b = tolerance_range / 12
        
        return {
            'a_prior': a_prior,
            'b_prior': b_prior,
            'sigma_a': sigma_a,
            'sigma_b': sigma_b
        }, None
        
    return None, None

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
    sum_log_data = np.sum(np.log(data))
    
    k_prior = prior_params['k_prior']
    theta_prior = prior_params['theta_prior']
    alpha_k = prior_params['alpha_k']
    beta_k = prior_params['beta_k']
    alpha_theta = prior_params['alpha_theta']
    beta_theta = prior_params['beta_theta']
    
    # For Gamma distribution with conjugate priors:
    # If X ~ Gamma(k, θ), with priors:
    # k ~ Gamma(α_k, β_k)  
    # θ ~ InverseGamma(α_θ, β_θ)
    
    # Posterior updates (using proper conjugate relationships):
    # θ | data ~ InverseGamma(α_θ + n*k, β_θ + Σx_i)
    # For shape parameter, we'll use a weighted average approach since full conjugate updating is complex
    
    # First, get MLE estimates from data
    sample_mean = np.mean(data)
    sample_var = np.var(data, ddof=1) if n > 1 else sample_mean
    
    if sample_var > 0 and sample_mean > 0:
        k_mle = sample_mean**2 / sample_var
        theta_mle = sample_var / sample_mean
        
        # Weighted combination of prior and likelihood
        # Weight by effective sample sizes
        prior_weight = 1.0  # Prior has weight of 1 "observation"
        data_weight = n     # Data has weight of n observations
        total_weight = prior_weight + data_weight
        
        # Posterior estimates as weighted averages
        k_posterior = (prior_weight * k_prior + data_weight * k_mle) / total_weight
        theta_posterior = (prior_weight * theta_prior + data_weight * theta_mle) / total_weight
        
    else:
        # Fallback to prior if data is insufficient
        k_posterior = k_prior
        theta_posterior = theta_prior
    
    return k_posterior, theta_posterior

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