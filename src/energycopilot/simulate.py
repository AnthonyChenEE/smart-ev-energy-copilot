# -*- coding: utf-8 -*-
"""simulate.py — Main simulation script for Smart EV Energy Copilot

This script orchestrates the complete EV energy optimization workflow:
1. Load configuration parameters
2. Generate synthetic input data (load, PV, prices)
3. Run the optimization algorithm
4. Save results and generate visualizations

Can be run as:
- Package: python -m energycopilot.simulate
- Standalone: python simulate.py
"""

# --- Standalone compatibility patch ---
if __name__ == "__main__" and __package__ is None:
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    __package__ = "energycopilot"
# --------------------------------------

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .data import synthetic_profiles, price_sell_vector
from .optimizer import optimize_schedule


def load_cfg() -> dict:
    """
    Load configuration from config.json or use defaults.

    Searches for config.json in the same directory as this script.
    If not found, returns default configuration values.

    Returns
    -------
    dict
        Configuration dictionary with keys:
        - EV_BATTERY_KWH: Battery capacity (kWh)
        - EV_SOC0: Initial state of charge (fraction)
        - EV_SOC_TARGET: Target final SOC (fraction)
        - P_MAX_KW: Maximum charging power (kW)
        - ETA_CHARGE: Charging efficiency (fraction)
        - FEED_IN_TARIFF: Grid export price ($/kWh)
        - HOURS: Planning horizon (hours)
    """
    here = os.path.dirname(__file__)
    cfg_path = os.path.join(here, "config.json")

    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Default configuration for a typical EV setup
    return {
        "EV_BATTERY_KWH": 80.0,      # 80 kWh battery (e.g., Tesla Model 3 LR)
        "EV_SOC0": 0.25,              # Start at 25% charge
        "EV_SOC_TARGET": 0.85,        # Target 85% charge (recommended for battery health)
        "P_MAX_KW": 11.0,             # 11 kW Level 2 home charger
        "ETA_CHARGE": 0.95,           # 95% charging efficiency
        "FEED_IN_TARIFF": 0.08,       # $0.08/kWh for solar export
        "HOURS": 24                   # 24-hour planning horizon
    }

def main():
    """
    Main simulation function.

    Workflow:
    1. Load configuration
    2. Generate synthetic input data
    3. Run optimization
    4. Save results (CSV, JSON, plots)
    """
    # Load configuration parameters
    cfg = load_cfg()
    T = int(cfg.get("HOURS", 24))

    # Generate synthetic input data
    df = synthetic_profiles(T=T)
    price_sell = price_sell_vector(
        T=T,
        feed_in_tariff=float(cfg.get("FEED_IN_TARIFF", 0.08))
    )

    # Run optimization
    res = optimize_schedule(
        df,
        battery_kwh=float(cfg.get("EV_BATTERY_KWH", 80.0)),
        soc0=float(cfg.get("EV_SOC0", 0.25)),
        soc_target=float(cfg.get("EV_SOC_TARGET", 0.85)),
        p_max_kw=float(cfg.get("P_MAX_KW", 11.0)),
        eta=float(cfg.get("ETA_CHARGE", 0.95)),
        price_sell=price_sell
    )

    # Create output directory
    outdir = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
    os.makedirs(outdir, exist_ok=True)

    # Save schedule as CSV
    csv_path = os.path.join(outdir, "schedule.csv")
    res["schedule"].to_csv(csv_path, index=False)

    # Save cost summary as JSON
    summary = {k: v for k, v in res.items() if k != "schedule"}
    json_path = os.path.join(outdir, "cost_summary.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Generate power flow plot
    dfp = res["schedule"]
    plt.figure(figsize=(10, 4))
    plt.plot(dfp["hour"], dfp["p_charge_kw"], label="EV Charge (kW)", linewidth=2)
    plt.plot(dfp["hour"], dfp["g_import_kw"], label="Grid Import (kW)", linestyle="--")
    plt.plot(dfp["hour"], dfp["g_export_kw"], label="Grid Export (kW)", linestyle="--")
    plt.plot(dfp["hour"], dfp["pv_kw"], label="Solar PV (kW)", alpha=0.7)
    plt.plot(dfp["hour"], dfp["load_kw"], label="Home Load (kW)", alpha=0.7)
    plt.legend(loc="upper right")
    plt.xlabel("Hour")
    plt.ylabel("Power (kW)")
    plt.title("Optimized Power Flow Schedule")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plot1 = os.path.join(outdir, "schedule_plot.png")
    plt.savefig(plot1, dpi=160)
    plt.close()

    # Generate SOC plot
    plt.figure(figsize=(10, 3.5))
    plt.plot(dfp["hour"], dfp["soc"] * 100.0, label="SOC", linewidth=2, color="green")
    plt.axhline(
        100 * float(cfg.get("EV_SOC_TARGET", 0.85)),
        linestyle="--",
        color="red",
        label="Target SOC"
    )
    plt.legend(loc="upper right")
    plt.xlabel("Hour")
    plt.ylabel("State of Charge (%)")
    plt.title("EV Battery State of Charge Over Time")
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plot2 = os.path.join(outdir, "soc_plot.png")
    plt.savefig(plot2, dpi=160)
    plt.close()

    # Print summary
    print("\n" + "="*60)
    print("✅ Optimization Complete!")
    print("="*60)
    print(f"Total Cost: ${res['total_cost_$']:.2f}")
    print(f"Final SOC: {res['soc_T']*100:.1f}%")
    print(f"\nResults saved to: {outdir}")
    print(f"  - Schedule: {os.path.basename(csv_path)}")
    print(f"  - Summary: {os.path.basename(json_path)}")
    print(f"  - Power plot: {os.path.basename(plot1)}")
    print(f"  - SOC plot: {os.path.basename(plot2)}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
