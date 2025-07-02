import pandas as pd
import time

# --- Step 0: Start Timer ---
start_time = time.time()

# --- Step 1: Load Excel File ---
file_path = "/content/boxes_100.xlsx"  # Ensure file is uploaded in Colab
df = pd.read_excel(file_path)

# Rename columns for convenience
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

# --- Step 2: Validation ---
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

# --- Step 3: First-Fit Decreasing (FFD) Palletizing ---
PALLET_CAPACITY_L = 1000  # 1 m³ per pallet = 1000 liters

# Sort boxes by descending volume
boxes_sorted = df.sort_values(by='volume_L', ascending=False).reset_index(drop=True)

pallets = []
current_pallet = []
current_volume = 0

for idx, row in boxes_sorted.iterrows():
    box_vol = row['volume_L']
    if current_volume + box_vol <= PALLET_CAPACITY_L:
        current_pallet.append(row)
        current_volume += box_vol
    else:
        pallets.append(pd.DataFrame(current_pallet))
        current_pallet = [row]
        current_volume = box_vol

# Add the final pallet
if current_pallet:
    pallets.append(pd.DataFrame(current_pallet))

# --- Step 4: Per-Pallet Report ---
print(f"\n📦 Boxes packed into {len(pallets)} pallet(s) using First-Fit Decreasing:\n")

utilizations = []
box_counts = []

for i, p in enumerate(pallets):
    vol_used = p['volume_L'].sum()
    utilizations.append(vol_used / PALLET_CAPACITY_L)
    box_counts.append(len(p))
    print(f"  🪵 Pallet {i+1}: {len(p)} boxes, {vol_used:.2f} L used ({vol_used / PALLET_CAPACITY_L:.1%})")

# --- Step 5: Summary Stats ---
end_time = time.time()
runtime = end_time - start_time

print("\n📊 Summary:")
print(f"🔢 Number of pallets used: {len(pallets)}")
print(f"📦 Average pallet volume utilization: {sum(utilizations) / len(utilizations) * 100:.2f}%")
print(f"📦 Average box count per pallet: {sum(box_counts) / len(box_counts):.2f}")
print(f"⏱️ Runtime: {runtime:.3f} seconds")

# --- Optional: Show first few boxes from the first pallet ---
print("\n🔍 First pallet preview:")
print(pallets[0][['box_id', 'length_cm', 'width_cm', 'height_cm', 'volume_L', 'fragile']].head())
