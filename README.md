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

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.



