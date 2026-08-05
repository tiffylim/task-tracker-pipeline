# task-tracker-pipeline
A reusable Python pipeline that validates, cleans, and deduplicates messy task tracker exports, with error handling for missing files and columns.

## Before and after

**Before** (three rows from `messy_tasks.csv`):

```text
task_id,task_name,assignee,status,priority,due_date,created_date
3,Write API docs,alice,TODO,Low,2024-03-25,2024-03-03
5,Fix login bug,Charlie,DONE,High,March 18 2024,2024-03-04
7,Write API docs, alice,todo,low,2024-03-25,2024-03-03
```

**After** (the same rows in `cleaned_tasks.csv`):

```text
task_id,task_name,assignee,status,priority,due_date,created_date
3,Write API docs,Alice,to do,low,2024-03-25,2024-03-03
5,Fix login bug,Charlie,done,high,2024-03-18,2024-03-04
```

Task 7 is gone: once cleaned, it duplicates task 3 in every column except
`task_id`. Because `task_id` is unique per row, the default
`drop_duplicates()` finds nothing — the comparison has to explicitly
exclude it.

| Column | Before | After |
|-----------|----------|--------|
| status | DONE | done |
| priority | High | high |
| due_date | March 18 2024 | 2024-03-18 |
| assignee | " alice" | Alice |
| status | TODO | to do |

Note: spreadsheet apps strip leading/trailing whitespace when importing
CSVs, so the space in `" alice"` is only visible in a text editor or via
`repr()` in Python.

## What it does

- **priority** — lowercase all values
- **status** — lowercase all values, then map `todo` to `to do`
- **assignee** — fill missing values with `Unassigned`, strip surrounding
  whitespace, and capitalize each word
- **due_date** — parse mixed date formats into one consistent format;
  unparseable dates become blank
- **duplicates** — remove rows that match on every column except `task_id`

## Files

- `clean_tasks.py` — the cleaning script
- `messy_tasks.csv` — sample input (20 rows)
- `cleaned_tasks.csv` — the output it produces (14 rows)

Requires pandas 2.0 or later. Tested with Python 3.12.13 and pandas 2.2.2.

## How to run it

Run the script as-is to clean the included sample file:

```bash
python clean_tasks.py
```

```text
Cleaned 20 rows to 14 rows. Saved to cleaned_tasks.csv.
```

To clean your own export, import the function and pass your filenames.
The first argument is the file to read, the second is the file to write:

```python
from clean_tasks import clean_tasks

clean_tasks("my_export.csv", "my_export_cleaned.csv")
```

## Error handling

The script exits cleanly instead of crashing in two cases. Both print a
message and return `None`:

**Missing file** — the input path doesn't exist:

```text
Missing file - wrong_file.csv
```

**Missing columns** — the CSV loaded, but doesn't have every column the
pipeline needs. All missing columns are reported at once, before any
cleaning runs:

```text
CSV is missing required columns: ['priority', 'due_date']
```

Because both paths return `None`, check the result before using it:

```python
result = clean_tasks("my_export.csv", "my_export_cleaned.csv")
if result is not None:
  print(result.shape)
```

## Why I built this

I spent eight years in fintech and banking operations, where cleaning up exports 
like this was a recurring, manual task. Measuring workload becomes unreliable 
when there are inconsistencies — the same status spelled four different ways 
and one person becomes three different assignees.

`messy_tasks.csv` is modeled on that experience: missing assignees, inconsistent 
casing and wording, extra whitespace, varying date formats, and duplicated rows 
with different IDs. The script turns a file like that into something that can 
actually be analyzed.
