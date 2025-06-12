# Getting Started

## Accessing BayesTolSim

BayesTolSim runs in your web browser - no software installation needed.

1. Open your web browser
2. Navigate to the BayesTolSim URL
3. Start your analysis immediately

## Your First Analysis (5 minutes)

Let's analyze a simple shaft-housing assembly:

### Step 1: Add Dimensions
1. Click **"+ Add Dimension"** 
2. Fill in the first dimension:
   - **Name**: `Shaft`
   - **Direction**: `+` 
   - **Nominal**: `100`
   - **Upper Tolerance**: `0.05`
   - **Lower Tolerance**: `-0.05`
   - **Distribution**: `Normal`

3. Add the second dimension:
   - **Name**: `Housing`
   - **Direction**: `-`
   - **Nominal**: `98`
   - **Upper Tolerance**: `0.03`
   - **Lower Tolerance**: `-0.03`
   - **Distribution**: `Normal`

### Step 2: Set Final Tolerances
In the "Current Dimension Chain" section:
- **Upper Tolerance**: `0.1`
- **Lower Tolerance**: `-0.1`

### Step 3: Run Simulation
1. Set **"Number of Samples"** to `10000`
2. Click **"Run Simulation"**
3. View your results in seconds

## Key Features

### Three Analysis Methods

**Normal Analysis (Start Here)**
- Use your design tolerances
- Get instant results
- Industry standard approach

**MLE Analysis (If You Have Data)**
- Upload your measurement data
- See what actually happens in production
- Compare with design assumptions

**Bayesian Analysis (Advanced)**
- Combine design specs with prototype data
- Best of both approaches
- Continuous improvement

### Data Upload (Optional)
If you have measurement data:
- Prepare CSV file with single column
- Column name must match dimension name exactly
- Upload via "MLE Data" or "Bayes Data" buttons

Example CSV format:
```
Shaft_Length
50.023
49.987
50.156
...
```

## Dashboard Layout

**Card 1**: Project header  
**Card 2**: Add and configure dimensions  
**Card 3**: View dimension chain and set final tolerances  
**Card 4**: Analyze individual dimensions  
**Card 5**: Run simulation and view results  

## Quick Tips

- Use descriptive dimension names
- Keep all measurements in mm
- Start with 10,000 samples for good accuracy
- Normal distribution works for most cases
- Check Cp and Cpk values (>1.33 is good)

## Getting Help

- Email: robbiezhou1@gmail.com
- Documentation: Continue reading for detailed guides
- Examples: Step-by-step tutorials available

**Ready to learn more?** Continue to the [User Guide](user-guide/dashboard-overview.md) or try a [Complete Example](examples/basic-example.md).