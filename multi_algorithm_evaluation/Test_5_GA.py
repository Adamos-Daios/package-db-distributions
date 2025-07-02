import pandas as pd
import numpy as np
import time

# --- Step 1: Load Dataset ---
file_path = "/content/boxes_100.xlsx"  # Make sure to upload your file in Colab
df = pd.read_excel(file_path)

# Rename columns for convenience
df = df.rename(columns={
    'Length (cm)': 'length',
    'Width (cm)': 'width',
    'Height (cm)': 'height',
    'External Volume (L)': 'volume',
    'Box ID': 'box_id'
})

# --- Step 2: Constants ---
PALLET_LENGTH = 120  # cm
PALLET_WIDTH = 100   # cm
PALLET_HEIGHT = 85   # cm
PALLET_VOLUME = (PALLET_LENGTH * PALLET_WIDTH * PALLET_HEIGHT) / 1000  # convert cm³ to liters (1L=1000cm³)

# --- Step 3: Genetic Algorithm parameters ---
POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1

# --- Step 4: Fitness Function ---
def fitness(order):
    total_vol = 0
    pallets_used = 1
    current_vol = 0
    for idx in order:
        box_vol = df.iloc[idx]['volume']
        if current_vol + box_vol <= PALLET_VOLUME:
            current_vol += box_vol
        else:
            pallets_used += 1
            current_vol = box_vol
        total_vol += box_vol
    # We want to minimize pallets used and maximize volume packed per pallet
    # Fitness could be inverse of pallets used or combination; here we penalize pallets used
    return -pallets_used  # negative because GA maximizes fitness by default

# --- Step 5: Initialize Population ---
def init_population(size, n_items):
    population = []
    for _ in range(size):
        individual = np.random.permutation(n_items)
        population.append(individual)
    return population

# --- Step 6: Selection (Tournament) ---
def tournament_selection(pop, fitnesses, k=3):
    selected = []
    for _ in range(len(pop)):
        aspirants_idx = np.random.choice(len(pop), k)
        aspirants_fitness = [fitnesses[i] for i in aspirants_idx]
        winner_idx = aspirants_idx[np.argmax(aspirants_fitness)]
        selected.append(pop[winner_idx])
    return selected

# --- Step 7: Crossover (Order Crossover) ---
def order_crossover(parent1, parent2):
    size = len(parent1)
    a, b = sorted(np.random.choice(range(size), 2, replace=False))
    child = [None]*size
    child[a:b+1] = parent1[a:b+1]
    fill_pos = (b+1) % size
    parent2_pos = (b+1) % size
    while None in child:
        if parent2[parent2_pos] not in child:
            child[fill_pos] = parent2[parent2_pos]
            fill_pos = (fill_pos + 1) % size
        parent2_pos = (parent2_pos + 1) % size
    return np.array(child)

# --- Step 8: Mutation (Swap Mutation) ---
def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if np.random.rand() < mutation_rate:
            j = np.random.randint(len(individual))
            individual[i], individual[j] = individual[j], individual[i]

# --- Step 9: Genetic Algorithm ---
def genetic_algorithm():
    n_items = len(df)
    population = init_population(POPULATION_SIZE, n_items)
    best_solution = None
    best_fitness = float('-inf')

    for gen in range(GENERATIONS):
        fitnesses = [fitness(ind) for ind in population]

        max_fitness = max(fitnesses)
        if max_fitness > best_fitness:
            best_fitness = max_fitness
            best_solution = population[fitnesses.index(max_fitness)]

        if gen % 10 == 0 or gen == GENERATIONS-1:
            print(f"Generation {gen+1}, Best Fitness: {-best_fitness}")  # Show pallets used as positive number

        selected = tournament_selection(population, fitnesses)
        next_population = []

        for i in range(0, POPULATION_SIZE, 2):
            parent1 = selected[i]
            parent2 = selected[(i+1) % POPULATION_SIZE]
            child1 = order_crossover(parent1, parent2)
            child2 = order_crossover(parent2, parent1)
            mutate(child1, MUTATION_RATE)
            mutate(child2, MUTATION_RATE)
            next_population.extend([child1, child2])

        population = next_population[:POPULATION_SIZE]

    return best_solution

# --- Step 10: Pack boxes into pallets from best solution ---
def pack_into_pallets(order):
    pallets = []
    current_pallet = []
    current_vol = 0

    for idx in order:
        box_vol = df.iloc[idx]['volume']
        if current_vol + box_vol <= PALLET_VOLUME:
            current_pallet.append(idx)
            current_vol += box_vol
        else:
            pallets.append(current_pallet)
            current_pallet = [idx]
            current_vol = box_vol
    if current_pallet:
        pallets.append(current_pallet)
    return pallets

# --- Step 11: Run GA and report ---
start_time = time.time()
best_solution = genetic_algorithm()
end_time = time.time()

pallets = pack_into_pallets(best_solution)
num_pallets = len(pallets)
utilizations = []
box_counts = []

for p in pallets:
    vol_used = sum(df.iloc[idx]['volume'] for idx in p)
    utilization = vol_used / PALLET_VOLUME
    utilizations.append(utilization)
    box_counts.append(len(p))

avg_utilization = sum(utilizations) / num_pallets * 100
avg_box_count = sum(box_counts) / num_pallets

print("\n📊 GA Packing Summary:")
print(f"🔢 Number of pallets used: {num_pallets}")
print(f"📦 Average pallet utilization: {avg_utilization:.2f}%")
print(f"📦 Average box count per pallet: {avg_box_count:.2f}")
print(f"⏱️ Algorithm runtime: {end_time - start_time:.2f} seconds")
