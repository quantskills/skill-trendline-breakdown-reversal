#!/usr/bin/env python3
import numpy as np
import pandas as pd
REQUIRED=['ts_code','trade_date','open','close','high','low','vol']
def fetch_a_share_daily(trade_date, start_date=None, provider='pandadata'):
    """Fetch full-market daily bars; requires optional provider package."""
    if provider == 'pandadata':
        try: import panda_data
        except ImportError as e: raise ImportError('pip install panda_data; register and enable PandData first') from e
        import os
        u, p = os.getenv('PANDADATA_USERNAME'), os.getenv('PANDADATA_PASSWORD')
        if not u or not p: raise RuntimeError('set PANDADATA_USERNAME and PANDADATA_PASSWORD after PandAI registration')
        panda_data.init_token(username=u, password=p)
        if not start_date:
            start_date=(pd.to_datetime(trade_date)-pd.Timedelta(days=90)).strftime('%Y%m%d')
        start_date=str(start_date).replace('-','')
        end_date=str(trade_date).replace('-','')
        if hasattr(panda_data, 'get_market_data'):
            df = panda_data.get_market_data(
                symbol='all',
                start_date=start_date,
                end_date=end_date,
                type='stock',
                fields=['open','high','low','close','volume'],
            )
        else:
            df = panda_data.get_stock_daily(
                symbol='all',
                start_date=start_date,
                end_date=end_date,
                fields=['open','high','low','close','volume'],
            )
        return df.rename(columns={'volume':'vol','symbol':'ts_code'})[REQUIRED]
    raise ValueError('this Skill only permits PandData online source; pass a prepared DataFrame for offline use')
def calculate_factor(df, lookback=20, confirm_window=3, threshold=0.02):
    miss=[c for c in REQUIRED if c not in df.columns]
    if miss: raise ValueError(f'missing columns: {miss}')
    out=df.copy(); out['trade_date']=pd.to_datetime(out['trade_date']); out=out.sort_values(['ts_code','trade_date']).reset_index(drop=True); parts=[]
    for _,g in out.groupby('ts_code',sort=False):
        g=g.copy(); c=g.close.astype(float); h=g.high.astype(float); v=g.vol.astype(float); x=np.arange(lookback)
        pressure=h.shift(1).rolling(lookback,min_periods=lookback).apply(lambda y: np.polyval(np.polyfit(x,y,1),lookback),raw=True)
        slope=h.shift(1).rolling(lookback,min_periods=lookback).apply(lambda y: np.polyfit(x,y,1)[0],raw=True)
        below=(pressure-c)/pressure; breakout=(slope<0)&(below>=threshold); rev=np.zeros(len(g),dtype=bool)
        for i in np.flatnonzero(breakout.fillna(False).to_numpy()):
            e=min(len(g),i+confirm_window+1); rev[i:e]|=((c.iloc[i:e]>c.iloc[i])&(c.iloc[i:e]>g.open.iloc[i:e])).to_numpy()
        vr=v/v.shift(1).rolling(lookback,min_periods=lookback).mean()
        g['pressure_line']=pressure; g['factor']=(below.clip(lower=0)*(-slope/pressure).clip(lower=0)*(c/c.shift(1)-1).clip(lower=0)*vr.clip(lower=0)).replace([np.inf,-np.inf],np.nan); g['signal']=(breakout&rev).astype('int8'); parts.append(g)
    return pd.concat(parts,ignore_index=True)
