import pandas as pd
import time

# --- Step 0: Timer ---
start_time = time.time()

# --- Step 1: Load Excel File ---
file_path = "/content/boxes_100.xlsx"  # Adjust path accordingly
df = pd.read_excel(file_path)

# Rename for convenience
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

# --- Step 3: Pallet dimensions in cm ---
PALLET_LENGTH = 120
PALLET_WIDTH = 100
PALLET_HEIGHT = 85

# --- Step 4: Layered (Shelf) Packing ---
# Sort boxes by height descending for shelf packing
boxes_sorted = df.sort_values(by='height_cm', ascending=False).reset_index(drop=True)

pallets = []
current_pallet = []
current_shelf_height = 0
current_shelf_width_used = 0
current_shelf_boxes = []
current_pallet_height = 0

def start_new_pallet():
    return {
        'shelves': [],
        'height_used': 0,
        'boxes': []
    }

def start_new_shelf():
    return {
        'height': 0,
        'width_used': 0,
        'boxes': []
    }

pallet = start_new_pallet()
shelf = start_new_shelf()

for idx, box in boxes_sorted.iterrows():
    box_length = box['length_cm']
    box_width = box['width_cm']
    box_height = box['height_cm']

    # Check if box fits in current shelf width-wise
    if shelf['width_used'] + box_width <= PALLET_WIDTH:
        # Check if shelf height accommodates box
        shelf['boxes'].append(box)
        shelf['width_used'] += box_width
        shelf['height'] = max(shelf['height'], box_height)
    else:
        # Shelf full, add shelf to pallet if height fits
        if pallet['height_used'] + shelf['height'] <= PALLET_HEIGHT:
            pallet['shelves'].append(shelf)
            pallet['height_used'] += shelf['height']
            pallet['boxes'].extend(shelf['boxes'])
            # Start new shelf
            shelf = start_new_shelf()
            # Place box on new shelf
            shelf['boxes'].append(box)
            shelf['width_used'] = box_width
            shelf['height'] = box_height
        else:
            # Pallet full, start new pallet
            pallets.append(pallet)
            pallet = start_new_pallet()
            shelf = start_new_shelf()
            # Place box on new shelf of new pallet
            shelf['boxes'].append(box)
            shelf['width_used'] = box_width
            shelf['height'] = box_height

# Add the last shelf and pallet
if shelf['boxes']:
    if pallet['height_used'] + shelf['height'] <= PALLET_HEIGHT:
        pallet['shelves'].append(shelf)
        pallet['height_used'] += shelf['height']
        pallet['boxes'].extend(shelf['boxes'])
    else:
        pallets.append(pallet)
        pallet = start_new_pallet()
        pallet['shelves'].append(shelf)
        pallet['height_used'] += shelf['height']
        pallet['boxes'].extend(shelf['boxes'])

if pallet['boxes']:
    pallets.append(pallet)

# --- Step 5: Reporting ---

print(f"\n📦 Boxes packed into {len(pallets)} pallet(s) using Layered (Shelf) heuristic:\n")

utilizations = []
box_counts = []

for i, p in enumerate(pallets):
    vol_used = sum(box['volume_L'] for box in p['boxes'])
    pallet_volume = (PALLET_LENGTH * PALLET_WIDTH * PALLET_HEIGHT) / 1000  # L
    utilization = vol_used / pallet_volume
    utilizations.append(utilization)
    box_counts.append(len(p['boxes']))

    print(f"  🪵 Pallet {i+1}: {len(p['boxes'])} boxes, {vol_used:.2f} L used ({utilization:.1%})")

# Summary
end_time = time.time()
runtime = end_time - start_time

print("\n📊 Summary:")
print(f"🔢 Number of pallets used: {len(pallets)}")
print(f"📦 Average pallet utilization: {sum(utilizations) / len(utilizations) * 100:.2f}%")
print(f"📦 Average box count per pallet: {sum(box_counts) / len(box_counts):.2f}")
print(f"⏱️ Runtime: {runtime:.3f} seconds")

# --- Optional: Preview first pallet's boxes ---
print("\n🔍 First pallet preview:")
first_pallet_boxes = pd.DataFrame(pallets[0]['boxes'])
print(first_pallet_boxes[['box_id', 'length_cm', 'width_cm', 'height_cm', 'volume_L', 'fragile']].head())
