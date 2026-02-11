# F1 Tyre Strategy Analysis & Optimization

A data-driven framework for analyzing and optimizing Formula 1 pit stop strategies using tyre degradation models, Monte Carlo simulations, and context-aware decision metrics.

## Overview

This project simulates tyre degradation across F1 races and employs probabilistic methods to recommend optimal pit stop strategies. The framework incorporates track-specific degradation factors, driver behavior patterns, and uncertainty quantification to support real-time strategy decisions.

### Key Features

- **Tyre Degradation Modeling**: Physics-informed degradation curves for Soft, Medium, and Hard compounds
- **Multi-Scenario Analysis**: One-stop vs. two-stop strategy comparison with Monte Carlo sampling
- **Context Awareness**: Track degradation factors and driver behavior influence on tyre wear
- **Risk Quantification**: Win probability, expected regret, and confidence intervals for strategy selection
- **Driver Profiling**: Data-driven classification of driver styles (Aggressive, Balanced, TyreSaver)
- **Grid-Wide Prediction**: Automated strategy recommendations for all drivers across all tracks

## Project Structure

```
├── README.md
├── requirements.txt
├── tyre-degradation-simulation.ipynb          # Main analysis notebook
├── tyre-degradation-simulation layer-1.ipynb  # Alternative notebook version
├── monte_carlo_strategy_summary.csv           # Summary results
├── data/
│   └── processed/
│       └── race_data.csv                      # Historical race telemetry
├── outputs/
│   └── final_strategy_predictions.csv         # Grid-wide predictions
└── src/
    ├── data_loader.py                         # Data loading utilities
    ├── degradation.py                         # Tyre degradation models
    ├── driver_profiles.py                     # Driver behavior profiles
    ├── strategy.py                            # Strategy simulation functions
    ├── track_profiles.py                      # Track-specific parameters
    └── utils.py                               # Helper utilities
```

## Data & Parameters

### Track Degradation Factors

Tracks are classified by tyre degradation intensity:

- **Low degradation** (0.7–0.8): Monaco, Baku, Monza
- **Medium** (1.0): Silverstone, Mexico, Abu Dhabi
- **Medium-High** (1.1): Barcelona, Singapore
- **High** (1.2): Spa, Suzuka
- **Very High** (1.3): Bahrain, Hungaroring

### Driver Style Classifications

| Style | Factor | Examples |
|-------|--------|----------|
| Aggressive | 1.1 | Max Verstappen, Charles Leclerc |
| Balanced | 1.0 | Carlos Sainz, Lando Norris, George Russell |
| TyreSaver | 0.9 | Lewis Hamilton, Sergio Pérez, Fernando Alonso |

### Tyre Compounds

- **Soft**: Fast but high degradation (α_base ≈ 0.03)
- **Medium**: Balanced performance and wear (α_base ≈ 0.025)
- **Hard**: Durable but slower (α_base ≈ 0.02)

## Analysis Layers

### Layer 1: Baseline Framework
Establishes fundamental one-stop and two-stop strategy optimization across tyre compounds for a standard 70-lap race.

**Outputs**:
- Optimal pit lap positions for each compound
- Comparison of strategy costs
- Monte Carlo uncertainty estimates

### Layer 2: Context-Aware Insights
Extends analysis to incorporate track characteristics and driver behavior, demonstrating that strategy optimality is context-dependent.

**Key Findings**:
- High-degradation tracks amplify benefits of multi-stop strategies
- Driver style modulates degradation rates by 10–20%
- Strategy recommendations vary significantly by track

### Layer 3: Risk-Aware Decision Making
Introduces probabilistic decision metrics beyond expected value, supporting risk-conscious strategy selection.

**Decision Metrics**:
- **Win Probability**: Likelihood that strategy A outperforms strategy B across uncertainty
- **Expected Regret**: Mean opportunity cost of suboptimal choice
- **Confidence Intervals**: 95% CI on degradation costs

## Usage

### Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Analysis

Open and execute the main notebook:

```bash
jupyter notebook tyre-degradation-simulation.ipynb
```

The notebook includes:
1. Initialization and data loading
2. Single-compound baseline analysis
3. Multi-compound comparison
4. Track-aware scenario analysis
5. Driver-aware simulations
6. Grid-wide strategy predictions

### Interpreting Results

**Key Output Files**:

- `monte_carlo_strategy_summary.csv`: Mean/std costs for each compound-strategy pair
- `outputs/final_strategy_predictions.csv`: Best-strategy recommendations for all driver-track combinations
- Visualizations in notebook: Strategy cost curves, win probabilities, driver degradation indices

### Example: Predict Strategy for a Specific Driver & Track

```python
from src.strategy import predict_race_strategy

result = predict_race_strategy(
    track="Hungaroring",
    driver="Lewis Hamilton",
    compound="Soft"
)

print(f"Best Strategy: {result['best_strategy']}")
print(f"Two-stop Win Probability: {result['two_stop_win_probability']:.2%}")
print(result['comparison_table'])
```

## Methodology

### Tyre Degradation Model

Relative performance decays as a function of lap count:

$$P(L) = 1 - \alpha \cdot L^2$$

where:
- **L** = tyre age (laps)
- **α** = degradation rate (compound-dependent, track-adjusted, driver-adjusted)

### Strategy Simulation

For each pit strategy, total degradation cost is computed as:

$$\text{Cost} = \sum_i P(L_i)$$

where $L_i$ is the tyre age during segment $i$.

### Monte Carlo Framework

For each strategy:
1. Sample α from $\mathcal{N}(\mu_\alpha, \sigma_\alpha)$
2. Simulate race and compute total cost
3. Repeat n=1000–3000 times
4. Compute mean, std, confidence intervals, and win probability

## Results

### Baseline Findings
- **Two-stop strategies** typically achieve 5–15% lower degradation cost
- **Compound selection** significantly impacts optimal pit timing
- **Uncertainty** (95% CI) spans ~10–20% of mean cost

### Track Effects
- **Low-degradation tracks** (Monaco): One-stop more competitive
- **High-degradation tracks** (Hungaroring): Two-stop strongly preferred

### Driver Effects
- **Aggressive drivers**: ~5–10% higher degradation; requires earlier pit stops
- **Tyre-savers**: ~5–10% lower degradation; can extend stints

## Author & License

**Author**: Sneha

**Repository**: [f1-tyre-strategy-colab](https://github.com/Sneha73685/f1-tyre-strategy-colab)

This project is open-source and available for research and educational use.

## References

- *Tyre Degradation Dynamics in Formula 1 Racing*
- Historical F1 race telemetry and pit stop data (2020–2024)
- Monte Carlo Methods for Uncertainty Quantification

## Contact & Contributions

For questions, feedback, or contributions, please open an issue or pull request on the repository.

---

**Last Updated**: February 2026
