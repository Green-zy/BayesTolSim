# Six Sigma Approach

The Six Sigma method forms the foundation of traditional tolerance analysis. It provides a standardized approach based on normal distribution theory and has been the industry standard for decades.

## Core Principles

### Normal Distribution Assumption
Six Sigma analysis assumes that manufacturing variations follow a **normal distribution**:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}$$

Where:
- **μ (mu)**: Mean (center of distribution)
- **σ (sigma)**: Standard deviation (measure of spread)

### The 6σ Rule
**Principle**: 99.73% of normally distributed values fall within ±3σ of the mean

**Tolerance interpretation**: If total tolerance range = 6σ, then:
- **σ = tolerance range / 6**
- **Process naturally stays within specifications**

## Parameter Calculation

### Automatic Parameter Estimation
BayesTolSim automatically calculates distribution parameters from tolerance specifications:

#### For Normal Distribution:
```
μ (Para1) = Nominal value
σ (Para2) = (Upper tolerance - Lower tolerance) / 6
```

#### Example Calculation:
```
Dimension: Shaft diameter
Nominal: 50.0 mm
Upper tolerance: +0.05 mm  
Lower tolerance: -0.03 mm

Calculation:
μ = 50.0 mm
σ = (0.05 - (-0.03)) / 6 = 0.08 / 6 = 0.0133 mm
```

### Statistical Interpretation:
- **99.73%** of shafts will be between 49.96 mm and 50.04 mm
- **Process capability** can be assessed using Cp and Cpk
- **Defect rate** can be estimated using normal distribution CDF

## Process Capability Metrics

### Cp (Process Capability Index)
**Formula**:
$$Cp = \frac{USL - LSL}{6\sigma}$$

**Interpretation**:
- **Cp > 1.33**: Capable process (Six Sigma standard)
- **Cp = 1.0**: Process spread equals specification spread
- **Cp < 1.0**: Incapable process

### Cpk (Process Capability with Centering)
**Formula**:
$$Cpk = \min\left(\frac{USL - \mu}{3\sigma}, \frac{\mu - LSL}{3\sigma}\right)$$

Where:
- **USL**: Upper Specification Limit = Nominal + Upper tolerance
- **LSL**: Lower Specification Limit = Nominal + Lower tolerance

**Interpretation**:
- **Cpk = Cp**: Process perfectly centered
- **Cpk < Cp**: Process off-center
- **Cpk < 1.0**: Process incapable even if Cp > 1.0

## Advantages of Six Sigma Method

### Simplicity and Speed
- **Easy to understand**: Normal distribution is intuitive
- **Quick calculation**: Minimal computational requirements
- **Industry standard**: Widely accepted and understood

### Established Framework
- **Historical data**: Decades of industrial application
- **Quality standards**: ISO, automotive, aerospace industries
- **Training programs**: Extensive educational infrastructure

### Conservative Approach
- **Safety factor**: 6σ provides substantial margin
- **Risk mitigation**: Accounts for unknown variations
- **Regulatory acceptance**: Meets most quality standards

## Limitations and Considerations

### Distribution Assumptions
**Real processes may not be normal**:
- **Skewed distributions**: Tool wear, material properties
- **Bounded processes**: Physical limits create non-normal behavior
- **Multi-modal**: Multiple process settings or suppliers

### Process Variations
**Six Sigma assumes stable processes**:
- **Time-varying parameters**: Tool wear, temperature effects
- **Batch-to-batch variation**: Material lot differences
- **Setup variations**: Operator and equipment differences

### Tolerance Allocation
**Equal emphasis on all dimensions**:
- **Critical vs. non-critical**: Some dimensions more important
- **Cost implications**: Tighter tolerances increase manufacturing cost
- **Interaction effects**: Dimension correlations not considered

## When to Use Six Sigma Method

### Ideal Scenarios
=== "Design Phase"
    **Early design when data is limited**
    
    - Establish baseline capability estimates
    - Allocate initial tolerances
    - Compare design alternatives

=== "Well-Established Processes"
    **Mature manufacturing with known behavior**
    
    - Processes with good historical control
    - Normal distribution validated by data
    - Standard operating procedures in place

=== "Conservative Analysis"
    **High-risk or safety-critical applications**
    
    - Aerospace, medical devices
    - When failure consequences are severe
    - Regulatory requirements mandate approach

### Enhancement Opportunities
**Six Sigma can be enhanced by**:
- **Data validation**: Use MLE to verify normal assumption
- **Bayesian integration**: Combine with trial data
- **Sequential improvement**: Start with Six Sigma, refine with data

## Implementation in BayesTolSim

### Default Workflow
1. **Enter tolerances**: Nominal and ± tolerance values
2. **Select "Normal"**: Distribution automatically chosen
3. **Auto-calculation**: μ and σ computed from tolerances
4. **Visualization**: View normal distribution curves
5. **Monte Carlo**: Simulate final dimension behavior

### Manual Override
**Custom parameter entry**:
- Override automatic calculations
- Use process-specific knowledge
- Apply empirical correction factors

### Integration with Other Methods
**Six Sigma as baseline**:
- Compare with MLE results
- Use as Bayesian prior
- Validate assumptions with data

---

**Next**: Learn about [Maximum Likelihood Estimation](mle.md) to incorporate production data into your analysis.