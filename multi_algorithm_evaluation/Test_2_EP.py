import pandas as pd
import time
import sys
import platform

# --- Pallet dimensions (cm) ---
PALLET_LENGTH = 120  # 1.2 meters
PALLET_WIDTH = 100   # 1.0 meters
PALLET_HEIGHT = 85   # 0.85 meters

# --- Load your box dataset ---
file_path = "/content/boxes_100.xlsx"  # Upload your file to Colab
df = pd.read_excel(file_path)

# Rename columns for convenience
df = df.rename(columns={
    'Box ID': 'box_id',
    'Length (cm)': 'length_cm',
    'Width (cm)': 'width_cm',
    'Height (cm)': 'height_cm',
    'External Volume (L)': 'volume_L',
    'Fragile': 'fragile'
})

# Basic validation
valid = (
    (df['length_cm'] > 0) &
    (df['width_cm'] > 0) &
    (df['height_cm'] > 0)
)
df = df[valid].reset_index(drop=True)
print(f"✅ Loaded {len(df)} valid boxes")

# Sort boxes by volume descending (largest first)
df = df.sort_values(by='volume_L', ascending=False).reset_index(drop=True)

# --- Extreme Point Heuristic Implementation ---
class Pallet:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.boxes = []
        self.extreme_points = [(0, 0, 0)]  # Start with origin point

    def can_place(self, box, point):
        x, y, z = point
        # Check if box fits within pallet bounds
        if (x + box['length_cm'] > self.length or
            y + box['width_cm'] > self.width or
            z + box['height_cm'] > self.height):
            return False

        # Check overlap with already placed boxes
        for b in self.boxes:
            if not (
                x + box['length_cm'] <= b['pos_x'] or
                b['pos_x'] + b['length_cm'] <= x or
                y + box['width_cm'] <= b['pos_y'] or
                b['pos_y'] + b['width_cm'] <= y or
                z + box['height_cm'] <= b['pos_z'] or
                b['pos_z'] + b['height_cm'] <= z
            ):
                return False
        return True

    def place_box(self, box):
        # Try all extreme points to place the box
        for i, point in enumerate(self.extreme_points):
            if self.can_place(box, point):
                # Place the box here
                placed_box = box.copy()
                placed_box['pos_x'], placed_box['pos_y'], placed_box['pos_z'] = point
                self.boxes.append(placed_box)

                # Update extreme points:
                # Remove current point and add new ones at the top and sides of the placed box
                del self.extreme_points[i]

                new_points = [
                    (point[0] + box['length_cm'], point[1], point[2]),
                    (point[0], point[1] + box['width_cm'], point[2]),
                    (point[0], point[1], point[2] + box['height_cm'])
                ]

                for np in new_points:
                    if np not in self.extreme_points and self.is_within_bounds(np):
                        self.extreme_points.append(np)
                return True
        return False

    def is_within_bounds(self, point):
        x, y, z = point
        return x <= self.length and y <= self.width and z <= self.height

# --- Pack boxes into pallets ---
start_time = time.time()
pallets = []

for idx, box in df.iterrows():
    placed = False
    for pallet in pallets:
        if pallet.place_box(box):
            placed = True
            break
    if not placed:
        # Create new pallet
        p = Pallet(PALLET_LENGTH, PALLET_WIDTH, PALLET_HEIGHT)
        if not p.place_box(box):
            raise ValueError(f"Box {box['box_id']} too large to fit in an empty pallet")
        pallets.append(p)

end_time = time.time()

# --- Reporting ---
print(f"\n📦 Packed {len(df)} boxes into {len(pallets)} pallet(s) using Extreme Point heuristic.\n")

utilizations = []
box_counts = []

# Calculate pallet volume in liters (cm³ to liters)
pallet_vol = PALLET_LENGTH * PALLET_WIDTH * PALLET_HEIGHT / 1000  # 1020 liters

for i, pallet in enumerate(pallets):
    vol_used = sum([b['volume_L'] for b in pallet.boxes])
    utilization = vol_used / pallet_vol
    utilizations.append(utilization)
    box_counts.append(len(pallet.boxes))
    print(f"  🪵 Pallet {i+1}: {len(pallet.boxes)} boxes, {vol_used:.2f} L used ({utilization:.1%} utilization)")

print("\n📊 Summary:")
print(f"🔢 Number of pallets used: {len(pallets)}")
print(f"📦 Average pallet volume utilization: {sum(utilizations) / len(utilizations) * 100:.2f}%")
print(f"📦 Average box count per pallet: {sum(box_counts) / len(box_counts):.2f}")
print(f"⏱️ Runtime: {end_time - start_time:.3f} seconds")

# --- Preview first pallet's boxes ---
print("\n🔍 First pallet preview:")
first_pallet_df = pd.DataFrame(pallets[0].boxes)
print(first_pallet_df[['box_id', 'length_cm', 'width_cm', 'height_cm', 'volume_L', 'pos_x', 'pos_y', 'pos_z']].head())

# --- Environment info ---
print("\n🖥️ Environment Information:")
print(f"Python version: {sys.version}")
print(f"Platform: {platform.platform()}")
