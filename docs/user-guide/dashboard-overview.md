# Dashboard Overview

The BayesTolSim dashboard has 5 cards that guide you through tolerance analysis.

## Card Layout

**Card 1: Header**
Project information and branding.

**Card 2: Dimension Chain Setup**
Add dimensions and configure their properties. This is your main workspace.

**Card 3: Current Dimension Chain**
Visual representation of your assembly and final tolerance settings.

**Card 4: View Distribution**
Analyze individual dimensions in detail.

**Card 5: Final Results**
Monte Carlo simulation results and process capability.

## Typical Workflow

1. **Setup** (Card 2): Add your dimensions
2. **Configure** (Card 3): Set final tolerances  
3. **Analyze** (Card 4): Check individual dimensions
4. **Simulate** (Card 5): Generate results
5. **Interpret**: Make engineering decisions

## Interface Elements

### Buttons
- **Blue buttons**: Primary actions (Run Simulation)
- **Green buttons**: Add items (+ Add Dimension)
- **Red buttons**: Remove items (- Remove Dimension)

### Visual Feedback
- **Green**: Successful operations (MLE applied)
- **Blue**: Bayesian updates applied
- **Red**: Errors or warnings

### Interactive Features
- **Real-time updates**: Changes appear immediately
- **Hover information**: Move mouse over plots for details
- **Click interactions**: Click plots for additional analysis

## Navigation Tips

1. **Start simple**: Begin with 2-3 dimensions
2. **Build gradually**: Add complexity step by step
3. **Check results**: Validate at each step
4. **Use descriptive names**: "Shaft_Length" not "Dim1"
5. **Keep consistent units**: Use mm throughout

## Performance Tips

- Start with 1,000-5,000 samples for testing
- Use 10,000+ samples for final analysis
- Focus on critical dimensions first
- Save screenshots of successful setups

**Next**: Learn [Dimension Setup](dimension-setup.md) to start building your analysis.