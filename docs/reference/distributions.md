# Distribution Types Reference

BayesTolSim supports four probability distributions. This guide helps you choose the right one for your manufacturing process.

## Normal Distribution

### When to Use
**Most manufacturing processes** - This is your default choice.

**Examples:**
- Machined surfaces (turning, milling, grinding)
- Standard assembly processes
- Most injection molded parts
- Any process with random variation around a target

**Characteristics:**
- Symmetric bell curve
- Most values near the center (nominal)
- Equal chance of being above or below target

### How Parameters Are Set
From your tolerances:
- **Mean (μ)** = Your nominal value
- **Standard deviation (σ)** = Tolerance range ÷ 6

**Example:** 50.0 ±0.1mm becomes μ=50.0, σ=0.033

## Lognormal Distribution

### When to Use
**Processes affected by tool wear or degradation**

**Examples:**
- Hole diameters (drill bits wear and holes get smaller)
- Surface finish (tends to get rougher over time)
- Part dimensions affected by tool wear
- Processes where values cannot be negative

**Characteristics:**
- Slightly skewed toward smaller values
- Cannot produce negative dimensions
- Accounts for gradual process drift

### Engineering Insight
Tool wear typically makes holes smaller, surfaces rougher, or dimensions drift in one direction. Lognormal accounts for this tendency.

## Gamma Distribution

### When to Use
**Complex processes with multiple sources of variation**

**Examples:**
- Injection molding (heating, cooling, pressure effects)
- Composite part manufacturing
- Complex assemblies with multiple process steps
- Chemical or thermal processes

**Characteristics:**
- Very flexible shape
- Can model almost any pattern of variation
- Good when you're not sure about the variation pattern

### Engineering Insight
When your process has many variables affecting the outcome, Gamma can adapt to fit the actual pattern better than Normal or Lognormal.

## Uniform Distribution

### When to Use
**Highly controlled processes or conservative analysis**

**Examples:**
- Precision grinding within very tight limits
- Parts made on calibrated fixtures
- When you want a conservative "worst-case" analysis
- When you have no data and want to be safe

**Characteristics:**
- Equal probability across the entire tolerance range
- Most conservative assumption
- No preference for center vs edges of tolerance

### Engineering Insight
Use this when your process is so tightly controlled that any value within tolerance is equally likely, or when you want to be conservative.

## Selection Guide

### Quick Decision Tree

**Start here:** Do you have measurement data?
- **No data**: Use Normal (works for 80% of cases)
- **Have data**: Upload it and try MLE to see which fits best

**If Normal doesn't fit your data well:**
- **Tool wear issues**: Try Lognormal
- **Complex process**: Try Gamma
- **Very tight control**: Try Uniform

### Process-Based Recommendations

| Process Type | Recommended Distribution |
|--------------|-------------------------|
| **Machining (turning, milling)** | Normal |
| **Drilling, reaming** | Lognormal |
| **Injection molding** | Gamma |
| **Precision grinding** | Uniform |
| **Assembly operations** | Normal |
| **Composite manufacturing** | Gamma |

## Data Requirements for MLE

If uploading measurement data:

| Distribution | Minimum Samples | Recommended |
|--------------|----------------|-------------|
| **Normal** | 20 | 50+ |
| **Lognormal** | 30 | 75+ |
| **Gamma** | 50 | 100+ |
| **Uniform** | 15 | 30+ |

## Troubleshooting Distribution Choice

### Signs You Picked Wrong Distribution
- Parameters seem unrealistic
- Poor fit between curve and histogram (with MLE)
- Process capability much different than expected

### Solutions
- Try a different distribution
- Check your measurement data for outliers
- Consider if your process has multiple modes
- Verify units and data quality

## Advanced Tips

### When You Have Data
1. Start with Normal as baseline
2. Upload data using MLE
3. Check visual fit between curve and histogram
4. Try other distributions if fit is poor
5. Choose the one that best matches your data

### When You Don't Have Data
1. Use Normal for most cases
2. Consider Lognormal if tool wear is significant
3. Use Uniform if you want to be conservative
4. Gamma is rarely needed without data

### Bayesian Analysis
- Your distribution choice affects the prior
- Start with Normal unless you have strong reasons otherwise
- The data will help refine the choice through updating

**Next**: Return to [User Guide](../user-guide/dashboard-overview.md) for practical application or explore our [Examples](../examples/basic-example.md) for hands-on tutorials.