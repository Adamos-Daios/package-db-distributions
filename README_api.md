📥 Excel to API Workflow – Picking List Generator
This section describes how to convert an Excel box dataset into a .db file and run a FastAPI web app to extract random box samples for testing and integration (e.g., with Arduino).

🪜 Step-by-Step Instructions
1. ✅ Download the Excel File
Choose the Excel database file (e.g., boxes_10000.xlsx) from the boxes_database folder and save it locally.

2. 🔄 Convert Excel to Database
Download the import_excel.py script and run:

```bash
python import_excel.py
This will convert the Excel file into a lightweight .db (SQLite) file used by the API.
```
⚙️ API Setup Instructions
3. 📁 Navigate to Your Project Folder
```bash
mkdir box_filter_api
cd box_filter_api
```
Or if already created:

```bash
cd C:\Users\adamo\package-picker\box_filter_api
```

4. 🧪 Create a Virtual Environment
```bash
python -m venv env
```

6. ▶️ Activate the Virtual Environment
```
bash
.\env\Scripts\activate   # On Windows
# source env/bin/activate   # On macOS/Linux
```

6. 📦 Install Required Packages
   
```
bash
pip install fastapi uvicorn pandas openpyxl
pip list
```

8. 🔁 (If the Excel file changes)
Any time the Excel file is updated or replaced, rerun:

```
bash
python import_excel.py
```

8. 🚀 Run the FastAPI Server

```
bash
uvicorn main:app --reload
```

Open your browser and visit:

👉 http://127.0.0.1:8000/docs – interactive Swagger UI.

9. 🛑 To Stop the Server
Press Ctrl + C in the terminal.

10. 🧠 Arduino Integration
Arduino or any other client can access the API through HTTP calls to http://127.0.0.1:8000.
