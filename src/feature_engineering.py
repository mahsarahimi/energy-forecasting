
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

print ("1- load data")
file_path = 'data/processed/PUBLIC_PREDISPATCHIS_202508121400_20250812133340_clean.csv'
df0 = pd.read_csv(file_path, header=0)

# ## 2- check missing values, data ranges and duplicates
print ("2- check missing values, data ranges and duplicates")
# Check for duplicate rows in the DataFrame
duplicates = df0.duplicated()
print("duplicates are:" , duplicates.any())  # True if there are any duplicates

# Check for missing values in each column
print("count of missing values:" , df0.isna().sum())


# %%
# To display rows with any missing values
print(df0[df0.isna().any(axis=1)])

# %%
df0.dropna(inplace=True)
print ("count of missing values after dropping rows with NaN:" , df0.isna().sum())

# %%
# Display the range (min and max) for each column in the DataFrame
for col in df0.columns:
    if np.issubdtype(df0[col].dtype, np.number):
        print(f"{col}: min={df0[col].min()}, max={df0[col].max()}")
    else:
        print(f"{col}: unique values count={df0[col].nunique()}")

print ("3- create time-based features")
# ## 3- create time-based features


# Convert the 'DATETIME' column to proper datetime type
df0['DATETIME'] = pd.to_datetime(df0['DATETIME'])



# We'll do system-wide forecasting, so we can aggregate the data over DUIDs.
df0.sort_values(by='DATETIME', inplace=True)
df0.reset_index(drop=True, inplace=True)
df = df0.groupby("DATETIME").agg({
    "LOCAL_PRICE_ADJUSTMENT": "mean",
    "LOCALLY_CONSTRAINED": "mean"
}).reset_index()




# extracting date and time features
df['hour'] = df['DATETIME'].dt.hour
df['day_of_week'] = df['DATETIME'].dt.dayofweek  # Monday=0
df['month'] = df['DATETIME'].dt.month
df['is_weekend'] = df['day_of_week'].isin([5,6]).astype(int)
df['is_weekday'] = df['day_of_week'].isin([0,1,2,3,4]).astype(int)



import holidays

# Create a set of Australian holidays for the relevant years in the data
years = df['DATETIME'].dt.year.unique()
au_holidays = holidays.country_holidays('AU', years=years)

# Add is_holiday flag
df['is_holiday'] = df['DATETIME'].dt.date.isin(au_holidays).astype(int)

#4 ## 4- Create lag features
print ("4- Create lag features")


for lag in [1, 2, 3, 6]:  # 30 min steps --> lag 2 = 1 hour
    df[f'lag_{lag}'] = df['LOCAL_PRICE_ADJUSTMENT'].shift(lag)


# ## 5- Rolling window stats
print ("5- Rolling window stats")
# Smooth past data into trends & volatility measures.
# 

# %%
df['price_roll_mean_3'] = df['LOCAL_PRICE_ADJUSTMENT'].rolling(3).mean()
df['price_roll_std_3'] = df['LOCAL_PRICE_ADJUSTMENT'].rolling(3).std()
df['price_roll_mean_6'] = df['LOCAL_PRICE_ADJUSTMENT'].rolling(6).mean()
df['price_roll_std_6'] = df['LOCAL_PRICE_ADJUSTMENT'].rolling(6).std()
df['price_roll_mean_12'] = df['LOCAL_PRICE_ADJUSTMENT'].rolling(12).mean()
df['price_roll_std_12'] = df['LOCAL_PRICE_ADJUSTMENT'].rolling(12).std()
df['price_roll_mean_24'] = df['LOCAL_PRICE_ADJUSTMENT'].rolling(24).mean()
df['price_roll_std_24'] = df['LOCAL_PRICE_ADJUSTMENT'].rolling(24).std()

# %%




# %% [markdown]
# ## 6- Encode categorical variables
# DUID is categorical (generator ID).
# If predicting per-unit prices, one-hot encode:
print ("6- Encode categorical variables")

# %%
#df = pd.get_dummies(df, columns=['DUID'], drop_first=True)



# %%
#df.drop(columns=['DATETIME'], inplace=True)  # Drop the original DATETIME column
# drop Nan rows
df.dropna(inplace=True)

# %%
import os
os.makedirs('../data/features', exist_ok=True)
df.to_csv('../data/features/price_features.csv', index=False)
print("Feature engineering complete. Processed data saved to '../data/features/price_features.csv'.")


