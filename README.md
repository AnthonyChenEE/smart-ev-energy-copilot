# ⚡ Smart EV Energy Copilot — Drive the Future of Intelligent Energy  

**Smart Energy Optimization for Home × EV × Grid**  
A lightweight, open-source demo **inspired by Xiaomi Auto’s “Human × Car × Home × AI” ecosystem vision**.  
This project demonstrates how to **optimize EV charging schedules** using linear programming, balancing **home load**, **solar PV**, and **electricity tariffs** to minimize energy costs.

> 🚗 Built with Python · Powered by Optimization · Designed for Education and Innovation  
> *(Independent open-source project — inspired by Xiaomi Auto’s ecosystem vision, not affiliated with the company.)*

---

## 🧠 项目简介（中文说明）

**Smart EV Energy Copilot（智能电动车能源副驾）**  
是一个面向智能电动车与家庭能源系统的**能量优化算法演示项目**。  
项目以“小米汽车人车家全生态”理念为灵感，利用线性规划算法，在**家庭负荷、光伏发电与分时电价**之间实现最优能量分配，  
以达到“更低成本、更高效率、更智能”的充电策略。

- 📘 **算法核心**：基于 PuLP 的线性规划模型  
- ⚙️ **主要约束**：功率上限、SOC 动态、能量平衡、末端 SOC 目标  
- 💡 **输出结果**：最优充电计划、成本分析、功率与 SOC 曲线  
- 🧩 **可扩展性**：支持多车协同调度、时变电价、光伏预测等扩展  

> 🧠 让算法更懂能源，让能源更懂你。

<img width="1024" height="1024" alt="ChatGPT Image Oct 30, 2025, 12_03_04 AM" src="https://github.com/user-attachments/assets/e7d166c8-f656-4d48-8bd0-f68197dc1169" />

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/AnthonyChenEE/smart-ev-energy-copilot.git
cd smart-ev-energy-copilot

# Install dependencies
pip install -r requirements.txt
```

### Run Simulation

```bash
# Run the optimization
python src/energycopilot/simulate.py

# Or as a module
python -m energycopilot.simulate
```

### View Results

After running, check the `outputs/` directory for:
- `schedule.csv` — Hourly charging/power schedule
- `cost_summary.json` — Total cost and final SOC
- `schedule_plot.png` — Power flow visualization
- `soc_plot.png` — Battery SOC curve

---

## 📐 How It Works

### Algorithm Overview

The optimizer uses **linear programming** (via PuLP) to solve a constrained optimization problem:

**Objective**: Minimize total energy cost
```
minimize Σ[price_buy(t) × grid_import(t) - price_sell(t) × grid_export(t)]
```

**Decision Variables**:
- `p(t)` — EV charging power at time t
- `g_import(t)` — Grid import power
- `g_export(t)` — Grid export power (solar feed-in)
- `soc(t)` — Battery state of charge

**Key Constraints**:
1. **Power Balance**: `PV + Grid Import = Home Load + EV Charge + Grid Export`
2. **SOC Dynamics**: `SOC(t+1) = SOC(t) + η × Charge Power × Δt / Battery Capacity`
3. **Charging Limits**: `0 ≤ Charge Power ≤ P_max`
4. **SOC Bounds**: `0 ≤ SOC ≤ 1`
5. **Target SOC**: `SOC(final) ≥ Target`

### Architecture

```
src/energycopilot/
├── data.py         # Synthetic data generation (load, PV, prices)
├── optimizer.py    # Linear programming solver
└── simulate.py     # Main simulation script
```

---

## ⚙️ Configuration

Create `src/energycopilot/config.json` to customize parameters:

```json
{
  "EV_BATTERY_KWH": 80.0,
  "EV_SOC0": 0.25,
  "EV_SOC_TARGET": 0.85,
  "P_MAX_KW": 11.0,
  "ETA_CHARGE": 0.95,
  "FEED_IN_TARIFF": 0.08,
  "HOURS": 24
}
```

**Parameters**:
- `EV_BATTERY_KWH`: Battery capacity (kWh)
- `EV_SOC0`: Initial state of charge (0-1)
- `EV_SOC_TARGET`: Desired final SOC (0-1)
- `P_MAX_KW`: Maximum charging power (kW)
- `ETA_CHARGE`: Charging efficiency (0-1)
- `FEED_IN_TARIFF`: Solar export price ($/kWh)
- `HOURS`: Planning horizon (hours)

---

## 🎯 Example Results

**Input Scenario**:
- Initial SOC: 25%
- Target SOC: 85%
- Battery: 80 kWh
- Home charger: 11 kW

**Output**:
- Total cost: ~$5-8 (depending on electricity rates)
- Charging strategy: Prioritizes off-peak hours (10pm-7am @ $0.18/kWh)
- Avoids peak hours (5pm-9pm @ $0.48/kWh)
- Utilizes solar PV when available

---

## 🔧 Customization & Extensions

### Use Real Data
Replace `synthetic_profiles()` in `data.py` with:
- Historical home electricity consumption
- Actual solar PV system output
- Real-time electricity pricing API

### Multi-Vehicle Support
Extend optimizer to handle multiple EVs with different:
- Battery capacities
- Charging priorities
- Arrival/departure times

### V2G (Vehicle-to-Grid)
Allow bidirectional power flow:
- Discharge during peak pricing
- Support home loads during outages
- Add battery degradation costs

### Advanced Pricing
Incorporate:
- Real-time pricing (RTP)
- Demand charges
- Tiered rate structures

---

## 📊 Technology Stack

- **Python 3.7+** — Core programming language
- **PuLP** — Linear programming modeling
- **pandas** — Data manipulation
- **NumPy** — Numerical computing
- **Matplotlib** — Visualization

---

## 📚 References & Inspiration

This project draws inspiration from:
- **Xiaomi Auto's Ecosystem Vision**: Human × Car × Home × AI integration
- **Smart Home Energy Management**: Coordinating EV, solar, and grid
- **Linear Programming Applications**: Optimal resource allocation

### Academic Context
- Energy management systems (EMS)
- Vehicle-to-home (V2H) integration
- Time-of-use (TOU) tariff optimization

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- [ ] Real-world data integration
- [ ] Web dashboard/GUI
- [ ] Multi-vehicle coordination
- [ ] V2G/V2H capabilities
- [ ] Battery degradation modeling
- [ ] Weather-based PV forecasting

---

## 📄 License

MIT License — Free to use, modify, and distribute.

See [LICENSE](LICENSE) for details.

---

## 🔗 Related Projects

- [Pyomo](http://www.pyomo.org/) — Alternative optimization framework
- [CVXPY](https://www.cvxpy.org/) — Convex optimization
- [Home Assistant](https://www.home-assistant.io/) — Home automation platform

---

## 💬 Contact

- **Issues**: [GitHub Issues](https://github.com/AnthonyChenEE/smart-ev-energy-copilot/issues)
- **Discussions**: Share your results and ideas!

---

**⚡ Let's drive the future of intelligent energy together!**
