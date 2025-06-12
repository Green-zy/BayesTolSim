# Monte Carlo Simulation

This is where you run the final analysis to see how your complete assembly will perform.

## Before You Start

Make sure you have:
- At least one dimension defined
- Final dimension tolerances set (in Card 3)
- All dimension parameters filled in

## Sample Size

Choose how many virtual assemblies to simulate:

**1,000 - 5,000**: Quick testing, good for initial checks
**10,000 - 50,000**: Standard analysis, recommended for most cases  
**100,000+**: High precision, use for critical applications

**Think of it as**: How many parts would you manufacture? More samples = more accurate results but takes longer.

## Running the Simulation

1. Set your sample size
2. Click "Run Simulation"
3. Wait a few seconds for results

## Understanding Results

### The Purple Curve
Shows the distribution of your final assembly dimension:
- **Center**: Expected final dimension
- **Width**: How much variation to expect
- **Shape**: Pattern of variation

### Key Statistics

**Mean**: Average final dimension
**Std Dev**: Typical variation
**Min/Max**: Extreme values in simulation
**5th/95th Percentile**: Range containing 90% of assemblies

### Process Capability

**Cp**: Process capability
- **> 1.33**: Good (capable process)
- **1.0 - 1.33**: Marginal (monitor closely)
- **< 1.0**: Poor (process cannot meet requirements)

**Cpk**: Process capability with centering
- **> 1.33**: Good and well-centered
- **Much less than Cp**: Process off-center

### Defect Rates

**CDF left of LSL**: Percentage of undersized assemblies
**CDF right of USL**: Percentage of oversized assemblies

Example: 0.0023 = 0.23% = 2,300 parts per million defective

## Plot Interactions

**Hover**: Move mouse over curve to see probability information
**Click**: Click anywhere on curve to see cumulative probability up to that point (red shaded area)

## Interpreting Results

### Shape Analysis
**Bell curve**: Normal, well-controlled assembly process
**Skewed**: One or more dimensions contribute asymmetric variation
**Multiple peaks**: Check individual dimensions for issues

### Capability Assessment
**Excellent (Cp > 1.67)**: Process exceeds requirements, consider relaxing tolerances
**Good (Cp 1.33-1.67)**: Process meets requirements
**Marginal (Cp 1.0-1.33)**: Monitor closely, consider improvements
**Poor (Cp < 1.0)**: Must improve process or relax tolerances

### Defect Rate Guidance
**< 0.1% (1,000 PPM)**: Excellent quality
**0.1-0.5% (1,000-5,000 PPM)**: Good quality
**> 0.5% (5,000+ PPM)**: Needs improvement

## Engineering Actions

### If Results Are Good
- Document the successful configuration
- Consider if tolerances could be relaxed to save cost
- Use this process for similar assemblies

### If Results Are Poor
- Identify which dimensions contribute most variation
- Tighten control on critical dimensions
- Consider alternative manufacturing methods
- Relax design tolerances if functionally acceptable

### If Results Are Marginal
- Implement process monitoring
- Consider slight improvements
- Plan for quality control measures

## Common Issues

**No results**: Check that final tolerances are set
**Unrealistic results**: Verify dimension setup and parameters
**Simulation takes too long**: Reduce sample size for testing

**Next**: Explore the [Examples](../examples/basic-example.md) for complete walkthroughs or learn about [Statistical Methods](../methods/six-sigma.md).