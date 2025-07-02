# Multi-Algorithm Evaluation on Synthetic Picking Lists

This folder contains Python scripts implementing and evaluating mixed-palletizing algorithms using synthetic box datasets designed to reflect real-world warehouse operations.

## Algorithms Implemented

The following palletizing algorithms were custom-implemented and tested on four randomized picking lists derived from the [boxes_database_500.xlsx](https://github.com/Adamos-Daios/package-db-distributions/blob/main/boxes_database/boxes_database_500.xlsx)

- First Fit Decreasing (FFD)
- Extreme Point (EP)
- Guillotine Cut
- Layered (Shelf)
- Genetic Algorithm
- Tabu Search (TS)

## Test Scenarios

Using the `box_filter` API, four randomized picking lists of varying sizes were generated:

- **Light orders (20 items):** Small, quick-fulfillment shipments  
- **Typical orders (35 items):** Standard daily warehouse orders  
- **Heavy orders (50 items):** Larger restocking or retail shipments  
- **Overflow orders (100 items):** Peak demand or bulk consolidation loads  


