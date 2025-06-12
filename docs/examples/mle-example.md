# MLE Analysis Example

This tutorial demonstrates how to use Maximum Likelihood Estimation (MLE) to fit distributions to production data, replacing theoretical assumptions with empirical evidence.

## Scenario Description

**Context**: You have historical production data for a shaft diameter and want to validate your Six Sigma assumptions against actual manufacturing performance.

**Data**: 6 months of production measurements from CNC turning operation
- Target diameter: 25.0 mm
- Design tolerance: ±0.025 mm
- Production volume: 150 measurements

## Data Preparation

### CSV File Format
Create a file named `shaft_diameter_data.csv`:

```csv
Shaft_Diameter
25.0023
24.9987
25.0156
24.9945
25.0089
24.9912
25.0234
24.9876
25.0067
24.9934
...
(150 total measurements)
```

!!! warning "CSV Requirements"
    - **Single column**: Only one column with measurements
    - **Exact name match**: Column name must exactly match dimension name
    - **No headers**: First row should be column name, then data
    - **Numeric format**: Use decimal point (not comma)

### Sample Data Generation (for tutorial)
If you don't have real data, use this Python script to generate realistic sample data:

```python
import numpy as np
import pandas as pd

# Generate realistic manufacturing data
np.random.seed(42)  # For reproducible results

# Simulate tool wear effect (slight drift toward smaller values)
n_samples = 150
base_diameter = 25.0
tool_wear_drift = np.linspace(0, -0.008, n_samples)  # 8 micron drift
random_variation = np.random.normal(0, 0.012, n_samples)  # 12 micron std

measurements = base_diameter + tool_wear_drift + random_variation

# Create DataFrame and save
df = pd.DataFrame({'Shaft_Diameter': measurements})
df.to_csv('shaft_diameter_data.csv', index=False)
print(f"Generated {len(df)} measurements")
print(f"Mean: {df['Shaft_Diameter'].mean():.4f}")
print(f"Std: {df['Shaft_Diameter'].std():.4f}")
```

## Step 1: Setup Baseline Analysis

### Create Six Sigma Baseline
1. **Add dimension**:
   - **Name**: `Shaft_Diameter`
   - **Direction**: `+`
   - **Nominal**: `25.0`
   - **Upper Tolerance**: `0.025`
   - **Lower Tolerance**: `-0.025`
   - **Distribution**: `Normal`

2. **Observe Six Sigma parameters**:
   - **Para1 (μ)**: 25.000000
   - **Para2 (σ)**: 0.008333 (= 0.05/6)

### View Baseline Distribution
1. **Select dimension**: "Shaft_Diameter" in dropdown
2. **Observe plot**: Perfect normal curve centered at 25.0
3. **Check statistics**:
   ```
   Distribution: Normal
   Mean (μ): 25.000
   Std Dev (σ): 0.008
   Cp: 1.000
   Cpk: 1.000
   ```

## Step 2: Apply MLE Analysis

### Upload Production Data
1. **Click**: "MLE Data" button in the Shaft_Diameter row
2. **Select file**: `shaft_diameter_data.csv`
3. **Wait for processing**: Should see "✓ MLE Applied" with green background

### Observe Parameter Changes
After successful upload, parameters should update:
- **Para1**: ~24.996 (actual production mean)
- **Para2**: ~0.015 (actual production standard deviation)

!!! info "Parameter Interpretation"
    - **Mean shift**: Production average slightly below nominal (tool wear effect)
    - **Increased variation**: Real process has more variation than Six Sigma assumption
    - **Distribution validation**: Is normal distribution appropriate?

## Step 3: Analyze MLE Results

### View Updated Distribution
1. **Select dimension**: Should show both histogram and fitted curve
2. **Histogram (gray bars)**: Shows actual data distribution
3. **MLE curve (blue line)**: Best-fit normal distribution

### Compare Statistics
```
=== MLE FIT ===
Distribution: Normal
Mean (μ): 24.996
Std Dev (σ): 0.015
5th Percentile: 24.972
95th Percentile: 25.020
Cp: 0.556
Cpk: 0.489

=== DATA SUMMARY ===
Sample Size: 150
Sample Mean: 24.996
Sample Std: 0.015
Min: 24.962
Max: 25.031
```

### Key Insights from MLE Analysis

**Process Capability Reality Check**:
- **Cp dropped** from 1.000 to 0.556 (below 1.33 requirement)
- **Cpk even lower** at 0.489 (process off-center)
- **Incapable process**: Real manufacturing cannot meet design intent

**Distribution Validation**:
- **Visual fit**: Does blue curve match histogram shape?
- **Residual analysis**: Are there systematic deviations?
- **Tail behavior**: Normal assumption appropriate?

## Step 4: Compare Methods

### Side-by-Side Comparison

| Metric | Six Sigma Theory | MLE Reality | Impact |
|--------|------------------|-------------|---------|
| **Mean** | 25.000 | 24.996 | 4 μm bias |
| **Std Dev** | 0.008 | 0.015 | 87% more variation |
| **Cp** | 1.000 | 0.556 | Process incapable |
| **Cpk** | 1.000 | 0.489 | Off-center + incapable |

### Root Cause Analysis

**Mean Shift (24.996 vs 25.000)**:
- **Tool wear**: Consistent drift toward smaller diameters
- **Machine bias**: Systematic offset in setup
- **Measurement bias**: Calibration issues

**Increased Variation (0.015 vs 0.008)**:
- **Process instability**: Temperature, vibration effects
- **Material variation**: Raw material inconsistency  
- **Operator effects**: Setup and monitoring variations

## Step 5: Engineering Actions

### Immediate Actions
**Process cannot meet current specifications**:

1. **Reject current process**: Cp < 1.0 indicates fundamental incapability
2. **Root cause investigation**: Address mean shift and increased variation
3. **Temporary measures**: 100% inspection until process improved

### Process Improvement Options

=== "Address Mean Shift"
    **Centering the process:**
    
    - **Tool offset adjustment**: Compensate for systematic bias
    - **Machine calibration**: Correct measurement/positioning errors
    - **Setup procedures**: Standardize operator setup methods

=== "Reduce Variation"
    **Tighten process control:**
    
    - **Temperature control**: Stabilize thermal conditions
    - **Vibration isolation**: Reduce machine instability
    - **Material specifications**: Tighter raw material controls
    - **Operator training**: Reduce human variation sources

=== "Design Changes"
    **If process improvement is not cost-effective:**
    
    - **Relax tolerances**: Increase ±0.025 to ±0.040 mm
    - **Alternative processes**: Consider grinding instead of turning
    - **Functional analysis**: Verify tolerance requirements

## Advanced Analysis

### Sequential Analysis
**Track process evolution**:
- Upload weekly data batches
- Compare parameter evolution
- Identify improvement effectiveness

### Integration with Bayesian
**Next step**: Use MLE results to inform Bayesian priors for prototype testing

## Notes on MLE 

### Value of MLE Analysis
1. **Reality check**: Validates or challenges theoretical assumptions
2. **Data-driven decisions**: Replace guesswork with evidence
3. **Process insight**: Reveals actual capability limitations
4. **Risk assessment**: Quantifies real manufacturing risk

### When MLE is Most Valuable
- **Mature processes**: Significant historical data available
- **Critical dimensions**: High-impact tolerance requirements
- **Process validation**: Qualifying new manufacturing methods
- **Supplier assessment**: Evaluating vendor capabilities

### Limitations to Remember
- **Sample size dependent**: Needs adequate data for reliability
- **Snapshot in time**: May not capture long-term variations
- **Distribution assumptions**: Still assumes single distribution type
- **No prior knowledge**: Ignores design intent and specifications

---

**Next**: Learn [Bayesian Analysis](bayesian-example.md) to combine the best of design specifications and production data.