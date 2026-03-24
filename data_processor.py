import pandas as pd
import glob
import os

# Load all 3 CSV files from the data folder
csv_files = glob.glob("data/*.csv")

# Combine all CSV files into one dataframe
df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# Step 1: Filter only Pink Morsels
df = df[df["product"] == "pink morsel"]

# Step 2: Calculate sales (price x quantity)
# Remove the '$' sign from price and convert to float
df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
df["sales"] = df["price"] * df["quantity"]

# Step 3: Keep only the required columns
df = df[["sales", "date", "region"]]

# Step 4: Save to output CSV
output_path = "data/processed_data.csv"
df.to_csv(output_path, index=False)

print(f"Done! Processed {len(df)} rows.")
print(df.head())