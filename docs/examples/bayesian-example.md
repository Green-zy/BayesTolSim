# Bayesian Analysis Example

This tutorial demonstrates how to use Bayesian updating to intelligently combine design specifications (prior knowledge) with trial sample data (new evidence) for optimal parameter estimation.

## Conceptual Overview

**Bayesian Philosophy**: Start with what you know (design specs), update with what you learn (data)

**Mathematical Framework**:
```
Prior (Design Knowledge) × Likelihood (Data Evidence) = Posterior (Updated Knowledge)
```

**Practical Benefit**: Get the best of both worlds - design intent plus empirical evidence

## Scenario Description

**Context**: New bearing design for automotive application
- **Design stage**: Engineering specifications based on function requirements
- **Prototype stage**: Initial manufacturing trials with 25 sample measurements
- **Goal**: Optimize process parameters before full production

**Component**: Inner race diameter
- **Functional requirement**: 50.0 ±0.02 mm (tight tolerance for proper fit)
- **Design confidence**: Medium (new supplier, new process)
- **Trial data**: 25 prototype measurements available

## Step 1: Prepare Trial Data

### Create Trial Dataset
File: `bearing_inner_race_trials.csv`

```csv
Bearing_Inner_Race
50.0045
49.9978
50.0123
49.9956
50.0089
49.9934
50.0167
49.9912
50.0078
49.9967
50.0134
49.9945
50.0056
49.9989
50.0112
49.9923
50.0087
49.9945
50.0156
49.9978
50.0034
49.9967
50.0098
49.9934
50.0123
```

**Data characteristics** (for tutorial understanding):
- **Sample size**: 25 measurements (typical prototype batch)
- **Sample mean**: ~50.002 (slightly above nominal)
- **Sample std**: ~0.008 (tighter than design assumption)
- **Distribution**: Approximately normal

## Step 2: Setup Prior (Design Specifications)

### Define Design-Based Prior
1. **Add dimension**:
   - **Name**: `Bearing_Inner_Race`
   - **Direction**: `+`
   - **Nominal**: `50.0`
   - **Upper Tolerance**: `0.02`
   - **Lower Tolerance**: `-0.02`
   - **Distribution**: `Normal`

2. **Observe prior parameters**:
   - **Para1 (μ)**: 50.000000
   - **Para2 (σ)**: 0.006667 (= 0.04/6)

### Interpret Prior
**Engineering assumptions**:
- **μ = 50.0**: Process should center on nominal
- **σ = 0.0067**: Six Sigma approach suggests this variation
- **Confidence level**: Medium (new process, some uncertainty)

## Step 3: Apply Bayesian Updating

### Upload Trial Data
1. **Click**: "Bayes Data" button in the Bearing_Inner_Race row
2. **Select file**: `bearing_inner_race_trials.csv`
3. **Wait for processing**: Should see "⚡ 1 Bayes Applied" with blue background

### Observe Parameter Evolution
After successful upload, parameters update:
- **Para1**: ~50.0017 (balanced between prior and data)
- **Para2**: ~0.0051 (reduced uncertainty)

!!! info "Bayesian Magic"
    - **Balanced estimate**: Neither pure design nor pure data
    - **Reduced uncertainty**: Posterior more confident than either prior or data alone
    - **Principled combination**: Mathematically optimal integration

## Step 4: Analyze Three-Curve Visualization

### Understanding the Plot
When you select "Bearing_Inner_Race" in the distribution viewer:

=== "Prior (Blue Curve)"
    **Design specifications as starting knowledge**
    
    - **Center**: 50.000 (design nominal)
    - **Spread**: Reflects design uncertainty
    - **Source**: Engineering tolerance analysis

=== "Likelihood (Orange Curve)"
    **What the trial data suggests**
    
    - **Center**: ~50.002 (trial data mean)
    - **Spread**: Based on trial data variation
    - **Source**: 25 prototype measurements

=== "Posterior (Green Area)"
    **Updated knowledge after seeing data**
    
    - **Center**: ~50.0017 (compromise between prior and data)
    - **Spread**: Narrower than either prior or likelihood
    - **Source**: Bayesian combination

### Statistical Evolution
```
=== PRIOR ===
Distribution: Normal
Mean (μ): 50.000
Std Dev (σ): 0.0067
Source: Design specifications

=== LIKELIHOOD ===
Distribution: Normal
Mean (μ): 50.002
Std Dev (σ): 0.008
Source: Trial data (n=25)

=== POSTERIOR ===
Distribution: Normal
Mean (μ): 50.0017
Std Dev (σ): 0.0051
Cp: 1.568
Cpk: 1.531
```

## Step 5: Interpret Results

### Knowledge Integration Success
**Posterior combines best of both**:

1. **Mean adjustment**: Moved from 50.000 to 50.0017
   - **Prior influence**: Keeps close to design intent
   - **Data influence**: Acknowledges measured bias
   - **Balanced result**: Neither pure theory nor pure empiricism

2. **Uncertainty reduction**: σ decreased from 0.0067 to 0.0051
   - **Information gain**: Data reduces uncertainty
   - **Confidence increase**: More precise parameter estimates
   - **Better predictions**: Tighter confidence intervals

### Process Capability Assessment
**Posterior indicates excellent capability**:
- **Cp = 1.568**: Well above 1.33 minimum requirement
- **Cpk = 1.531**: Process well-centered and capable
- **Defect rate**: Extremely low risk of out-of-spec parts

## Step 6: Sequential Updates

### Second Batch of Data
Simulate receiving additional trial data after process adjustments:

File: `bearing_inner_race_batch2.csv`
```csv
Bearing_Inner_Race
50.0012
49.9989
50.0034
49.9967
50.0045
49.9978
50.0023
49.9956
50.0067
49.9934
50.0089
49.9912
50.0001
49.9945
50.0056
```

### Upload Second Batch
1. **Click**: "Bayes Data" button again (same dimension)
2. **Select**: `bearing_inner_race_batch2.csv`
3. **Observe**: "⚡ 2 Bayes Applied" (sequential update indicator)

### Sequential Learning Results
**Parameters after second update**:
- **Para1**: ~50.0009 (further refined estimate)
- **Para2**: ~0.0043 (even more confident)

**Benefits of sequential updating**:
- **Continuous improvement**: Each data batch improves estimates
- **Real-time adaptation**: Process changes reflected immediately
- **Uncertainty reduction**: Confidence grows with sample size

## Step 7: Compare All Methods

### Method Comparison Table

| Method | Mean | Std Dev | Cp | Cpk | Data Used | Design Knowledge |
|--------|------|---------|----|----|-----------|------------------|
| **Six Sigma** | 50.000 | 0.0067 | 1.000 | 1.000 | None | Full |
| **MLE** | 50.002 | 0.008 | 0.833 | 0.792 | Full | None |
| **Bayesian** | 50.0009 | 0.0043 | 1.860 | 1.823 | Partial | Partial |

### Method Strengths Revealed

=== "Six Sigma"
    **Conservative but uninformed**
    
    - **Pros**: Simple, established, risk-averse
    - **Cons**: Ignores actual process behavior
    - **Best for**: Early design when no data available

=== "MLE"
    **Data-driven but ignores design intent**
    
    - **Pros**: Uses real measurements
    - **Cons**: Small sample size creates uncertainty
    - **Best for**: Mature processes with large datasets

=== "Bayesian"
    **Optimal information integration**
    
    - **Pros**: Best of both worlds, uncertainty quantification
    - **Cons**: More complex, requires both specs and data
    - **Best for**: Development phase with evolving data

## Step 8: Engineering Decisions

### Process Qualification Decision
**Based on Bayesian results**:
- **Proceed to production**: Cp = 1.86 >> 1.33 requirement
- **Process is robust**: Low risk of quality issues
- **Monitoring plan**: Continue sequential updates in production

### Tolerance Optimization
**Current analysis suggests over-specification**:
- **Relax tolerances**: Could open to ±0.03 mm while maintaining Cp > 1.33
- **Cost reduction**: Less stringent manufacturing requirements
- **Alternative applications**: Use this process for tighter-tolerance components

### Risk Assessment
**Quantified uncertainty**:
- **Parameter confidence**: σ = 0.0043 gives precise estimates
- **Defect prediction**: Very low probability of specification violations
- **Process monitoring**: Statistical control limits established

## Step 9: Production Implementation

### Control Strategy
**Based on Bayesian learning**:

1. **Initial setup**: Target μ = 50.0009 (posterior mean)
2. **Process limits**: ±3σ = ±0.013 around target
3. **Update frequency**: Weekly Bayesian updates with new data

### Continuous Improvement
**Learning loop established**:
- **Weekly data collection**: 20-30 measurements
- **Bayesian updates**: Refine parameters continuously
- **Trend monitoring**: Detect process drift early
- **Capability tracking**: Maintain Cp/Cpk targets

### Knowledge Transfer
**Prepare for next product**:
- **Posterior as prior**: Use final estimates for similar components
- **Process understanding**: Document learned behavior
- **Supplier qualification**: Establish process capability database

## Key Benefits Demonstrated

### Statistical Advantages
1. **Optimal estimation**: Mathematically best combination of information
2. **Uncertainty quantification**: Full probability distributions
3. **Sequential learning**: Improves with each data batch
4. **Prior knowledge preservation**: Doesn't discard design intent

### Engineering Benefits
1. **Risk reduction**: Better parameter estimates reduce manufacturing risk
2. **Cost optimization**: More accurate capability assessment enables cost-effective tolerancing
3. **Faster qualification**: Combines design knowledge with limited trial data
4. **Continuous improvement**: Built-in learning mechanism for production

### Business Impact
1. **Time to market**: Faster process qualification with limited data
2. **Quality assurance**: Quantified confidence in process capability
3. **Cost management**: Optimal tolerance allocation based on real capability
4. **Competitive advantage**: Superior process understanding

## Important Considerations

### When Bayesian Analysis Works Best
=== "Ideal Scenarios"
    **Maximum value situations:**
    
    - **New processes**: Limited data but design requirements known
    - **Prototype phases**: Iterative learning with evolving data
    - **Critical applications**: Need both reliability and empirical validation
    - **Supplier development**: Combining specifications with trial runs

=== "Prerequisites"
    **Requirements for success:**
    
    - **Design specifications**: Clear tolerance requirements
    - **Quality data**: Reliable measurement systems
    - **Process stability**: Consistent manufacturing conditions
    - **Statistical literacy**: Understanding of uncertainty concepts

### Limitations and Pitfalls
=== "Data Quality Issues"
    **Garbage in, garbage out:**
    
    - **Biased samples**: Non-representative trial data
    - **Measurement error**: Systematic or random measurement issues
    - **Process instability**: Data from unstable conditions
    - **Sample size**: Too few points for reliable likelihood

=== "Prior Specification"
    **Prior choice matters:**
    
    - **Over-confident priors**: Too narrow initial assumptions
    - **Under-confident priors**: Unnecessarily wide uncertainty
    - **Wrong distribution**: Inappropriate statistical model
    - **Unrealistic parameters**: Physically impossible values

### Validation and Verification
**Always validate Bayesian results**:

1. **Visual inspection**: Do the three curves make sense?
2. **Parameter reasonableness**: Are posterior estimates physically plausible?
3. **Convergence checking**: Did the updating process converge properly?
4. **Cross-validation**: Test predictions against held-out data

## Advanced Techniques

### Prior Sensitivity Analysis
**Test robustness of results**:

1. **Try different priors**: Vary initial σ by ±50%
2. **Compare posteriors**: How much do results change?
3. **Convergence assessment**: Do different priors converge to similar posteriors?

### Model Selection
**Choose best distribution**:

1. **Compare fits**: Try Normal, Gamma, Lognormal
2. **Visual assessment**: Which best matches data pattern?
3. **Statistical criteria**: Use AIC/BIC if available
4. **Engineering judgment**: Consider physical process mechanisms

### Production Scaling
**Extend to full production**:

1. **Batch size planning**: How many samples needed for updates?
2. **Update frequency**: Weekly, monthly, or trigger-based?
3. **Control limits**: Set statistical process control boundaries
4. **Drift detection**: Monitor for parameter changes over time

## Practical Checklist

### Before Starting Bayesian Analysis
- [ ] **Clear specifications**: Well-defined nominal and tolerances
- [ ] **Quality data**: Calibrated measurement system
- [ ] **Stable process**: Consistent manufacturing conditions
- [ ] **Representative samples**: Data reflects actual production intent

### During Analysis
- [ ] **Visual validation**: Three-curve plot makes engineering sense
- [ ] **Parameter reasonableness**: Posterior estimates are physically plausible
- [ ] **Uncertainty reduction**: Posterior is more confident than prior or likelihood alone
- [ ] **Sequential consistency**: Multiple updates show convergence

### After Analysis
- [ ] **Documentation**: Record prior assumptions and data sources
- [ ] **Validation plan**: Define how to verify predictions
- [ ] **Monitoring strategy**: Plan for ongoing data collection
- [ ] **Knowledge transfer**: Prepare learnings for future projects

## Mathematical Deep Dive

### Conjugate Updating (Normal Distribution)
**Analytical solution for Normal case**:

**Prior**: μ ~ N(μ₀, σ₀²)
```
μ₀ = 50.000 (design nominal)
σ₀² = (0.0067)² (design uncertainty)
```

**Data**: x₁, x₂, ..., xₙ ~ N(μ, σ²)
```
n = 25 (sample size)
x̄ = 50.002 (sample mean)
s² = (0.008)² (sample variance)
```

**Posterior**: μ | data ~ N(μₙ, σₙ²)
```
Precision updating:
τ₀ = 1/σ₀² (prior precision)
τₙ = n/s² (data precision)

μₙ = (τ₀μ₀ + τₙx̄)/(τ₀ + τₙ)
σₙ² = 1/(τ₀ + τₙ)
```

### Information Integration
**How much each source contributes**:

```
Prior weight = τ₀/(τ₀ + τₙ)
Data weight = τₙ/(τ₀ + τₙ)

Final estimate = Prior weight × Prior mean + Data weight × Data mean
```

**Example calculation**:
```
τ₀ = 1/(0.0067)² = 22,282
τₙ = 25/(0.008)² = 390,625

Prior weight = 22,282/(22,282 + 390,625) = 0.054
Data weight = 390,625/(22,282 + 390,625) = 0.946

μₙ = 0.054 × 50.000 + 0.946 × 50.002 = 50.0017
```

**Interpretation**: Data gets 94.6% weight due to larger precision (smaller uncertainty).

## Next Steps

### Immediate Actions
1. **Apply to your projects**: Use real component data
2. **Experiment with priors**: Understand sensitivity to assumptions
3. **Compare methods**: Validate against Six Sigma and MLE approaches
4. **Document learnings**: Build organizational knowledge base

### Advanced Applications
1. **Hierarchical models**: Multiple components with shared parameters
2. **Time series**: Parameter evolution over production runs
3. **Multi-variate**: Correlated dimensions in assemblies
4. **Design optimization**: Use Bayesian results for tolerance allocation

### Organizational Implementation
1. **Training**: Educate team on Bayesian thinking
2. **Standards**: Develop company procedures for Bayesian analysis
3. **Tools**: Integrate with existing quality systems
4. **Culture**: Foster data-driven decision making

---

**Congratulations!** You've mastered Bayesian analysis in BayesTolSim. This powerful approach bridges the gap between design theory and manufacturing reality, enabling smarter engineering decisions through principled uncertainty quantification.

**Next**: Explore [Statistical Methods](../methods/six-sigma.md) for deeper theoretical understanding or [Technical Reference](../reference/distributions.md) for implementation details.