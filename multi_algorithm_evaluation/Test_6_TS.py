import pandas as pd
import time
import random
from copy import deepcopy

# --- Step 1: Load your dataset ---
file_path = "/content/boxes_100.xlsx"  # Upload this file to Colab files

df = pd.read_excel(file_path)

# Rename for convenience
df = df.rename(columns={
    'Box ID': 'box_id',
    'Length (cm)': 'length_cm',
    'Width (cm)': 'width_cm',
    'Height (cm)': 'height_cm',
    'External Volume (L)': 'volume_L',
    'Max Load Capacity (kg)': 'max_load_kg',
    'Fragile': 'fragile',
    'Stackable': 'stackable',
})

# Convert Fragile and Stackable to boolean if necessary
df['fragile'] = df['fragile'].astype(str).str.lower().map({'yes': True, 'no': False})
df['stackable'] = df['stackable'].astype(str).str.lower().map({'yes': True, 'no': False})

# Fill NAs if any
df['fragile'] = df['fragile'].fillna(False)
df['stackable'] = df['stackable'].fillna(True)

# Create box list with needed attributes
boxes = df.to_dict('records')

# --- Step 2: Constants ---
PALLET_LENGTH = 120  # cm
PALLET_WIDTH = 100   # cm
PALLET_HEIGHT = 85   # cm
PALLET_VOLUME_L = (PALLET_LENGTH / 100) * (PALLET_WIDTH / 100) * (PALLET_HEIGHT / 100) * 1000  # liters

# Weight constraint can be added here if you want
PALLET_MAX_WEIGHT = None  # e.g., 1000  # kg, or None to ignore

# --- Step 3: Helper functions ---

def is_valid_pallet(pallet):
    # Check volume
    total_vol = sum(box['volume_L'] for box in pallet)
    if total_vol > PALLET_VOLUME_L:
        return False
    # Check weight if needed
    if PALLET_MAX_WEIGHT is not None:
        total_weight = sum(box['max_load_kg'] for box in pallet)
        if total_weight > PALLET_MAX_WEIGHT:
            return False
    # Fragile boxes should be on top: simplistic check - no fragile box below non-fragile
    # For demo: If any fragile box and any non-stackable box in same pallet, reject
    fragile_boxes = [box for box in pallet if box['fragile']]
    if fragile_boxes:
        non_stackable = [box for box in pallet if not box['stackable']]
        if non_stackable:
            return False
    return True

def initial_solution(boxes):
    """Simple greedy packing by volume."""
    pallets = []
    current_pallet = []
    current_vol = 0
    for box in boxes:
        if current_vol + box['volume_L'] <= PALLET_VOLUME_L:
            current_pallet.append(box)
            current_vol += box['volume_L']
        else:
            pallets.append(current_pallet)
            current_pallet = [box]
            current_vol = box['volume_L']
    if current_pallet:
        pallets.append(current_pallet)
    return pallets

def evaluate(pallets):
    """Objective: minimize pallets, maximize utilization."""
    num_pallets = len(pallets)
    utilizations = [sum(box['volume_L'] for box in p) / PALLET_VOLUME_L for p in pallets]
    avg_util = sum(utilizations) / num_pallets
    score = num_pallets - avg_util  # Lower is better
    return score

def neighbors(solution):
    """Generate neighbors by swapping boxes between pallets."""
    neighbors = []
    for i in range(len(solution)):
        for j in range(i+1, len(solution)):
            for box_i in solution[i]:
                for box_j in solution[j]:
                    new_solution = deepcopy(solution)
                    new_solution[i].remove(box_i)
                    new_solution[j].remove(box_j)
                    new_solution[i].append(box_j)
                    new_solution[j].append(box_i)
                    # Validate pallets after swap
                    if is_valid_pallet(new_solution[i]) and is_valid_pallet(new_solution[j]):
                        neighbors.append(new_solution)
    return neighbors

# --- Step 4: Tabu Search algorithm ---

def tabu_search(boxes, max_iter=100, tabu_size=20):
    current_solution = initial_solution(boxes)
    best_solution = current_solution
    best_score = evaluate(best_solution)
    tabu_list = []

    for iteration in range(max_iter):
        neighborhood = neighbors(current_solution)
        neighborhood = [sol for sol in neighborhood if sol not in tabu_list]
        if not neighborhood:
            print("No valid neighbors found, stopping early.")
            break
        scores = [evaluate(sol) for sol in neighborhood]
        best_neighbor = neighborhood[scores.index(min(scores))]
        best_neighbor_score = min(scores)

        if best_neighbor_score < best_score:
            best_solution = best_neighbor
            best_score = best_neighbor_score

        tabu_list.append(best_neighbor)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        current_solution = best_neighbor
        print(f"Iteration {iteration+1}, Best Score: {best_score:.4f}")

    return best_solution

# --- Step 5: Run Tabu Search ---

start_time = time.time()
final_solution = tabu_search(boxes, max_iter=50)
end_time = time.time()

# --- Step 6: Reporting ---

num_pallets = len(final_solution)
avg_util = sum(sum(box['volume_L'] for box in p) / PALLET_VOLUME_L for p in final_solution) / num_pallets
avg_box_count = sum(len(p) for p in final_solution) / num_pallets

print("\n📝 Tabu Search Result:")
print(f"Number of pallets used: {num_pallets}")
print(f"Average pallet utilization: {avg_util * 100:.2f}%")
print(f"Average box count per pallet: {avg_box_count:.2f}")
print(f"Runtime: {end_time - start_time:.2f} seconds")
