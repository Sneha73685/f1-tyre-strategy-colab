# 🏎️ F1 Tyre Strategy Optimizer

> **Data-driven pit stop strategy recommendations for Formula 1 racing**

A comprehensive probabilistic framework for simulating tyre degradation and optimizing pit stop strategies across all F1 tracks and drivers. Combines physics-informed degradation modeling with Monte Carlo uncertainty quantification to deliver race-ready strategy insights.

---

## 🎯 What This Does

Predicts the **optimal pit stop strategy** for any Formula 1 driver at any track by:

1. **Modeling tyre degradation** through quadratic performance decay curves (track and driver-aware)
2. **Simulating pit strategies** (one-stop vs. two-stop) across thousands of uncertain scenarios
3. **Quantifying risk** through win probabilities, expected regret, and confidence intervals
4. **Recommending actions** with statistical confidence

**Example Output:**
```
Track: Hungaroring | Driver: Lewis Hamilton | Compound: Soft
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Best Strategy: Two-stop
Two-stop Win Probability: 78.3%

Strategy Comparison:
├─ One-stop  | Mean Cost: 42.5 ± 3.2 (95% CI: 36.8–49.1)
└─ Two-stop  | Mean Cost: 38.9 ± 2.8 (95% CI: 33.6–44.7)
```

---

## 📦 Project Structure

```
f1-tyre-strategy-colab/
├── tyre-degradation-simulation.ipynb    # Main analysis (3 layers)
├── data/
│   └── processed/
│       └── race_data.csv                # Historical telemetry
├── outputs/
│   ├── final_strategy_predictions.csv   # 120 driver-track combos
│   └── monte_carlo_strategy_summary.csv # Aggregate results
├── src/
│   ├── degradation.py                   # TyreDegradationModel class
│   ├── strategy.py                      # Simulation & prediction functions
│   ├── data_loader.py                   # CSV utilities
│   ├── driver_profiles.py               # Driver metadata
│   └── track_profiles.py                # Track parameters
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### Installation

```bash
# Clone the repo
git clone https://github.com/Sneha73685/f1-tyre-strategy-colab.git
cd f1-tyre-strategy-colab

# Install dependencies
pip install -r requirements.txt
```

### Run the Analysis

```bash
jupyter notebook tyre-degradation-simulation.ipynb
```

The notebook is organized into **3 progressive layers**:

| Layer | Focus | Output |
|-------|-------|--------|
| **1** | Baseline degradation modeling & strategy optimization | Per-compound pit timing |
| **2** | Track & driver context integration | Context-aware recommendations |
| **3** | Risk-aware decision making | Win probabilities & regret analysis |

### Quick API Usage

```python
from src.strategy import predict_race_strategy

# Get strategy recommendation
result = predict_race_strategy(
    track="Monaco",
    driver="Max Verstappen",
    compound="Soft",
    n_sim=3000
)

print(result['best_strategy'])                    # "Two-stop"
print(f"{result['two_stop_win_probability']:.1%}") # "75.4%"
print(result['comparison_table'])
#           Strategy  Mean Cost  Std Dev
# 0  One-stop     45.2      3.1
# 1  Two-stop     39.8      2.9
```

---

## 🔬 Technical Approach

### Tyre Degradation Model

**Quadratic decay** of relative performance vs. tyre age:

$$P(L) = 1 - \alpha \cdot L^2$$

Where:
- $L$ = stint length (laps)
- $\alpha$ = compound-specific degradation rate
  - Soft: $\alpha \approx 0.03$
  - Medium: $\alpha \approx 0.025$
  - Hard: $\alpha \approx 0.02$

**Context modulation:**
$$\alpha_{\text{adjusted}} = \alpha_{\text{base}} \times f_{\text{track}} \times f_{\text{driver}}$$

- $f_{\text{track}}$: Monaco (0.7) to Hungaroring (1.3)
- $f_{\text{driver}}$: TyreSaver (0.9) to Aggressive (1.1)

### Strategy Cost Function

Total race cost sums degradation across stints:

$$\text{Cost} = \sum_{\text{stints}} \int_0^{L_i} (1 - \alpha L^2) \, dL$$

| Strategy | Pit Laps | Optimization |
|----------|----------|--------------|
| One-stop | Single lap (optimized 15–40) | Grid search |
| Two-stop | Two laps (optimized 15–50) | 2D grid search |

### Monte Carlo Uncertainty Quantification

For robust recommendations:

```
For each simulation (n=1000–3000):
  1. Sample α ~ Normal(μ_context, σ=0.005)
  2. Simulate race with sampled degradation
  3. Record total cost
  
Compute: mean, std, 95% CI, win probability
```

**Win Probability:** $P(\text{Strategy A} < \text{Strategy B})$

---

## 📊 Key Results

### Compound Performance (Baseline)
- **Soft**: Fastest but short-lived → One-stop viable only on slow-lap tracks
- **Medium**: Most common choice → Balanced pit flexibility  
- **Hard**: Durable but risky → Two-stops often required to avoid late-race pace loss

### Track Sensitivity
| Track Group | Degradation | Preference |
|-------------|-------------|-----------|
| Street circuits (Monaco, Singapore) | Low (0.7–0.8) | One-stop competitive |
| Medium circuits (Silverstone, Barcelona) | Medium (1.0–1.1) | Mixed strategies |
| High-wear circuits (Hungaroring, Bahrain) | High (1.2–1.3) | Two-stop dominant |

### Driver Effects
- **Aggressive drivers** (Verstappen, Leclerc) → 5–10% faster but 5–10% higher wear
- **Balanced drivers** (Sainz, Norris) → Middle of pack
- **Tyre-savers** (Hamilton, Alonso) → Gentler on rubber, enables longer stints

---

## 📈 Phase 2: Realistic Race Simulation

The notebook includes an extended `PHASE 2` section with real-world race dynamics:

### Dynamic Lap Times
```python
lap_time = base_lap_time 
         + degradation_penalty 
         + fuel_weight_penalty    # 0–2.5s
         + cold_tyre_penalty      # 0–1.2s (first 2 laps)
```

### Safety Car & Traffic
- **Safety car probability** by track (Monaco: 60%, Monza: 15%)
- **Pit rejoin difficulty** (Monaco hard vs. Monza easy)
- **Traffic penalties** during normal racing

### Full Simulation API
```python
result = compare_strategies_full(
    track="Monaco",
    driver="Lewis Hamilton",
    compound="Soft",
    n_sim=3000  # Race time (seconds) instead of cost
)
```

---

## 📁 Output Files

| File | Contents | Size |
|------|----------|------|
| `monte_carlo_strategy_summary.csv` | 6 rows (3 compounds × 2 strategies) | <1 KB |
| `outputs/final_strategy_predictions.csv` | 120 rows (12 tracks × 10 drivers) | ~5 KB |

Both include: mean cost, std dev, 95% CI bounds, win probability

---

## 🛠️ Customization

### Adjust Simulation Fidelity

```python
# In notebook, early cell
FAST_MODE = True  # Toggle for speed vs. accuracy

if FAST_MODE:
    N_SIM_SMALL = 200   # Layer 1 baseline
    N_SIM_MED = 300     # Layer 2 context
    N_SIM_FULL = 500    # Layer 3 & Phase 2
else:
    N_SIM_SMALL = 1000
    N_SIM_MED = 2000
    N_SIM_FULL = 5000
```

### Add a New Track

```python
TRACK_DEGRADATION_FACTORS["NewTrack"] = 1.15
SAFETY_CAR_PROBABILITY["NewTrack"] = 0.4
OVERTAKE_DIFFICULTY["NewTrack"] = 0.65
BASE_LAP_TIMES["NewTrack"] = 92  # seconds
```

### Add a New Driver

```python
DRIVER_STYLE_MAP["Your Driver"] = "Aggressive"  # or "Balanced", "TyreSaver"
```

---

## 🔍 Interpreting Output

### Win Probability
- **75%**: Strategy A is 75% likely to be faster than Strategy B across uncertainty
- **50%**: Strategies are equivalent; other factors (driver preference, tire supply) decide

### Expected Regret
- **2.5 seconds**: If you pick worse strategy, expect to lose ~2.5s vs. optimal
- **0.5 seconds**: Strategies are nearly equivalent; pick either

### Confidence Interval (95% CI)
- Shows range of outcomes accounting for model uncertainty
- Narrower CI = more confident prediction

---

## 🎓 Methodology References

- Quadratic tyre degradation: Standard F1 modeling approach
- Monte Carlo framework: Uncertainty quantification best practice
- Driver profiling: Derived from telemetry across 2020–2024 seasons
- Track factors: Empirical pit stop data from official race broadcasts

---

## 📝 License & Attribution

**Author**: Sneha  
**Repository**: [f1-tyre-strategy-colab](https://github.com/Sneha73685/f1-tyre-strategy-colab)  
**License**: Open-source (research & educational use)

---

## 🚀 Contributing

Found a bug? Have a track-specific adjustment? Pull requests welcome!

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-idea`
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature/your-idea`
5. Open a pull request

---

## 📧 Questions?

Open an issue on GitHub or reach out directly. Happy strategizing! 🏁
