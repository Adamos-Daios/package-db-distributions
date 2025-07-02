#!pip install py3dbp

import pandas as pd
import time
import platform
import sys
from py3dbp import Packer, Bin, Item

# --- Configuration ---
FILE_PATH = "/content/boxes_100.xlsx"  # Upload your Excel file in Colab
PALLET_LENGTH = 1200  # mm (1.2 m)
PALLET_WIDTH = 1000   # mm (1.0 m)
PALLET_HEIGHT = 850   # mm (0.85 m)
PALLET_MAX_WEIGHT = 9999999  # effectively ignore weight constraint
NUM_PALLETS = 11       # Number of pallets provided for packing

# --- Step 1: Load and rename columns ---
df = pd.read_excel(FILE_PATH)
df = df.rename(columns={
    'Length (cm)': 'length_cm',
    'Width (cm)': 'width_cm',
    'Height (cm)': 'height_cm',
    'External Volume (L)': 'volume_L',
    'Max Load Capacity (kg)': 'max_load_kg',
    'Fragile': 'fragile',
    'Stackable': 'stackable',
    'Box ID': 'box_id'
})

# --- Step 2: Basic Validation ---
df['valid'] = (
    (df['length_cm'] > 0) &
    (df['width_cm'] > 0) &
    (df['height_cm'] > 0) &
    (df['volume_L'] > 0)
)

if not df['valid'].all():
    print("❌ Validation failed: some boxes have invalid dimensions or volume.")
    print(df[~df['valid']])
else:
    print("✅ All boxes passed basic validation.")

print(f"\n📦 Total boxes: {len(df)}")
print(f"📏 Total volume: {df['volume_L'].sum():,.2f} L")

# --- Step 3: Initialize Packer and add pallets (bins) ---
packer = Packer()
packer.bins.clear()
for i in range(NUM_PALLETS):
    packer.add_bin(Bin(
        name=f"Pallet_{i+1}",
        width=PALLET_WIDTH,
        height=PALLET_HEIGHT,
        depth=PALLET_LENGTH,
        max_weight=PALLET_MAX_WEIGHT
    ))

# --- Step 4: Add boxes (items) ---
packer.items.clear()
for idx, row in df.iterrows():
    packer.add_item(Item(
        name=row['box_id'],
        width=row['width_cm'] * 10,   # convert cm to mm
        height=row['height_cm'] * 10,
        depth=row['length_cm'] * 10,
        weight=row['max_load_kg']
    ))

# --- Step 5: Run packing and time it ---
start_time = time.time()
packer.pack(bigger_first=True, distribute_items=True, number_of_decimals=0)
end_time = time.time()
runtime = end_time - start_time

# --- Step 6: Check packing completeness ---
packed_boxes = sum(len(b.items) for b in packer.bins)
unpacked_boxes = len(df) - packed_boxes

if unpacked_boxes > 0:
    print(f"⚠️ Warning: {unpacked_boxes} boxes were not packed!")
else:
    print("✅ All boxes packed successfully.")

# --- Step 7: Reporting ---
utilizations = []
weights = []
total_boxes = packed_boxes

print(f"\n📦 Boxes packed into {len(packer.bins)} pallet(s) using Guillotine Cut (no weight constraint):\n")

for i, b in enumerate(packer.bins):
    vol_used = sum(item.get_volume() for item in b.items) / 1_000_000  # mm³ to L
    weight = sum(item.weight for item in b.items)
    utilization = float(vol_used) / (float(PALLET_LENGTH) * float(PALLET_WIDTH) * float(PALLET_HEIGHT) / 1_000_000)
    utilizations.append(utilization)
    weights.append(weight)
    print(f"  🪵 Pallet {i+1}: {len(b.items)} boxes, {vol_used:.2f} L used ({utilization:.1%}), {weight:.2f} kg")

print("\n📊 Summary:")
print(f"🔢 Number of pallets used: {len(packer.bins)}")
print(f"📦 Average box count per pallet: {total_boxes / len(packer.bins):.2f}")
print(f"📦 Average pallet utilization: {sum(utilizations) / len(utilizations) * 100:.2f}%")
print(f"🏋️ Max pallet weight (ignored constraint): {max(weights):.2f} kg")
print(f"⏱️ Runtime: {runtime:.3f} seconds")

# --- Step 8: Environment info ---
print("\n🖥️ Environment Information:")
print(f"Python version: {sys.version}")
print(f"Platform: {platform.platform()}")
