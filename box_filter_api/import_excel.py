# import_excel.py

import pandas as pd
import sqlite3
import os

# Prompt the user for the Excel file name
excel_file = input("Enter the Excel file name (e.g., boxes_10000.xlsx): ")

# Check if file exists
if not os.path.exists(excel_file):
    print(f"❌ File '{excel_file}' not found.")
    exit(1)

# Load the Excel file
df = pd.read_excel(excel_file)

# Define the database and table names
db_name = "packages.db"
table_name = "boxes"

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_name)

# Write the dataframe to the SQLite table
df.to_sql(table_name, conn, if_exists="replace", index=False)

conn.close()

print(f"✅ Excel data from '{excel_file}' imported into '{db_name}' (table: '{table_name}')!")
