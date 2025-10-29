import numpy as np,pandas as pd,pulp

def optimize_schedule(df,battery_kwh=80.0,soc0=0.25,soc_target=0.85,p_max_kw=11.0,eta=0.95,price_sell=None):
    T=len(df);dt=1.0;price_sell=np.zeros(T) if price_sell is None else np.asarray(price_sell)
    model=pulp.LpProblem('HomeCarGrid',pulp.LpMinimize)
    p={t:pulp.LpVariable(f'p_{t}',0,p_max_kw) for t in range(T)}
    g_imp={t:pulp.LpVariable(f'g_imp_{t}',0) for t in range(T)}
    g_exp={t:pulp.LpVariable(f'g_exp_{t}',0) for t in range(T)}
    soc={t:pulp.LpVariable(f'soc_{t}',0,1) for t in range(T+1)}
    model+=soc[0]==soc0
    for t in range(T):
        load,pv=df.loc[t,['load_kw','pv_kw']]
        model+=pv+g_imp[t]==load+p[t]+g_exp[t]
        model+=soc[t+1]==soc[t]+eta*p[t]*dt/battery_kwh
    model+=soc[T]>=soc_target
    model+=pulp.lpSum(df.loc[t,'price_buy']*g_imp[t]-price_sell[t]*g_exp[t] for t in range(T))
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    out=df.copy();out['p_charge_kw']=[p[t].value() for t in range(T)];out['g_import_kw']=[g_imp[t].value() for t in range(T)];out['g_export_kw']=[g_exp[t].value() for t in range(T)];out['soc']=[soc[t].value() for t in range(T)]
    return {'schedule':out,'total_cost_$':float(pulp.value(model.objective)),'soc_T':soc[T].value()}
