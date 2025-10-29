# -*- coding: utf-8 -*-
"""simulate.py — Xiaomi EV Energy Copilot
Can be run as package (python -m energycopilot.simulate)
or standalone (python simulate.py)
"""

# --- Standalone compatibility patch ---
if __name__ == "__main__" and __package__ is None:
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    __package__ = "energycopilot"
# --------------------------------------

import os, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .data import synthetic_profiles, price_sell_vector
from .optimizer import optimize_schedule

def load_cfg():
    here = os.path.dirname(__file__)
    cfg_path = os.path.join(here, "config.json")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "EV_BATTERY_KWH": 80.0,
        "EV_SOC0": 0.25,
        "EV_SOC_TARGET": 0.85,
        "P_MAX_KW": 11.0,
        "ETA_CHARGE": 0.95,
        "FEED_IN_TARIFF": 0.08,
        "HOURS": 24
    }

def main():
    cfg = load_cfg()
    T = int(cfg.get("HOURS", 24))

    df = synthetic_profiles(T=T)
    price_sell = price_sell_vector(T=T, feed_in_tariff=float(cfg.get("FEED_IN_TARIFF", 0.08)))

    res = optimize_schedule(
        df,
        battery_kwh=float(cfg.get("EV_BATTERY_KWH", 80.0)),
        soc0=float(cfg.get("EV_SOC0", 0.25)),
        soc_target=float(cfg.get("EV_SOC_TARGET", 0.85)),
        p_max_kw=float(cfg.get("P_MAX_KW", 11.0)),
        eta=float(cfg.get("ETA_CHARGE", 0.95)),
        price_sell=price_sell
    )

    outdir = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
    os.makedirs(outdir, exist_ok=True)

    csv_path = os.path.join(outdir, "schedule.csv")
    res["schedule"].to_csv(csv_path, index=False)

    summary = {k: v for k, v in res.items() if k != "schedule"}
    json_path = os.path.join(outdir, "cost_summary.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    dfp = res["schedule"]
    plt.figure(figsize=(10,4))
    plt.plot(dfp["hour"], dfp["p_charge_kw"], label="p_charge (kW)")
    plt.plot(dfp["hour"], dfp["g_import_kw"], label="grid import (kW)")
    plt.plot(dfp["hour"], dfp["g_export_kw"], label="grid export (kW)")
    plt.plot(dfp["hour"], dfp["pv_kw"], label="pv (kW)")
    plt.plot(dfp["hour"], dfp["load_kw"], label="home load (kW)")
    plt.legend()
    plt.xlabel("hour")
    plt.ylabel("kW")
    plt.tight_layout()
    plot1 = os.path.join(outdir, "schedule_plot.png")
    plt.savefig(plot1, dpi=160)
    plt.close()

    plt.figure(figsize=(10,3.5))
    plt.plot(dfp["hour"], dfp["soc"]*100.0, label="SOC %")
    plt.axhline(100*float(cfg.get("EV_SOC_TARGET", 0.85)), linestyle="--", label="target (%)")
    plt.legend()
    plt.xlabel("hour")
    plt.ylabel("SOC (%)")
    plt.tight_layout()
    plot2 = os.path.join(outdir, "soc_plot.png")
    plt.savefig(plot2, dpi=160)
    plt.close()

    print("✅ Optimization complete.")
    print("Saved:", csv_path, json_path, plot1, plot2)

if __name__ == "__main__":
    main()
