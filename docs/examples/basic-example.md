# Basic Example: Shaft-Housing Assembly

This example walks through a complete tolerance analysis from start to finish.

## Assembly Description

We'll analyze a simple assembly:
- **Shaft length**: 50.0 ±0.05 mm
- **Housing depth**: 48.0 ±0.03 mm (subtracts from total)
- **End cap thickness**: 2.5 ±0.02 mm

**Expected final dimension**: 50 - 48 + 2.5 = 4.5 mm

## Step 1: Add Dimensions

### First Dimension (Shaft)
1. Click **"+ Add Dimension"**
2. Fill in:
   - **Name**: `Shaft_Length`
   - **Direction**: `+`
   - **Nominal**: `50.0`
   - **Upper Tolerance**: `0.05`
   - **Lower Tolerance**: `-0.05`
   - **Distribution**: `Normal`

Notice the parameters auto-fill:
- **Para1**: 50.000000 (mean)
- **Para2**: 0.016667 (standard deviation = 0.1/6)

### Second Dimension (Housing)
1. Click **"+ Add Dimension"** again
2. Fill in:
   - **Name**: `Housing_Depth`
   - **Direction**: `-` (subtracts)
   - **Nominal**: `48.0`
   - **Upper Tolerance**: `0.03`
   - **Lower Tolerance**: `-0.03`
   - **Distribution**: `Normal`

### Third Dimension (End Cap)
1. Click **"+ Add Dimension"** once more
2. Fill in:
   - **Name**: `End_Cap`
   - **Direction**: `+`
   - **Nominal**: `2.5`
   - **Upper Tolerance**: `0.02`
   - **Lower Tolerance**: `-0.02`
   - **Distribution**: `Normal`

## Step 2: Check the Chain

Look at the "Current Dimension Chain" plot:
- Blue line: Shaft (50 mm, positive)
- Red line: Housing (48 mm, negative)
- Blue line: End cap (2.5 mm, positive)
- Total: Should show about 4.5 mm

## Step 3: Set Final Tolerances

Before simulation, specify what's acceptable for the final assembly:
- **Upper Tolerance**: `0.1`
- **Lower Tolerance**: `-0.1`

This means final dimension of 4.5 ±0.1 mm is acceptable.

## Step 4: Analyze Individual Dimensions (Optional)

1. Go to "View Distribution of a Dimension"
2. Select "Shaft_Length" from dropdown
3. See the purple curve showing normal distribution
4. Check statistics:
   ```
   Mean: 50.000
   Std Dev: 0.017
   Cp: 1.000
   Cpk: 1.000
   ```

This shows the process exactly uses the full tolerance (Cp = 1.0).

## Step 5: Run Simulation

1. Set **"Number of Samples"** to `10000`
2. Click **"Run Simulation"**
3. Wait 1-3 seconds

## Step 6: Interpret Results

### Expected Results
```
Mean: 4.5001
Std Dev: 0.0202
Cp: 2.475
Cpk: 2.475
CDF left of LSL: 0.0000
CDF right of USL: 0.0000
```

### What This Means

**Process Capability**: Cp = 2.475 is excellent (well above 1.33 minimum)
**Centering**: Cpk = Cp means perfectly centered
**Quality**: Zero defect rate (CDF = 0.0000)
**Variation**: Final standard deviation (0.0202) is much smaller than individual components

### Engineering Conclusions

**Current Design**: Over-specified for quality requirements
**Opportunity**: Could relax tolerances to reduce manufacturing cost
**Recommendation**: 
- Could increase shaft tolerance from ±0.05 to ±0.08 mm
- Could increase housing tolerance from ±0.03 to ±0.05 mm
- Maintain Cp > 1.33 for good margin

### Why the Assembly is Better than Components

The assembly variation follows the "root sum of squares" rule:
√(0.0167² + 0.0100² + 0.0067²) ≈ 0.0202

This is much smaller than the worst individual component, showing the statistical advantage of assemblies.

## Next Steps

Now that you understand the basics:

1. **Try different distributions**: Change shaft to "Lognormal" and see the effect
2. **Modify tolerances**: Make them tighter or looser and observe capability changes
3. **Add more dimensions**: Practice with more complex assemblies
4. **Upload data**: Try the MLE or Bayesian features with sample data

**Advanced Examples**:
- [MLE Analysis with Production Data](mle-example.md)
- [Bayesian Analysis with Trial Data](bayesian-example.md)

This example shows how statistical tolerance analysis provides insights beyond traditional worst-case calculations, helping optimize both quality and cost.