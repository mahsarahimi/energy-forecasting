import pandas as pd
import os



def preprocess_csv(input_path, output_path):
    # Step 1: Preview and skip metadata/header rows
    # (Assume first 3 rows are metadata, 4th row is header)
    df = pd.read_csv(input_path, skiprows=3, header=0, on_bad_lines='skip')

    # # Step 2: Remove columns where all values are the same
    # constant_cols = [col for col in df.columns if df[col].nunique(dropna=False) == 1]
    # df = df.drop(columns=constant_cols)

    # Step 3: Remove useless columns
    useless_cols = ['I', 'PREDISPATCH', 'LOCAL_PRICE', '1', 'PREDISPATCHSEQNO','LASTCHANGED']
    df = df.drop(columns=[col for col in useless_cols if col in df.columns])
    
    # Step 4: Optionally, reset index
    df = df.reset_index(drop=True)

    # Step 5: Write cleaned DataFrame to output CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned CSV written to: {output_path}")

if __name__ == "__main__":
    input_csv = "../data/raw/PUBLIC_PREDISPATCHIS_202508121400_20250812133340.CSV"  # Change as needed
    output_csv = "../data/processed/PUBLIC_PREDISPATCHIS_202508121400_20250812133340_clean.csv"
    preprocess_csv(input_csv, output_csv)
