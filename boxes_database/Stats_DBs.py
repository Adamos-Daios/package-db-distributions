# 📦 STEP 1: Install and import dependencies
import pandas as pd
import os
from google.colab import files
from IPython.display import display

# 📂 STEP 2: Upload all 7 datasets
print("Upload your Excel files (e.g., boxes_0500.xlsx to boxes_100000.xlsx):")
uploaded = files.upload()

# 🧠 STEP 3: Process each file and collect stats
summary_list = []

for filename in uploaded.keys():
    print(f"Processing: {filename}")
    df = pd.read_excel(filename)

    # Normalize binary flags
    df['Fragile'] = df['Fragile'].map({'Yes': 1, 'No': 0})
    df['Stackable'] = df['Stackable'].map({'Yes': 1, 'No': 0})

    # Calculate summary statistics
    stats = {
        "Dataset": filename,
        "Items": len(df),
        "Avg Length (cm)": df['Length (cm)'].mean(),
        "Avg Width (cm)": df['Width (cm)'].mean(),
        "Avg Height (cm)": df['Height (cm)'].mean(),
        "Avg Max Load (kg)": df['Max Load Capacity (kg)'].mean(),
        "Fragile %": df['Fragile'].mean() * 100,
        "Stackable %": df['Stackable'].mean() * 100
    }

    summary_list.append(stats)

# 🧾 STEP 4: Create a DataFrame with the results
summary_df = pd.DataFrame(summary_list)
summary_df = summary_df.sort_values(by="Items").round(2)

# 🖨️ Display summary
print("\nSummary Statistics Across Datasets:")
display(summary_df)

# 💾 STEP 5: Save and export as CSV (optional)
summary_df.to_csv("MixedPalletBoxes_Summary.csv", index=False)
files.download("MixedPalletBoxes_Summary.csv")
