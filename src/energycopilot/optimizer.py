# -*- coding: utf-8 -*-
"""optimizer.py — Linear programming optimizer for EV charging schedule

This module implements the core optimization logic using PuLP to solve
a linear programming problem that minimizes energy costs while satisfying
all constraints (power limits, SOC dynamics, energy balance).
"""

import numpy as np
import pandas as pd
import pulp


def optimize_schedule(
    df: pd.DataFrame,
    battery_kwh: float = 80.0,
    soc0: float = 0.25,
    soc_target: float = 0.85,
    p_max_kw: float = 11.0,
    eta: float = 0.95,
    price_sell=None
) -> dict:
    """
    Optimize EV charging schedule to minimize energy costs.

    This function formulates and solves a linear programming problem that
    determines the optimal charging schedule for an electric vehicle while
    considering home load, solar PV generation, and time-varying electricity prices.

    Parameters
    ----------
    df : pd.DataFrame
        Input data with columns: 'load_kw' (home load), 'pv_kw' (solar PV),
        'price_buy' (grid purchase price per kWh). One row per time period.
    battery_kwh : float, default=80.0
        EV battery capacity in kWh
    soc0 : float, default=0.25
        Initial state of charge (SOC) as a fraction (0 to 1)
    soc_target : float, default=0.85
        Target SOC at the end of planning horizon (0 to 1)
    p_max_kw : float, default=11.0
        Maximum charging power in kW
    eta : float, default=0.95
        Charging efficiency (typically 0.9-0.95)
    price_sell : array-like, optional
        Selling price (feed-in tariff) per kWh for each time period.
        If None, defaults to zeros (no feed-in).

    Returns
    -------
    dict
        Dictionary containing:
        - 'schedule': DataFrame with optimized charging/import/export schedule
        - 'total_cost_$': Total energy cost in dollars
        - 'soc_T': Final state of charge at end of horizon

    Algorithm
    ---------
    Decision variables:
        p[t]     : EV charging power at time t (kW)
        g_imp[t] : Grid import at time t (kW)
        g_exp[t] : Grid export at time t (kW)
        soc[t]   : State of charge at time t (fraction)

    Objective:
        minimize Σ(price_buy[t] * g_imp[t] - price_sell[t] * g_exp[t])

    Constraints:
        1. Power balance: pv[t] + g_imp[t] = load[t] + p[t] + g_exp[t]
        2. SOC dynamics: soc[t+1] = soc[t] + eta * p[t] * dt / battery_kwh
        3. SOC bounds: 0 ≤ soc[t] ≤ 1
        4. Charging limit: 0 ≤ p[t] ≤ p_max_kw
        5. Final SOC target: soc[T] ≥ soc_target
    """
    # Time horizon and time step
    T = len(df)
    dt = 1.0  # 1 hour per period

    # Initialize sell price if not provided
    if price_sell is None:
        price_sell = np.zeros(T)
    else:
        price_sell = np.asarray(price_sell)

    # Create optimization model
    model = pulp.LpProblem('HomeCarGrid', pulp.LpMinimize)

    # Decision variables
    # EV charging power (kW) at each time step
    p = {t: pulp.LpVariable(f'p_{t}', lowBound=0, upBound=p_max_kw)
         for t in range(T)}

    # Grid import power (kW)
    g_imp = {t: pulp.LpVariable(f'g_imp_{t}', lowBound=0)
             for t in range(T)}

    # Grid export power (kW)
    g_exp = {t: pulp.LpVariable(f'g_exp_{t}', lowBound=0)
             for t in range(T)}

    # State of charge (0 to 1) - T+1 time points (including initial)
    soc = {t: pulp.LpVariable(f'soc_{t}', lowBound=0, upBound=1)
           for t in range(T + 1)}

    # Initial SOC constraint
    model += soc[0] == soc0, "Initial_SOC"

    # Add constraints for each time period
    for t in range(T):
        load = df.loc[t, 'load_kw']
        pv = df.loc[t, 'pv_kw']

        # Power balance constraint
        model += (pv + g_imp[t] == load + p[t] + g_exp[t],
                  f"Power_Balance_{t}")

        # SOC dynamics constraint
        model += (soc[t + 1] == soc[t] + eta * p[t] * dt / battery_kwh,
                  f"SOC_Dynamics_{t}")

    # Final SOC target constraint
    model += soc[T] >= soc_target, "Final_SOC_Target"

    # Objective function: minimize total energy cost
    model += pulp.lpSum(
        df.loc[t, 'price_buy'] * g_imp[t] - price_sell[t] * g_exp[t]
        for t in range(T)
    ), "Total_Cost"

    # Solve the optimization problem
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    # Extract solution
    out = df.copy()
    out['p_charge_kw'] = [p[t].value() for t in range(T)]
    out['g_import_kw'] = [g_imp[t].value() for t in range(T)]
    out['g_export_kw'] = [g_exp[t].value() for t in range(T)]
    out['soc'] = [soc[t].value() for t in range(T)]

    return {
        'schedule': out,
        'total_cost_$': float(pulp.value(model.objective)),
        'soc_T': soc[T].value()
    }
