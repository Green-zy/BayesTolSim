# Dimension Chain Setup

This is where you define the parts of your assembly. Each dimension represents a feature that affects the final assembly size.

## Adding Dimensions

- **+ Add Dimension**: Creates a new dimension
- **- Remove Dimension**: Removes the last dimension

You can add up to 20 dimensions in one analysis.

## Input Fields

### 1. Name
Give each dimension a descriptive name:
- Good: "Shaft_Length", "Housing_Depth", "Bearing_Width"
- Avoid: "Dim1", "Part A", names with spaces

### 2. Direction
Choose how this dimension affects the assembly:

**+ (Plus)**: Adds to the final size
- Examples: shaft lengths, spacer thicknesses, wall thicknesses

**- (Minus)**: Subtracts from the final size  
- Examples: hole depths, cavities, material removal

**Visual**: Blue lines show + directions, red lines show - directions

### 3. Nominal Value
The target dimension from your drawings (in mm).
- Example: 50.0, 25.5, 12.75

### 4. Tolerances

**Upper Tolerance**: Maximum allowed above nominal
- Example: +0.05 (enter as 0.05)

**Lower Tolerance**: Maximum allowed below nominal  
- Example: -0.03 (enter as -0.03)

The system calculates: Nominal + Tolerance = Specification Limit

### 5. Distribution Type

Choose the statistical model for manufacturing variation:

**Normal** (Start here for most cases)
- Use when: Standard machining, turning, milling
- Characteristics: Symmetric variation around target
- Best for: Most manufacturing processes

**Lognormal** (For wear-related processes)
- Use when: Tool wear affects the process
- Example: Hole diameters (tools wear and holes get smaller)
- Characteristics: Slightly skewed toward smaller values

**Gamma** (For complex processes)
- Use when: Multiple factors affect variation
- Examples: Injection molding, composite parts, complex assemblies
- Characteristics: Can handle various patterns of variation

**Uniform** (For highly controlled processes)
- Use when: Very tight process control or conservative analysis
- Examples: Precision grinding, calibrated fixtures
- Characteristics: Equal probability across the tolerance range

### 6. Parameters (Para1 & Para2)

The system automatically calculates these from your tolerances:

**Normal Distribution**:
- Para1 (μ): Your nominal value
- Para2 (σ): Tolerance range ÷ 6

**Advanced**: You can override these with mathematical expressions if needed.

### 7. Data Upload (Optional)

**MLE Data**: Upload production measurement data
- File: CSV with single column
- Column name must exactly match dimension name
- Effect: Uses actual manufacturing data instead of design assumptions

**Bayes Data**: Upload prototype/trial data  
- File: CSV with single column
- Prerequisite: Must set tolerances first
- Effect: Combines design specs with trial measurements

**Important**: You can use either MLE or Bayesian on a dimension, but not both.

## Chain Visualization

The plot shows your dimension stack-up:
- **Blue lines**: + (additive) dimensions
- **Red lines**: - (subtractive) dimensions
- **Total**: Final assembly dimension

Example: Shaft(+) - Housing(-) + Cap(+) = Final dimension

## Final Tolerances

Before running simulation, specify acceptable limits for the complete assembly:

**Upper Tolerance**: Maximum acceptable deviation above nominal final dimension
**Lower Tolerance**: Maximum acceptable deviation below nominal final dimension

These are used to calculate:
- Process capability (Cp, Cpk)
- Defect rates
- Quality metrics

## CSV File Format

If uploading data, use this exact format:

```
Dimension_Name
25.0023
24.9987
25.0156
24.9945
```

Requirements:
- Single column only
- Column header must match dimension name exactly
- No extra spaces or characters
- Use decimal point (not comma)

**Next**: Learn about [Distribution Analysis](distribution-analysis.md) to examine your dimensions in detail.