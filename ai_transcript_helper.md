Me: Please write in helper.py a function that reads one of the sample data csv's and returns the rows so they can go straight into bulk_insert, plus a convert function that turns each value into the right type

LLM:
Sure. I'll add two functions to `helper.py`:

1. **`convert(value)`**: takes one raw CSV cell (always a string) and returns an `int`, `float`, `None`, or the original string.
2. **`data_cleaner(path)`**: reads a CSV file, runs every cell through `convert`, and returns a list of tuples, which is the shape `cursor.executemany` expects.

### `convert`

```python
def convert(value):
    value = value.strip()
    if value == '':
        return None
    if len(value) > 1 and value[0] == '0' and value[1] != '.':
        return value
    try:
        return int(value)
    except ValueError:
        pass
    try:
        result = float(value)
        if result != result or result in (float('inf'), float('-inf')):
            return value
        return result
    except ValueError:
        return value
```

It goes through the checks in this order:

- **Strip whitespace.** A cell like `" 5"` after a comma should still become `5`.
- **Empty becomes `None`.** An empty cell, like the missing rating on ride 9 in `rides.csv`, becomes `None`, which `mysql.connector` sends as SQL `NULL`.
- **Leading zeros stay strings.** A value like `"02134"` (a zip code) or `"007"` would lose its zeros if it went through `int()`, so anything that starts with `0` and is longer than one character stays a string. `"0"` by itself still becomes the int `0`, which `driver_mode` needs, and `"0.5"` still becomes a float because of the `value[1] != '.'` check.
- **`int` before `float`.** `int("5")` works but `int("4.5")` raises `ValueError`, so trying `int` first keeps whole numbers like IDs and ratings as ints instead of turning them into `5.0`.
- **No NaN or infinity.** `float()` accepts strings like `"nan"`, `"inf"`, and `"Infinity"`, so a location or name with one of those words would turn into a special float. `result != result` is only true for NaN, and the `in` check catches both infinities. In those cases the original string is kept.
- **Fall back to the string.** Anything else, like `"jsmith"` or `"2026-10-01 08:15:00"`, stays a string. MySQL parses the datetime string into a `DATETIME` on insert.

### `data_cleaner`

```python
import csv


def data_cleaner(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        data_cleaned = []
        for row in reader:
            # skip blank lines
            if not any(cell.strip() for cell in row):
                continue
            data_cleaned.append(tuple(convert(cell) for cell in row))
    return data_cleaned
```

A few things to know:

- **`csv.reader` instead of `split(",")`.** Splitting on commas breaks as soon as a value contains one, like `"Orange, CA"` in quotes. `csv.reader` handles quoted fields correctly.
- **`newline=""`.** The `csv` docs recommend opening the file this way so the reader handles line endings itself. Otherwise a file saved on Windows (`\r\n`) can produce bad rows.
- **Blank lines are skipped.** A trailing empty line at the end of a CSV would otherwise become a row of `None`s and fail on the `NOT NULL` columns.
- **Rows are tuples.** `executemany` with positional `%s` placeholders takes a sequence of tuples, so the result can go straight into `bulk_insert`:

```python
self.bulk_insert(query, data_cleaner(rider_path))
```

Since the rows come back in file order, the column order in each CSV has to match the column order in the matching `INSERT` statement.
