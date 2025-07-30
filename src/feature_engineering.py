def create_time_features(df):
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'] >= 5
    return df

def create_lag_features(df, lags=[1, 2, 48, 336]):
    for lag in lags:
        df[f'demand_lag_{lag}'] = df['demand'].shift(lag)
    return df

def create_rolling_features(df):
    df['rolling_mean_48'] = df['demand'].rolling(window=48).mean()
    return df
