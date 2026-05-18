# Basic ETL concepts

---

## What is ETL?

**ETL = Extract → Transform → Load**

It's a pipeline that moves data from a source, cleans/shapes it, and stores it somewhere useful.

```
Source                  Transform                  Destination
(CSV / API)    →    (clean, reshape, validate)   →   (PostgreSQL / file / warehouse)
```

Real-world example: every night, an e-commerce company pulls sales data from their API, cleans it (remove duplicates, fix types, validate), and loads it into a database for analysts to query.

---

## Step 1 — Extract

**Extract** means pulling raw data from a source. The data is untouched at this stage — you just get it in.

### From CSV
```python
import pandas as pd

df = pd.read_csv("data.csv")

# useful options
df = pd.read_csv(
    "data.csv",
    usecols=["id", "name", "price"],    # only load columns you need
    dtype={"price": float},             # prevent wrong type guesses
    parse_dates=["created_at"],         # auto-parse date columns
)
```

### From an API
```python
import requests

response = requests.get("https://api.example.com/sales")
data = response.json()                  # API returns JSON → Python dict/list

df = pd.DataFrame(data)                 # convert to DataFrame
# or if nested:
df = pd.DataFrame(data["results"])      # dig into the key that has the records
```

### Extract Rules
- Never modify data during extract — just get it in
- Always check `df.shape` and `df.head()` right after extracting
- Log how many rows you extracted — useful for debugging later

---

## Step 2 — Transform

**Transform** means cleaning, reshaping, and enriching the raw data so it's ready to load.

### Common Transform Operations

**1. Fix data types**
```python
df["price"]      = df["price"].astype(float)
df["created_at"] = pd.to_datetime(df["created_at"])
df["is_active"]  = df["is_active"].astype(bool)
```

**2. Handle missing values**
```python
df["price"].fillna(df["price"].median(), inplace=True)
df.dropna(subset=["id", "name"])        # drop rows where key columns are missing
```

**3. Remove duplicates**
```python
df.drop_duplicates(subset=["id"])       # keep first occurrence of each id
df.drop_duplicates(subset=["id"], keep="last")  # keep most recent
```

**4. Rename / standardize columns**
```python
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
# "First Name " → "first_name"
```

**5. Filter invalid rows**
```python
df = df[df["price"] > 0]               # remove negative prices
df = df[df["quantity"].notna()]         # remove rows with no quantity
```

**6. Add derived columns**
```python
df["revenue"]    = df["price"] * df["quantity"]
df["month"]      = df["created_at"].dt.month
df["is_premium"] = np.where(df["price"] >= 100, True, False)
```

**7. Aggregate if needed**
```python
daily = df.groupby("date").agg(
    total_revenue = ("revenue", "sum"),
    order_count   = ("id",      "count"),
).reset_index()
```

### Transform Rules
- Always work on a `.copy()` of extracted data
- Transform one thing at a time — easier to debug
- Log row count before and after each major step (did you lose rows unexpectedly?)

---

## Step 3 — Validate (Pydantic)

**Validation** is checking that data matches the expected shape and types before loading.

This sits between Transform and Load — you don't want corrupt data going into your database.

```python
from pydantic import BaseModel, validator
from typing import Optional

class SaleRecord(BaseModel):
    id:         int
    product:    str
    price:      float
    quantity:   int
    revenue:    float

    @validator("price")
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("price must be positive")
        return v

# validate one row
record = SaleRecord(id=1, product="Widget", price=29.99, quantity=5, revenue=149.95)

# validate all rows (loop over DataFrame rows)
valid_records = []
for row in df.to_dict("records"):       # convert each row to a dict
    try:
        valid_records.append(SaleRecord(**row))
    except Exception as e:
        print(f"Invalid row: {row} — {e}")  # log bad rows, skip them
```

**Why Pydantic?**
- Catches type errors before they hit the database
- Self-documents what a valid record looks like
- Better error messages than manual if/else checks

---

## Step 4 — Load

**Load** means writing the cleaned, validated data to its destination.

### To CSV (simplest)
```python
df.to_csv("output.csv", index=False)
```

### To PostgreSQL
```python
from sqlalchemy import create_engine

# connection string format: postgresql://user:password@host:port/database
engine = create_engine("postgresql://postgres:password@localhost:5432/mydb")

df.to_sql(
    name="sales",           # table name
    con=engine,
    if_exists="append",     # "replace" (drop+recreate) or "append" (add rows) or "fail"
    index=False,            # don't write the DataFrame index as a column
)
```

### Load Rules
- Use `if_exists="append"` for incremental loads (daily runs adding new data)
- Use `if_exists="replace"` only for full refreshes (reloading everything)
- Always verify row count after loading — query the DB and compare

---

## Putting It All Together — Pipeline Pattern

```python
def extract(filepath):
    df = pd.read_csv(filepath)
    print(f"Extracted {len(df)} rows")
    return df

def transform(df):
    df = df.copy()
    df.columns = df.columns.str.lower().str.strip()
    df["price"] = df["price"].astype(float)
    df = df.dropna(subset=["id", "price"])
    df = df[df["price"] > 0]
    df["revenue"] = df["price"] * df["quantity"]
    print(f"After transform: {len(df)} rows")
    return df

def validate(df):
    valid = []
    for row in df.to_dict("records"):
        try:
            valid.append(SaleRecord(**row))
        except Exception as e:
            print(f"Skipped: {e}")
    print(f"Valid records: {len(valid)}")
    return valid

def load(records, engine):
    df = pd.DataFrame([r.dict() for r in records])
    df.to_sql("sales", con=engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows")

# run the pipeline
raw     = extract("sales.csv")
cleaned = transform(raw)
valid   = validate(cleaned)
load(valid, engine)
```

---

## Key Concepts Summary

| Term | Meaning |
|------|---------|
| Extract | Pull raw data from source (CSV, API, DB) — don't modify yet |
| Transform | Clean, reshape, enrich with pandas |
| Validate | Check shape/types with Pydantic before loading |
| Load | Write to destination (PostgreSQL, file) |
| `if_exists="append"` | Add new rows to existing table |
| `if_exists="replace"` | Drop and recreate the table |
| `to_dict("records")` | Convert DataFrame to list of dicts — one dict per row |
| Incremental load | Only process new/changed data (efficient for large datasets) |
| Full refresh | Reload everything from scratch |

---
