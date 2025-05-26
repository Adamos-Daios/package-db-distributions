# Box Database Generator

A lightweight Python utility that creates versioned Excel datasets of box specifications for easy distribution.

---

## 📦 Key Features

* **Material Diversity**: Generates boxes made of Cardboard, Plastic, Wood, Metal, and Composite.
* **Dimensional Randomization**: Random lengths, widths, heights, and thicknesses within material-specific ranges.
* **Property Calculation**: Computes external/internal volumes and max load capacity.
* **Attribute Flags**: Assigns fragile, stackable, waterproof, and fire-retardant flags.
* **Environmental Ranges**: Random safe temperature limits for each material.
* **Metadata**: Includes box color and country of origin.

---

## ⚙️ Setup

1. **Clone repo**

   ```bash
   git clone https://github.com/your-username/box-database-generator.git
   cd box-database-generator
   ```
2. **Install deps**

   ```bash
   pip install pandas
   ```

---

## ▶️ Usage

* Open `generate_boxes.py`.
* Set the desired number of records (default: 10,000).
* Run:

  ```bash
  python generate_boxes.py
  ```
* Result: `boxes_database.xlsx` saved in the working directory.

---
📁 Pre-Generated Datasets
A collection of ready-to-use Excel datasets is available in the boxes_database/ folder. These files include:

boxes_500.xlsx

boxes_1000.xlsx

boxes_3000.xlsx

boxes_5000.xlsx

boxes_10000.xlsx

boxes_50000.xlsx

boxes_100000.xlsx

Each file contains a fixed number of randomly generated box records, following the same structure.

🧪 Research Applications
These datasets are intended for researchers exploring the Mixed Palletizing Problem or similar logistics/optimization tasks.

Fellow researchers are encouraged to:

Use these standardized datasets for testing and benchmarking.

Share results obtained using these databases to foster reproducibility and comparison.

Cite this repository when referencing results derived from the included files.

By using common datasets, the community can ensure consistency in evaluating different algorithmic approaches.


## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.



