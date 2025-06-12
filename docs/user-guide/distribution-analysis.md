# Distribution Analysis

This section lets you examine individual dimensions in detail before running the full simulation.

## Selecting a Dimension

Use the dropdown to select any dimension you've created. The dropdown shows the actual names you entered.

## What You'll See

### Default View (Tolerance-Based)
- **Purple curve**: Shows the theoretical distribution based on your tolerances
- **Statistics**: Mean, standard deviation, process capability

### With MLE Data
- **Gray histogram**: Your actual measurement data
- **Blue curve**: Best-fit distribution to your data
- **Comparison**: See how reality compares to theory

### With Bayesian Data
- **Blue curve**: Your design assumptions (prior)
- **Orange curve**: What your trial data suggests (likelihood)  
- **Green area**: Combined knowledge (posterior)
- **Gray histogram**: Your actual measurements

## Key Statistics

**Mean**: Average value
**Std Dev**: How much variation to expect
**Cp**: Process capability (>1.33 is good)
**Cpk**: Process capability accounting for centering (>1.33 is good)

### MLE Results Include
- **Sample size**: How many measurements
- **Sample statistics**: What your data actually shows
- **Comparison**: Theory vs reality

### Bayesian Results Include
- **Three sections**: Prior, Likelihood, Posterior
- **Updated capability**: Improved estimates combining design and data

## Plot Interactions

**Hover**: Move mouse over curves to see values
**Click**: (On main distribution) Shows cumulative probability

## Interpreting the Results

### Distribution Shape
**Symmetric bell curve**: Good process control
**Skewed right**: Possible tool wear or process drift
**Skewed left**: Unusual, investigate further
**Multiple peaks**: Multiple process modes

### Method Comparison
**Design vs MLE**: Are your assumptions correct?
**Prior vs Posterior**: How much did data change your estimates?

### Capability Assessment
**Cp, Cpk > 1.33**: Process capable
**Cp, Cpk < 1.33**: Process needs improvement
**Cpk much less than Cp**: Process off-center

## Common Issues

**Empty plot**: Check that parameters are set and positive
**Weird shape**: Verify distribution choice matches your process
**Poor fit**: Try different distribution or check data quality

## Quick Actions

- Compare different dimensions by switching dropdown selection
- Check if MLE results match your expectations
- Verify Bayesian updates make engineering sense
- Note any dimensions that need attention

**Next**: Learn about [Monte Carlo Simulation](monte-carlo.md) to get final assembly results.