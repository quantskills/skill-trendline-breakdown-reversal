#!/usr/bin/env python3
import argparse,json,pandas as pd
from factor import calculate_factor
def validate(df):
 s=pd.to_numeric(df['factor'],errors='coerce'); f=s.dropna(); return {'rows':len(s),'nan_ratio':float(s.isna().mean()),'min':None if f.empty else float(f.min()),'max':None if f.empty else float(f.max()),'infinite_count':int((~s.isna() & ~s.map(lambda x:abs(x)<float('inf'))).sum()),'signal_count':int(df.get('signal',pd.Series(dtype=int)).sum())}
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('csv'); a=p.parse_args(); print(json.dumps(validate(calculate_factor(pd.read_csv(a.csv))),ensure_ascii=False,indent=2))
