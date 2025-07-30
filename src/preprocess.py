import pandas as pd
import os

def load_dispatch_data(filepath):
    df = pd.read_csv(filepath)
    df['SETTLEMENTDATE'] = pd.to_datetime(df['SETTLEMENTDATE'])
    vic_df = df[df['REGIONID'] == 'VIC1'][['SETTLEMENTDATE', 'TOTALDEMAND']]
    vic_df.rename(columns={'SETTLEMENTDATE': 'datetime', 'TOTALDEMAND': 'demand'}, inplace=True)
    vic_df = vic_df.sort_values('datetime').reset_index(drop=True)
    return vic_df
