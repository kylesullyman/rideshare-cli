Me: Please write in db_operations a function to load the sample data if it hasn't been already, and write a bulk_insert function to handle writing multiple rows at once

LLM:
Sure. I'll add two pieces to `db_operations`:

1. **`bulk_insert(query, data)`**: a general helper that runs one parameterized query against a list of tuples using `executemany`, then commits once.
2. **`populate_tables(rider_path, driver_path, ride_path)`**: checks each table and, only if it's empty, loads the matching CSV through `data_cleaner` and `bulk_insert`.

You already have `single_record_params`, so `is_table_empty` can reuse it.

### `bulk_insert`

```python
def bulk_insert(self, query, data):
    self.cursor.executemany(query, data)
    self.connection.commit()
```

`executemany` sends every row through the same prepared statement, so it's faster than looping over `execute`, and it still uses placeholders, so values are never pasted into the SQL string. Committing once at the end means a table loads all at once or not at all, instead of ending up half-loaded.

### Checking for an empty table

```python
# table_name only ever comes from our own code (never user input),
# since table names can't be passed as placeholders
def is_table_empty(self, table_name):
    query = f"SELECT COUNT(*) FROM {table_name};"
    return self.single_record_params(query, {}) == 0
```

A table name can't be a `%s` placeholder in MySQL, so an f-string is the only option here. That's safe as long as `table_name` is always a hardcoded string from your code, which it is in `populate_tables`.

### `populate_tables`

```python
# fill empty tables
def populate_tables(self, rider_path, driver_path, ride_path):
    if self.is_table_empty("Rider"):
        query = """
        INSERT INTO Rider (rider_id, username, first_name, last_name)
        VALUES (%s, %s, %s, %s);
        """
        self.bulk_insert(query, data_cleaner(rider_path))
        print("Rider sample data loaded")

    if self.is_table_empty("Driver"):
        query = """
        INSERT INTO Driver (driver_id, username, first_name, last_name,
                            driver_mode)
        VALUES (%s, %s, %s, %s, %s);
        """
        self.bulk_insert(query, data_cleaner(driver_path))
        print("Driver sample data loaded")

    if self.is_table_empty("Ride"):
        query = """
        INSERT INTO Ride (ride_id, rider_id, driver_id, pickup_location,
                          dropoff_location, ride_datetime, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        self.bulk_insert(query, data_cleaner(ride_path))
        print("Ride sample data loaded")
```

You'll also need the import at the top of the file:

```python
from helper import data_cleaner
```

A few things to know:

- **Order matters.** Rider and Driver have to load before Ride. Otherwise the foreign keys `rider_id` and `driver_id` point at rows that don't exist yet and MySQL throws an `IntegrityError`.
- **Positional `%s` placeholders.** `data_cleaner` returns tuples, not dicts, so the placeholders are positional. The column order in each `INSERT` has to match the column order in the CSV.
- **Explicit IDs.** The CSVs include the primary key values, so I list `rider_id` / `driver_id` / `ride_id` in the column lists. `AUTO_INCREMENT` still works afterward. MySQL moves the counter past the largest inserted ID, so new accounts made in the app won't collide with the sample data.
- **Empty ratings.** Ride 9 in `rides.csv` has no rating. `convert` turns `''` into `None`, which becomes SQL `NULL`. Your schema allows that (`rating TINYINT NULL`), and the `CHECK` constraint doesn't reject `NULL`.
- **Datetimes.** `ride_datetime` stays a string like `'2026-10-01 08:15:00'` after `convert`, and MySQL parses that format into a `DATETIME` on its own.
- **`driver_mode`.** The `1`/`0` values become Python ints, which MySQL stores in a `BOOLEAN` (`TINYINT(1)`) column without any extra work.

Then in `app.py`, call it right after the tables are created:

```python
def startScreen():
    create_tables(db_ops)
    db_ops.populate_tables("riders.csv", "drivers.csv", "rides.csv")
```

On the first run, all three tables get loaded. On later runs, each `is_table_empty` check returns `False` and nothing gets inserted again.

## User

What happens if I call `reset_tables` and then run it again?

## Claude

`reset_tables` drops all three tables and recreates them empty. On the next `populate_tables` call, every `is_table_empty` check returns `True`, so all three CSVs load again in the right order, starting from the same clean sample data. Note that `reset_tables` drops `Ride` first for the same foreign key reason: you can't drop `Rider` or `Driver` while `Ride` still references them.
