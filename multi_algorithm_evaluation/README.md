# Multi-Algorithm Evaluation on Synthetic Picking Lists

This folder contains Python scripts implementing and evaluating mixed-palletizing algorithms using synthetic box datasets designed to reflect real-world warehouse operations.

## Algorithms Implemented

The following palletizing algorithms were custom-implemented and tested on four randomized picking lists derived from the [boxes_database_500.xlsx](https://github.com/Adamos-Daios/package-db-distributions/blob/main/boxes_database/boxes_database_500.xlsx)

- [First Fit Decreasing (FFD)](./Test_1_FFD.py)
- [Extreme Point (EP)](./Test_2_EP.py)
- [Guillotine Cut](./Test_3_Guilotine_Cut.py)
- [Layered (Shelf)](./Test_4_Layered_Shelf.py)
- [Genetic Algorithm](./Test_5_GA.py)
- [Tabu Search (TS)](./Test_6_TS.py)

## Test Scenarios

Using the `box_filter` API, four randomized picking lists of varying sizes were generated:

- **Light orders (20 items):** Small, quick-fulfillment shipments                       [boxes_20.xlsx](./boxes_20.xlsx)
- **Typical orders (35 items):** Standard daily warehouse orders                        [boxes_35.xlsx](./boxes_35.xlsx)
- **Heavy orders (50 items):** Larger restocking or retail shipments                    [boxes_50.xlsx](./boxes_50.xlsx)
- **Overflow orders (100 items):** Peak demand or bulk consolidation loads              [boxes_100.xlsx](./boxes_100.xlsx) 


