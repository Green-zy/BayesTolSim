# Bayesian Analysis

Bayesian analysis represents the pinnacle of statistical sophistication in tolerance analysis, intelligently combining engineering knowledge (prior information) with empirical evidence (data) to produce optimal parameter estimates with quantified uncertainty.

## Bayesian Philosophy

### The Bayesian Paradigm
**"Parameters have uncertainty, and we learn about them through data"**

**Core principle**: Update beliefs systematically as new evidence becomes available.

**Mathematical framework**:
$$P(\theta | data) = \frac{P(data | \theta) \times P(\theta)}{P(data)}$$

Where:
- **P(θ|data)**: Posterior (updated knowledge)
- **P(data|θ)**: Likelihood (what data tells us)
- **P(θ)**: Prior (initial knowledge)
- **P(data)**: Evidence (normalization constant)

### Why Bayesian for Manufacturing?
- **Incorporates engineering knowledge**: Design specifications become meaningful priors
- **Quantifies uncertainty**: Full probability distributions, not just point estimates
- **Sequential learning**: Continuously improves with new data
- **Optimal information fusion**: Mathematically best way to combine information sources

## Bayesian Workflow in BayesTolSim

### Stage 1: Prior Specification
**Transform design specifications into probabilistic knowledge**

#### From Tolerance Specifications
Design tolerances automatically become Bayesian priors:

=== "Normal Distribution Prior"
    **Design specs → Normal-Inverse-Gamma prior**
    
    ```
    μ_prior = Nominal value
    σ_μ = tolerance_range / 12  (prior uncertainty about mean)
    
    α = 2.5  (shape parameter for precision)
    β = (α - 1) × σ_prior²  (scale parameter)
    ```
    
    **Interpretation**: 
    - Mean centered on design nominal
    - Uncertainty reflects tolerance range
    - Moderately informative prior

=== "Gamma Distribution Prior"
    **Method of moments → Gamma-Inverse-Gamma prior**
    
    ```
    k_prior = (target_mean / target_std)²
    θ_prior = target_std² / target_mean
    
    α_k = 2.0  (shape hyperparameter)
    β_k = 2.0 / k_prior  (scale hyperparameter)
    ```

### Stage 2: Likelihood from Data
**What the trial/prototype data suggests**

#### Data Processing
Trial measurements provide likelihood information:
- **Sample size**: Typically 10-50 prototype measurements
- **Quality**: Representative of intended production process
- **Independence**: No systematic correlations between samples

#### Likelihood Calculation
For each distribution, data likelihood computed using:
- **Normal**: Standard normal likelihood with sample mean and variance
- **Gamma**: Gamma likelihood using method of moments
- **Lognormal**: Normal likelihood on log-transformed data
- **Uniform**: Constrained likelihood respecting data bounds

### Stage 3: Posterior Computation
**Optimal combination of prior and likelihood**

#### Conjugate Updating (Analytical)
For mathematically convenient cases:

=== "Normal Distribution"
    **Exact analytical solution**
    
    **Precision-weighted combination**:
    ```
    τ_prior = 1/σ_prior²  (prior precision)
    τ_data = n/s²  (data precision)
    
    μ_posterior = (τ_prior × μ_prior + τ_data × x̄) / (τ_prior + τ_data)
    σ_posterior² = 1 / (τ_prior + τ_data)
    ```
    
    **Variance updating**:
    ```
    α_posterior = α_prior + n/2
    β_posterior = β_prior + Σ(xi - μ_posterior)²/2
    ```

=== "Lognormal Distribution"
    **Log-space transformation**
    
    Transform to log-space and apply Normal conjugate updating:
    ```
    yi = ln(xi) for all data points
    Apply Normal Bayesian updating to {yi}
    Transform results back to original scale
    ```

#### Non-Conjugate Updating (MCMC)
For complex cases like Uniform distribution:

=== "Uniform Distribution"
    **Metropolis-Hastings sampling**
    
    ```python
    # Simplified algorithm
    for iteration in range(n_samples):
        # Propose new parameters
        a_new = random_walk(a_current)
        b_new = random_walk(b_current)
        
        # Check constraints: a < min(data), b > max(data)
        if valid_constraints(a_new, b_new, data):
            # Calculate acceptance probability
            ratio = likelihood_ratio × prior_ratio
            if random() < min(1, ratio):
                accept_proposal()
    ```

## Sequential Learning

### Iterative Knowledge Refinement
**The power of continuous improvement**

#### First Update: Prior → Posterior₁
```
Prior (Design specs) + Data₁ → Posterior₁
```
- Combines engineering knowledge with initial trials
- Reduces parameter uncertainty
- Provides updated process understanding

#### Second Update: Posterior₁ → Posterior₂
```
Posterior₁ (Previous knowledge) + Data₂ → Posterior₂
```
- Previous posterior becomes new prior
- Additional data further refines estimates
- Uncertainty continues to decrease

#### Convergence Properties
**As data accumulates**:
- **Parameter estimates stabilize**: Central tendency converges
- **Uncertainty decreases**: Confidence intervals narrow
- **Robustness increases**: Less sensitive to individual data points
- **Predictive accuracy improves**: Better forecasting capability

### Mathematical Properties
**Theoretical guarantees**:
- **Coherence**: Consistent probability updating
- **Optimality**: Minimizes expected loss under reasonable criteria
- **Robustness**: Graceful handling of model uncertainty
- **Calibration**: Uncertainty quantification is well-calibrated

## Three-Curve Visualization

### Understanding the Bayesian Trinity

=== "Prior Curve (Blue)"
    **Engineering knowledge before seeing data**
    
    **Characteristics**:
    - Center: Design nominal
    - Spread: Engineering uncertainty
    - Shape: Design assumptions
    
    **Interpretation**:
    - "What we expected based on specifications"
    - Reflects tolerance analysis and engineering judgment
    - May be optimistic or conservative

=== "Likelihood Curve (Orange)"
    **What the data suggests**
    
    **Characteristics**:
    - Center: Sample mean
    - Spread: Sample variability
    - Shape: Empirical distribution
    
    **Interpretation**:
    - "What actually happened in trials"
    - Reflects prototype/trial manufacturing reality
    - Independent of design expectations

=== "Posterior Curve (Green)"
    **Optimal combination of knowledge and evidence**
    
    **Characteristics**:
    - Center: Weighted average of prior and likelihood
    - Spread: Reduced uncertainty (narrower than either prior or likelihood)
    - Shape: Refined understanding
    
    **Interpretation**:
    - "Best estimate combining all available information"
    - More confident than either source alone
    - Balanced between design intent and empirical evidence

### Visual Interpretation Guide

#### Scenario 1: Prior-Data Agreement
- **All three curves clustered together**
- **Interpretation**: Design expectations confirmed by data
- **Action**: High confidence in process capability

#### Scenario 2: Prior-Data Disagreement
- **Prior and likelihood separated**
- **Posterior between them**
- **Interpretation**: Reality differs from expectations
- **Action**: Investigate causes, update design understanding

#### Scenario 3: High Data Precision
- **Likelihood very narrow**
- **Posterior close to likelihood**
- **Interpretation**: Data overwhelms prior assumptions
- **Action**: Trust the empirical evidence

#### Scenario 4: High Prior Confidence
- **Prior very narrow**
- **Posterior close to prior**
- **Interpretation**: Strong engineering knowledge confirmed
- **Action**: Limited learning from small data sample

## Advantages of Bayesian Approach

### Statistical Superiority
- **Optimal estimation**: Mathematically best use of available information
- **Uncertainty quantification**: Full probability distributions
- **Sequential consistency**: Coherent updating with new data
- **Robustness**: Graceful handling of model uncertainty

### Engineering Value
- **Incorporates expertise**: Engineering knowledge isn't discarded
- **Risk quantification**: Probability distributions enable risk analysis
- **Decision support**: Provides input for engineering decisions
- **Continuous improvement**: Natural framework for ongoing learning

### Business Benefits
- **Faster qualification**: Combines specs with limited trial data
- **Risk management**: Quantified uncertainty supports decision making
- **Cost optimization**: Better parameter estimates enable efficient tolerancing
- **Competitive advantage**: Superior process understanding

## Challenges and Limitations

### Technical Challenges

=== "Prior Specification"
    **Subjectivity in prior choice**
    
    **Issues**:
    - How confident should prior be?
    - What if design assumptions are wrong?
    - How to handle conflicting expert opinions?
    
    **Mitigation**:
    - Sensitivity analysis with different priors
    - Use relatively uninformative priors when uncertain
    - Update priors based on historical performance

=== "Computational Complexity"
    **MCMC can be demanding**
    
    **Issues**:
    - Convergence assessment
    - Computational time for complex models
    - Debugging sampling algorithms
    
    **BayesTolSim solution**:
    - Optimized algorithms for common distributions
    - Automatic convergence checking
    - User-friendly interface hides complexity

### Practical Considerations

=== "Data Quality Requirements"
    **Same as MLE, plus more**
    
    - **Representative samples**: Must reflect intended production
    - **Process stability**: Consistent with prior assumptions
    - **Adequate sample size**: Enough to meaningfully update prior
    - **Quality measurements**: Precise, unbiased instrumentation

=== "Interpretation Complexity"
    **Three-curve visualization requires understanding**
    
    - **Training needed**: Team must understand Bayesian concepts
    - **Communication challenges**: Explaining uncertainty to stakeholders
    - **Decision frameworks**: How to use probabilistic information

## Best Practices

### Prior Specification Guidelines
1. **Start conservative**: Use moderately informative priors
2. **Document assumptions**: Record rationale for prior choices
3. **Sensitivity analysis**: Test robustness to prior specification
4. **Update systematically**: Learn from prior-data disagreements

### Data Collection Strategy
1. **Quality over quantity**: Prefer fewer high-quality measurements
2. **Representative conditions**: Match intended production environment
3. **Systematic sampling**: Avoid bias in measurement selection
4. **Process documentation**: Record conditions and context

### Results Communication
1. **Visual emphasis**: Use three-curve plots effectively
2. **Uncertainty focus**: Emphasize confidence intervals
3. **Engineering context**: Relate results to practical decisions
4. **Progressive disclosure**: Start simple, add complexity gradually

## Advanced Applications

### Design Optimization
**Use posterior distributions for tolerance allocation**:
- **Monte Carlo with posteriors**: Propagate parameter uncertainty
- **Robust design**: Account for manufacturing uncertainty
- **Sensitivity analysis**: Identify critical parameters

### Process Control
**Bayesian monitoring and control**:
- **Control limits**: Based on posterior predictive distributions
- **Change detection**: Bayesian hypothesis testing
- **Process adjustment**: Decision theory for interventions

### Supply Chain Management
**Supplier qualification and monitoring**:
- **Capability assessment**: Bayesian process capability
- **Risk evaluation**: Uncertainty-aware supplier selection
- **Continuous monitoring**: Update supplier performance models

### Product Development
**Accelerated learning for new products**:
- **Knowledge transfer**: Use previous product posteriors as priors
- **Platform development**: Hierarchical Bayesian models
- **Technology transition**: Systematic knowledge migration

---

**Next**: See Bayesian analysis in action with our [Bayesian Updating Example](../examples/bayesian-example.md), or explore how all three methods compare in our [Basic Example](../examples/basic-example.md).