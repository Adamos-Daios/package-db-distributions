from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from typing import Optional, Literal
import sqlite3
import pandas as pd
from io import BytesIO, StringIO
import random

app = FastAPI()

# Define enums for dropdowns
MaterialEnum = Literal["Cardboard", "Plastic", "Wood", "Metal", "Composite"]
ColorEnum = Literal["White", "Gray", "Brown", "Light Brown", "Deep Brown", "Yellow", "Light Yellow", "Dark Yellow"]
CountryEnum = Literal["Greece", "Germany", "China", "USA", "India", "Mexico", "Japan", "Australia", "France"]
YesNoEnum = Literal["Yes", "No"]

def run_query(
    min_length=None, max_length=None,
    min_width=None, max_width=None,
    min_height=None, max_height=None,
    min_thickness=None, max_thickness=None,
    min_volume=None, max_volume=None,
    min_load_capacity=None,
    min_temp=None, max_temp=None,
    material=None, fragile=None,
    stackable=None, waterproof=None, fire_retardant=None,
    color=None, country=None,
    limit=None
):
    conn = sqlite3.connect("packages.db")
    cursor = conn.cursor()

    query = "SELECT * FROM boxes WHERE 1=1"
    params = []

    # Dimension filters
    if min_length: query += " AND `Length (cm)` >= ?"; params.append(min_length)
    if max_length: query += " AND `Length (cm)` <= ?"; params.append(max_length)
    if min_width: query += " AND `Width (cm)` >= ?"; params.append(min_width)
    if max_width: query += " AND `Width (cm)` <= ?"; params.append(max_width)
    if min_height: query += " AND `Height (cm)` >= ?"; params.append(min_height)
    if max_height: query += " AND `Height (cm)` <= ?"; params.append(max_height)
    if min_thickness: query += " AND `Thickness (cm)` >= ?"; params.append(min_thickness)
    if max_thickness: query += " AND `Thickness (cm)` <= ?"; params.append(max_thickness)

    # Volume & weight
    if min_volume: query += " AND `External Volume (L)` >= ?"; params.append(min_volume)
    if max_volume: query += " AND `External Volume (L)` <= ?"; params.append(max_volume)
    if min_load_capacity: query += " AND `Max Load Capacity (kg)` >= ?"; params.append(min_load_capacity)

    # Temperature
    if min_temp: query += " AND `Min Temperature (°C)` >= ?"; params.append(min_temp)
    if max_temp: query += " AND `Max Temperature (°C)` <= ?"; params.append(max_temp)

    # Material & Attributes
    if material: query += " AND Material = ?"; params.append(material)
    if fragile: query += " AND Fragile = ?"; params.append(fragile)
    if stackable: query += " AND Stackable = ?"; params.append(stackable)
    if waterproof: query += " AND Waterproof = ?"; params.append(waterproof)
    if fire_retardant: query += " AND `Fire Retardant` = ?"; params.append(fire_retardant)

    # Colors & Origin
    if color: query += " AND Color = ?"; params.append(color)
    if country: query += " AND `Country of Origin` = ?"; params.append(country)

    # Randomization
    query += " ORDER BY RANDOM()"
    # No LIMIT here – handled in Python when needed
    cursor.execute(query, params)
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return results


@app.get("/download/csv")
def download_csv(
    min_length: Optional[float] = Query(None, ge=20, le=100),
    max_length: Optional[float] = Query(None, ge=20, le=100),
    min_width: Optional[float] = Query(None, ge=5, le=99),
    max_width: Optional[float] = Query(None, ge=5, le=99),
    min_height: Optional[float] = Query(None, ge=5, le=95),
    max_height: Optional[float] = Query(None, ge=5, le=95),
    min_thickness: Optional[float] = Query(None),
    max_thickness: Optional[float] = Query(None),
    min_volume: Optional[float] = Query(None),
    max_volume: Optional[float] = Query(None),
    min_load_capacity: Optional[float] = Query(None),
    min_temp: Optional[int] = Query(None, ge=-45, le=120),
    max_temp: Optional[int] = Query(None, ge=-45, le=120),
    material: Optional[MaterialEnum] = Query(None),
    fragile: Optional[YesNoEnum] = Query(None),
    stackable: Optional[YesNoEnum] = Query(None),
    waterproof: Optional[YesNoEnum] = Query(None),
    fire_retardant: Optional[YesNoEnum] = Query(None),
    color: Optional[ColorEnum] = Query(None),
    country: Optional[CountryEnum] = Query(None),
    limit: Optional[int] = Query(100),
    sample_with_replacement: Optional[bool] = Query(False, description="Allow duplicate boxes (sample with replacement)")
):
    raw_results = run_query(
        min_length, max_length,
        min_width, max_width,
        min_height, max_height,
        min_thickness, max_thickness,
        min_volume, max_volume,
        min_load_capacity,
        min_temp, max_temp,
        material, fragile,
        stackable, waterproof, fire_retardant,
        color, country,
        None  # no LIMIT in SQL
    )

    if sample_with_replacement and limit and raw_results:
        results = random.choices(raw_results, k=limit)
    else:
        results = raw_results[:limit] if limit else raw_results

    df = pd.DataFrame(results)
    csv = df.to_csv(index=False)
    return StreamingResponse(StringIO(csv), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=boxes.csv"})


@app.get("/download/excel")
def download_excel(
    min_length: Optional[float] = Query(None, ge=20, le=100),
    max_length: Optional[float] = Query(None, ge=20, le=100),
    min_width: Optional[float] = Query(None, ge=5, le=99),
    max_width: Optional[float] = Query(None, ge=5, le=99),
    min_height: Optional[float] = Query(None, ge=5, le=95),
    max_height: Optional[float] = Query(None, ge=5, le=95),
    min_thickness: Optional[float] = Query(None),
    max_thickness: Optional[float] = Query(None),
    min_volume: Optional[float] = Query(None),
    max_volume: Optional[float] = Query(None),
    min_load_capacity: Optional[float] = Query(None),
    min_temp: Optional[int] = Query(None, ge=-45, le=120),
    max_temp: Optional[int] = Query(None, ge=-45, le=120),
    material: Optional[MaterialEnum] = Query(None),
    fragile: Optional[YesNoEnum] = Query(None),
    stackable: Optional[YesNoEnum] = Query(None),
    waterproof: Optional[YesNoEnum] = Query(None),
    fire_retardant: Optional[YesNoEnum] = Query(None),
    color: Optional[ColorEnum] = Query(None),
    country: Optional[CountryEnum] = Query(None),
    limit: Optional[int] = Query(100),
    sample_with_replacement: Optional[bool] = Query(False, description="Allow duplicate boxes (sample with replacement)")
):
    raw_results = run_query(
        min_length, max_length,
        min_width, max_width,
        min_height, max_height,
        min_thickness, max_thickness,
        min_volume, max_volume,
        min_load_capacity,
        min_temp, max_temp,
        material, fragile,
        stackable, waterproof, fire_retardant,
        color, country,
        None  # no LIMIT in SQL
    )

    if sample_with_replacement and limit and raw_results:
        results = random.choices(raw_results, k=limit)
    else:
        results = raw_results[:limit] if limit else raw_results

    df = pd.DataFrame(results)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Boxes")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=boxes.xlsx"}
    )
