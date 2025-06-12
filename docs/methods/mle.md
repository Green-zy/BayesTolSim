# Maximum Likelihood Estimation (MLE)

Maximum Likelihood Estimation transforms tolerance analysis from theoretical assumptions to data-driven reality. By fitting statistical distributions directly to production measurements, MLE reveals the true behavior of manufacturing processes.

## Core Concept

### The MLE Principle
**Find the distribution parameters that make your observed data most likely to occur.**

Mathematically, for data points x₁, x₂, ..., xₙ:
$$L(\theta) = \prod_{i=1}^{n} f(x_i; \theta)$$

Where:
- **L(θ)**: Likelihood function
- **f(x; θ)**: Probability density function with parameters θ
- **Goal**: Find θ that maximizes L(θ)

### Why MLE Matters in Manufacturing
- **Reality check**: Validates or challenges design assumptions
- **Process insight**: Reveals actual manufacturing capability
- **Data-driven decisions**: Replaces guesswork with evidence
- **Risk quantification**: Accurately assesses manufacturing risk

## MLE Implementation in BayesTolSim

### Data Requirements
**CSV format with specific structure**:
```csv
Dimension_Name
25.0023
24.9987
25.0156
24.9945
25.0089
...
```

**Critical requirements**:
- **Single column**: Only measurement data
- **Exact name match**: Column header must match dimension name exactly
- **Sufficient data**: Minimum 20-30 samples for reliable estimates
- **Quality data**: Representative of actual production conditions

### Distribution-Specific MLE

=== "Normal Distribution"
    **Analytical solution (closed form)**
    
    **Parameters**:
    - μ (mean): Sample average
    - σ (standard deviation): Population standard deviation
    
    **Formulas**:
    ```
    μ_mle = (1/n) × Σ(xi)
    σ_mle = √[(1/n) × Σ(xi - μ_mle)²]
    ```
    
    **Use case**: Most manufacturing processes with symmetric variation

=== "Gamma Distribution"
    **Method of moments approach**
    
    **Parameters**:
    - k (shape): Controls distribution shape
    - θ (scale): Controls distribution spread
    
    **Formulas**:
    ```
    Sample mean: x̄ = (1/n) × Σ(xi)
    Sample variance: s² = (1/(n-1)) × Σ(xi - x̄)²
    
    k_mle = x̄² / s²
    θ_mle = s² / x̄
    ```
    
    **Use case**: Complex processes with flexible shape requirements

=== "Lognormal Distribution"
    **Log-transformation to Normal**
    
    **Parameters**:
    - μ (location): Mean of log-transformed data
    - σ (shape): Standard deviation of log-transformed data
    
    **Formulas**:
    ```
    yi = ln(xi) for all positive xi
    μ_mle = (1/n) × Σ(yi)
    σ_mle = √[(1/n) × Σ(yi - μ_mle)²]
    ```
    
    **Use case**: Right-skewed processes, tool wear effects

=== "Uniform Distribution"
    **Simple bounds estimation**
    
    **Parameters**:
    - a (lower bound): Minimum value
    - b (upper bound): Maximum value
    
    **Formulas**:
    ```
    a_mle = min(data) - small_buffer
    b_mle = max(data) + small_buffer
    ```
    
    **Use case**: Highly controlled processes with known limits

## Advantages of MLE Approach

### Statistical Optimality
- **Asymptotic efficiency**: Best possible estimates with large samples
- **Consistency**: Converges to true parameters as sample size increases
- **Invariance**: Transformations preserve MLE properties

### Practical Benefits
- **No assumptions**: Let data determine distribution shape
- **Objective**: Removes subjective parameter choices
- **Validation**: Quantifies how well model fits data
- **Comparative**: Can test multiple distributions

### Engineering Value
- **Process capability**: True capability based on actual performance
- **Supplier assessment**: Objective evaluation of vendor performance
- **Process improvement**: Identifies actual vs. theoretical performance gaps
- **Risk assessment**: Realistic defect rate predictions

## Limitations and Considerations

### Data Quality Requirements
**Garbage in, garbage out principle**:

=== "Sample Size"
    **Minimum requirements by distribution**:
    
    - **Normal**: 20+ samples for basic reliability
    - **Gamma**: 50+ samples (complex shape estimation)
    - **Lognormal**: 30+ samples (log-transform reduces effective n)
    - **Uniform**: 15+ samples (simple bounds)

=== "Representativeness"
    **Data must reflect actual production**:
    
    - **Process stability**: Consistent operating conditions
    - **Time span**: Adequate sampling period
    - **Operational conditions**: Normal production environment
    - **Measurement quality**: Calibrated, precise instruments

### Statistical Assumptions
**MLE assumes**:
- **Independent samples**: No systematic correlations
- **Identically distributed**: Same underlying process
- **Correct model**: Distribution choice is appropriate
- **Stable process**: Parameters don't change over time

### Practical Limitations
- **Historical snapshot**: Reflects past performance only
- **No forward guidance**: Doesn't incorporate design intent
- **Outlier sensitivity**: Extreme values can skew estimates
- **Distribution choice**: Still requires engineering judgment

## Model Validation

### Goodness of Fit Assessment

=== "Visual Methods"
    **Graphical validation techniques**:
    
    - **Histogram overlay**: Does fitted curve match data shape?
    - **Q-Q plots**: Quantile-quantile comparison
    - **P-P plots**: Probability-probability comparison
    - **Residual plots**: Pattern analysis in deviations

=== "Statistical Tests"
    **Formal hypothesis testing**:
    
    - **Kolmogorov-Smirnov**: General distribution testing
    - **Anderson-Darling**: Sensitive to tail behavior
    - **Cramér-von Mises**: Alternative goodness-of-fit test
    - **Shapiro-Wilk**: Specifically for normality testing

### Model Selection Criteria
**When multiple distributions fit reasonably well**:

- **AIC (Akaike Information Criterion)**: Balances fit quality with complexity
- **BIC (Bayesian Information Criterion)**: Stronger penalty for complexity
- **Engineering judgment**: Consider physical process mechanisms
- **Robustness**: How sensitive are results to distribution choice?

## Best Practices

### Data Collection Strategy
1. **Planned sampling**: Systematic collection over time
2. **Process documentation**: Record operating conditions
3. **Measurement protocols**: Standardized measurement procedures
4. **Quality control**: Regular calibration and validation

### Analysis Workflow
1. **Exploratory analysis**: Understand data characteristics
2. **Distribution comparison**: Test multiple candidates
3. **Parameter estimation**: Apply MLE to best-fit distribution
4. **Validation**: Assess goodness of fit
5. **Sensitivity analysis**: Test robustness of conclusions

### Integration Strategy
- **Complement Six Sigma**: Use MLE to validate theoretical assumptions
- **Inform Bayesian**: Use MLE results as likelihood in Bayesian updating
- **Continuous improvement**: Regular updates with new production data
- **Process monitoring**: Track parameter evolution over time

## Implementation Workflow in BayesTolSim

### Step 1: Data Preparation
```csv
# Prepare CSV with exact dimension name
Shaft_Diameter
50.023
49.987
50.156
...
```

### Step 2: Upload and Processing
1. Click "MLE Data" button for target dimension
2. Select prepared CSV file
3. System automatically:
   - Validates data format
   - Estimates optimal parameters
   - Updates distribution visualization

### Step 3: Results Interpretation
- **Parameter values**: Updated Para1 and Para2 fields
- **Visual feedback**: Green "✓ MLE Applied" indicator
- **Distribution plot**: Histogram with fitted curve overlay
- **Statistics**: Enhanced capability metrics

### Step 4: Validation and Decision
- **Visual inspection**: Does curve fit data well?
- **Parameter reasonableness**: Are estimates physically plausible?
- **Capability assessment**: Updated Cp/Cpk values
- **Process decision**: Accept, improve, or investigate further

## Performance Comparison

### Traditional vs. MLE Approach

| Aspect | Six Sigma Theory | MLE Reality |
|--------|------------------|-------------|
| **Basis** | Design tolerances | Production data |
| **Parameters** | σ = tolerance/6 | σ = actual variation |
| **Assumption** | Normal distribution | Data determines distribution |
| **Capability** | Theoretical Cp/Cpk | Actual Cp/Cpk |
| **Risk** | Assumed defect rate | Measured defect rate |

### When MLE Reveals Surprises
**Common findings**:
- **Higher variation**: Real σ > theoretical σ
- **Process bias**: Mean ≠ nominal
- **Non-normal behavior**: Skewness, multiple modes
- **Capability gaps**: Actual Cp < design Cp

## Advanced Applications

### Process Development
- **New process qualification**: Establish actual capabilities
- **Supplier evaluation**: Objective capability assessment
- **Process comparison**: Compare alternative manufacturing methods
- **Equipment validation**: Verify machine performance claims

### Quality Control
- **Control limit setting**: Data-driven statistical process control
- **Capability studies**: Realistic process capability assessment
- **Defect rate prediction**: Accurate quality forecasting
- **Process monitoring**: Track performance evolution

### Cost Optimization
- **Tolerance relaxation**: Identify over-specified tolerances
- **Process selection**: Choose most cost-effective capable processes
- **Investment justification**: Quantify benefits of process improvements
- **Risk management**: Balance quality costs with defect costs

---

**Next**: Learn how to combine MLE insights with design knowledge using [Bayesian Analysis](bayesian.md), or see MLE in action with our [Production Data Example](../examples/mle-example.md).