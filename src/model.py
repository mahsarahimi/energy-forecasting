"""
model.py
Production pipeline for forecasting LOCAL_PRICE_ADJUSTMENT
using Linear Regression.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import joblib
import os

# -------------------
# 1. Load feature-engineered data
# -------------------
DATA_PATH = "data/features/features_original.csv"
MODEL_PATH = "outputs/models/linear_regression_model.pkl"

df = pd.read_csv(DATA_PATH)

# Define target and features
target = "LOCAL_PRICE_ADJUSTMENT"
features = [col for col in df.columns if col not in ["DATETIME", target]]

X = df[features]
y = df[target]

# -------------------
# 2. TimeSeries Cross-validation
# -------------------
tscv = TimeSeriesSplit(n_splits=5)
model = LinearRegression()

results = []
fold = 1

for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    # Train
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)

    results.append({
        "Fold": fold,
        "MAE": mae,
        "RMSE": rmse
    })

    print(f"Fold {fold} -> MAE: {mae:.2f}, RMSE: {rmse:.2f}")
    fold += 1

# -------------------
# 3. Train on full dataset
# -------------------
model.fit(X, y)

# -------------------
# 4. Save final model
# -------------------
os.makedirs("models", exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"\n✅ Final model trained and saved to {MODEL_PATH}")

# -------------------
# 5. Save CV results
# -------------------
results_df = pd.DataFrame(results)
results_df.to_csv("outputs/models/cv_results.csv", index=False)
print("\nCross-validation results saved to models/cv_results.csv")
