# task-tracker-pipeline
A reusable Python pipeline that validates, cleans, and deduplicates messy task tracker exports, with error handling for missing files and columns.

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
