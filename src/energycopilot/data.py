def synthetic_profiles(T=24, seed=42):
    import numpy as np, pandas as pd
    rng=np.random.default_rng(seed)
    hours=np.arange(T)
    load=1.2+0.8*np.sin(2*np.pi*(hours-7)/24)
    pv=np.maximum(5*np.exp(-0.5*((hours-12)/3)**2)+rng.normal(0,0.1,T),0)
    price=np.full(T,0.3);price[(hours>=22)|(hours<7)]=0.18;price[(hours>=17)&(hours<=21)]=0.48
    return pd.DataFrame({'hour':hours,'load_kw':load,'pv_kw':pv,'price_buy':price})

def price_sell_vector(T=24,feed_in_tariff=0.08):
    import numpy as np;return np.full(T,feed_in_tariff)
