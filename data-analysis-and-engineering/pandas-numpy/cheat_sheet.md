# Pandas Cheat Sheet — Days 29–33

---

## Pandas Fundamentals

### Inspect
```python
df.shape                        # (rows, cols)
df.info()                       # types + null counts
df.describe()                   # stats for numeric cols
df.head()                       # first 5 rows
df.isnull().sum()               # missing per column
df["col"].value_counts()        # frequency count per unique value
```

### Select
```python
df["col"]                       # one column → Series
df[["col1", "col2"]]            # multiple columns → DataFrame
df.loc[label, "col"]            # by label — slice is INCLUSIVE on both ends
df.iloc[pos, 0]                 # by position — slice is EXCLUSIVE on end
```

### Filter
```python
df[df["col"] > val]                                   # single condition
df[(df["a"] > 1) & (df["b"] == "x")]                  # AND — use &, not 'and'
df[(df["a"] > 1) | (df["b"] == "x")]                  # OR  — use |, not 'or'
df[~(df["col"] == "x")]                               # NOT — use ~
df.query("col > 1 and dept == 'Eng'")                 # cleaner syntax
```

### Modify (vectorized — no loops)
```python
df["new"] = df["a"] * df["b"]                         # add column
df["col"].fillna(df["col"].median())                  # fill NaN (numbers → median)
df["col"].fillna("Unknown")                           # fill NaN (categories)
df.dropna()                                           # drop rows with NaN
df.rename(columns={"old": "new"})                     # rename columns
df.drop(columns=["col"])                              # remove columns
df.sort_values("col", ascending=False)                # sort
df2 = df[["col1", "col2"]].copy()                     # always .copy() before modifying a slice
```

### String Operations (.str accessor)
```python
df["col"].str.lower()
df["col"].str.upper()
df["col"].str.strip()                                 # remove whitespace
df["col"].str.len()                                   # length of each string
df["col"].str.contains("x", case=False)               # → boolean mask, wrap in df[...] to filter
df["col"].str.replace("old", "new")
```

### ⚠️ Key Rules
- `loc` slice is **inclusive** both ends. `iloc` slice is **exclusive** end (like Python).
- After filtering, labels have gaps — use `iloc` for position, `loc` for label.
- Never use `and`/`or` for combining conditions — use `&`/`|` with parentheses around each condition.
- NaN is contagious — always check with `isnull().sum()` before doing math.
- Always `.copy()` before modifying a filtered/sliced DataFrame.

---

## GroupBy & Aggregation

### Basic GroupBy
```python
df.groupby("col")["target"].mean()                    # one aggregation
df.groupby("col")["target"].agg(["mean", "max", "count"])  # multiple on one column
```

### Named Aggregations (default choice)
```python
df.groupby("col").agg(
    new_name  = ("source_col",  "func"),              # func: sum, mean, min, max, count, std
    new_name2 = ("source_col2", "func2"),
).reset_index()
```

### Dict Aggregation (different func per column)
```python
df.groupby("col").agg({
    "salary":    "mean",
    "years_exp": "sum",
    "rating":    "max",
})
```

### `agg()` vs `transform()`
```python
# agg — one row per group (collapsed)
df.groupby("dept")["salary"].agg("mean")              # shape: (n_groups,)

# transform — same shape as original df (broadcast back)
df["dept_avg"] = df.groupby("dept")["salary"].transform("mean")  # shape: (n_rows,)
# use transform when you want to add a column back to the original df
```

### Multi-Level GroupBy
```python
df.groupby(["col1", "col2"])["target"].mean().reset_index()
# order matters — first column = outer group, second = inner group
```

### Custom Lambda
```python
df.groupby("col")["target"].agg(lambda x: x.max() - x.min())

# named version
df.groupby("col").agg(
    salary_range = ("salary", lambda x: x.max() - x.min()),
    above_avg    = ("salary", lambda x: (x > x.mean()).sum()),
).reset_index()
# x = Series of that column's values for the current group only
```

### Useful Functions
```python
.idxmax()       # index label of max value
.idxmin()       # index label of min value
.nlargest(n)    # top n values
.nsmallest(n)   # bottom n values
.reset_index()  # always use after groupby to get normal DataFrame back
```

### ⚠️ Key Rules
- `groupby()` promotes the group column to the index — use `reset_index()` to get it back as a column.
- `agg()` collapses rows. `transform()` keeps the same shape.
- Use `transform()` when you need to add the group-level value back to individual rows.

---

## Pivot Tables & Merging

### `pivot_table()`
```python
pd.pivot_table(
    df,
    index   = "employee",          # rows
    columns = "month",             # column headers (category spread out)
    values  = "sales",             # cell values
    aggfunc = "sum",               # sum, mean, count, max — required
    margins = True,                # adds "All" totals row and column
    fill_value = 0,                # replace NaN cells with 0
)
```

### `melt()` — Wide to Long (reverse of pivot)
```python
df.melt(
    id_vars    = "employee",           # columns to keep as-is
    value_vars = ["Jan", "Feb", "Mar"],# columns to unpivot
    var_name   = "month",             # name for the new column-names column
    value_name = "sales"              # name for the values column
)
# pivot → melt → back to original (they are inverses)
# always reset_index() after pivot before melting
```

### `merge()` — SQL-style Joins
```python
pd.merge(left, right, on="key", how="inner")    # only matching rows
pd.merge(left, right, on="key", how="left")     # all left, NaN if no right match
pd.merge(left, right, on="key", how="right")    # all right, NaN if no left match
pd.merge(left, right, on="key", how="outer")    # all rows from both, NaN where no match

# different key names in each DataFrame
pd.merge(left, right, left_on="emp_id", right_on="employee_id")

# safety checks
pd.merge(..., validate="m:1")      # raises error if key not unique in right
pd.merge(..., indicator=True)      # adds _merge column: both/left_only/right_only
```

### `concat()` — Stacking DataFrames
```python
pd.concat([df1, df2])                           # vertical stack (more rows)
pd.concat([df1, df2], ignore_index=True)        # reset index after stacking
pd.concat([df1, df2], keys=["Q1", "Q2"])        # track source with MultiIndex
pd.concat([df1, df2], axis=1)                   # horizontal stack (more columns)
pd.concat([df1, df2], join="inner")             # keep only shared columns
```

### `merge()` vs `concat()`
| Situation | Use |
|-----------|-----|
| Combining rows of same structure | `concat()` |
| Adding columns via shared key | `merge()` |
| SQL-style JOIN | `merge()` |

### ⚠️ Key Rules
- `pivot_table()` requires `aggfunc` — it handles duplicate (index, column) combinations.
- After pivot, the index column is no longer a regular column — `reset_index()` before `melt()`.
- Always check row count after merge — unexpected drops or duplicates are common bugs.
- `concat()` does NOT match on keys — just appends. Always use `ignore_index=True` to avoid duplicate index.

---

## Time Series

### Parsing Dates
```python
pd.to_datetime(series)                          # parse string column to datetime64
pd.to_datetime(series, format="%d/%m/%Y")       # explicit format
pd.to_datetime(series, format="mixed")          # infer format per element
pd.date_range(start="2024-01-01", periods=365, freq="D")  # generate date sequence
```

### Setting Datetime as Index
```python
df = df.set_index("date")                       # unlocks time-based slicing and resample
df.loc["2024-03"]                               # all of March (use .loc, not df[])
df.loc["2024-01-01":"2024-01-31"]               # January only
```

### `.dt` Accessor
```python
df["date"].dt.month                             # 1–12
df["date"].dt.month_name()                      # January, February...
df["date"].dt.day                               # 1–31
df["date"].dt.day_name()                        # Monday, Tuesday...
df["date"].dt.quarter                           # 1–4
df["date"].dt.dayofweek                         # 0=Monday, 6=Sunday
df["date"].dt.dayofweek >= 5                    # True for weekends
df["date"].dt.isocalendar().week                # week number
```

### Resampling
```python
df["col"].resample("ME").sum()                  # monthly total (ME = month end label)
df["col"].resample("W").mean()                  # weekly average
df["col"].resample("QE").sum()                  # quarterly total
df["col"].resample("YE").sum()                  # yearly total
df["col"].resample("ME").agg(["sum", "mean"])   # multiple aggregations

# freq aliases: D=daily, W=weekly, ME=month end, MS=month start, QE=quarter end
```

### Rolling Windows
```python
df["col"].rolling(7).mean()                     # 7-day moving average
df["col"].rolling(30).mean()                    # 30-day moving average
df["col"].rolling(7).std()                      # rolling volatility
df["col"].rolling(7, min_periods=1).mean()      # no leading NaNs
# first n-1 rows are NaN — window not full yet
```

### Shifting
```python
df["col"].shift(1)                              # lag — yesterday's value on today's row
df["col"].shift(-1)                             # lead — tomorrow's value on today's row
df["col"].shift(7)                              # same day last week
df["col"] - df["col"].shift(1)                  # day-over-day change
df["col"].pct_change()                          # % change (shortcut for shift(1) division)
df["col"].diff(1)                               # shortcut for col - col.shift(1)
# pct_change() is row-over-row — what it means depends on what each row represents
```

### ⚠️ Key Rules
- Use `df.loc["2024-03"]` not `df["2024-03"]` for partial string indexing (pandas 2.0+).
- `resample()` requires datetime as the index.
- `pct_change()` has no concept of time — it's just row-over-row. Shape your data with `resample()` first.
- Rolling first `n-1` rows are NaN by default.

---

## Vectorization & Performance

### Vectorized Operations (always prefer these)
```python
df["new"] = df["a"] * df["b"]                   # math — vectorized
df["name"].str.upper()                          # string ops — vectorized via .str
```

### `np.where()` — Vectorized If/Else
```python
np.where(condition, value_if_true, value_if_false)

df["band"] = np.where(df["salary"] >= 80000, "High", "Low")
df["adj"]  = np.where(df["rating"] >= 4.0, df["salary"] * 1.1, df["salary"] * 1.02)
```

### `np.select()` — Multiple Conditions
```python
conditions = [
    df["salary"] >= 100000,
    df["salary"] >= 70000,
]
choices = ["Senior", "Mid"]

df["level"] = np.select(conditions, choices, default="Junior")
# conditions checked in order — first match wins
# default triggers if no condition matches
```

### `.apply()` — Use Sparingly
```python
# on a Series — receives one scalar at a time
df["col"].apply(lambda x: x * 2)               # BAD — use df["col"] * 2 instead

# on a DataFrame with axis=1 — receives one row (Series) at a time
df.apply(func, axis=1)                          # only use when logic needs multiple columns
df.apply(func, axis=1, result_type="expand")    # expand list result into separate columns
df["col"].apply(func, args=(extra_arg,))        # pass extra arguments
```

### `.map()` — Replace Values with Dict
```python
mapping = {"Eng": "Engineering", "HR": "Human Resources"}
df["dept_label"] = df["department"].map(mapping)    # NaN if key not in dict
```

### Binning
```python
# pd.cut — fixed value ranges (you define the edges)
pd.cut(df["salary"], bins=[0, 60000, 80000, 200000], labels=["Low", "Mid", "High"])

# pd.qcut — equal-sized groups (quantile-based)
pd.qcut(df["salary"], q=4, labels=["Q1", "Q2", "Q3", "Q4"])
pd.qcut(df["salary"], q=4, duplicates="drop")   # if bin edges overlap
```

### Profiling
```python
%%timeit          # measure entire cell — runs multiple times, reports mean ± std
%timeit expr      # measure a single expression
```

### When to Use What
| Task | Best approach |
|------|---------------|
| Math on a column | Vectorized arithmetic |
| Single if/else | `np.where()` |
| Multiple conditions | `np.select()` |
| Replace values with dict | `.map()` |
| Complex multi-column logic | `.apply(axis=1)` |
| Bin by value range | `pd.cut()` |
| Bin by equal groups | `pd.qcut()` |
| Never | Python `for` loop over rows |

### ⚠️ Key Rules
- Vectorized ops run in C under the hood — 10x–100x faster than Python loops.
- `np.where` is ~66x faster than `.apply` for if/else logic.
- Use `.apply()` only when no vectorized alternative exists.
- `pd.cut()` — unequal group sizes, you define edges. `pd.qcut()` — equal group sizes, pandas defines edges.
