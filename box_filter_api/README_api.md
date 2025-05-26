## 📅 Excel to API Workflow – Picking List Generator

This section explains how to transform the Excel box database into a `.db` file and run a FastAPI server that provides random box selections via HTTP.

---

### 🦨 Step-by-Step Instructions

#### 1. ✅ Download the Excel File

Choose an Excel file from the [boxes_database folder](https://github.com/Adamos-Daios/package-db-distributions/tree/main/boxes_database), e.g., `boxes_10000.xlsx`, and save it locally.

#### 2. 🔄 Convert Excel to Database

Download the  [`import_excel.py`](https://github.com/Adamos-Daios/package-db-distributions/blob/main/box_filter_api/import_excel.py) script from this repository and run:

```bash
python import_excel.py
```

This will create a `.db` (SQLite) file that the API will use.

---

### ⚙️ API Setup Instructions

#### 3. 📁 Navigate to Your Project Folder

```bash
mkdir box_filter_api
cd box_filter_api
```


#### 4. 🧪 Create a Virtual Environment

```bash
python -m venv env
```

#### 5. ▶️ Activate the Virtual Environment

```bash
.\env\Scripts\activate   # On Windows
# source env/bin/activate   # On macOS/Linux
```

#### 6. 📦 Install Required Packages

```bash
pip install fastapi uvicorn pandas openpyxl
pip list
```

#### 7. 🔁 (If the Excel file changes)

Run again:

```bash
python import_excel.py
```

---

#### 8. 🚀 Run the FastAPI Server

Download the [`main.py`](https://github.com/Adamos-Daios/package-db-distributions/blob/main/box_filter_api/main.py) script if you haven’t already, then run:


```bash
uvicorn main:app --reload
```

Open in your browser:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

This opens the interactive Swagger UI for testing.

---

#### 9. 📁 Stop the Server

Press `Ctrl + C` in the terminal window to stop the server.

---

#### 10. 🧠 Arduino or Client Integration

Arduino or other clients can access the API using `http://127.0.0.1:8000`.

---

## 🔗 Useful Links

- **Boxes Database Folder**: [boxes_database](https://github.com/Adamos-Daios/package-db-distributions/tree/main/boxes_database)
- **import_excel.py Script**: [import_excel.py](https://github.com/Adamos-Daios/package-db-distributions/blob/main/box_filter_api/import_excel.py)
- **main.py Script**: [main.py](https://github.com/Adamos-Daios/package-db-distributions/blob/main/box_filter_api/main.py)

