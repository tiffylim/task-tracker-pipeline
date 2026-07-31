import pandas as pd


def clean_tasks(input_path, output_path):
  """
  Clean messy task tracker data and export it to a new CSV file.

  Input CSV must contain the columns: task_name, assignee, status,
  priority, due_date, created_date.

  Standardize the status and priority columns to lowercase, mapping
  "todo" to "to do".
  Fill missing values in assignee with "Unassigned",
  strip surrounding whitespace, and capitalize each word.
  Parse mixed date formats in due_date into a single datetime type,
  marking any unparseable value as NaT.
  Remove duplicate rows, comparing every column except task_id.

  Exit early without cleaning if the input file is not found, or if the
  CSV is missing any required column.

  Parameters:
    input_path (str): path to read the messy CSV file
    output_path (str): path to write the cleaned CSV file

  Returns:
    DataFrame: the cleaned and deduplicated data,
    or None if the file was missing or a required column was absent.
  """

  try:
    df = pd.read_csv(input_path)
  except FileNotFoundError:
    print(f"Missing file - {input_path}")
    return

  required = ["task_name", "assignee", "status",
              "priority", "due_date", "created_date"]
  missing = [col for col in required if col not in df.columns]
  if missing:
    print(f"CSV is missing required columns: {missing}")
    return

  df["priority"] = df["priority"].str.lower()
  status_map = {"todo": "to do"}
  df["status"] = df["status"].str.lower().replace(status_map)
  df["assignee"] = (df["assignee"].fillna("Unassigned")
                    .str.strip().str.title())
  df["due_date"] = pd.to_datetime(df["due_date"], format="mixed",
                                  errors="coerce")

  # task_id is excluded: it is unique per row, so including it would
  # make every row look distinct and no duplicates would be found.
  df_deduped = df.drop_duplicates(subset=["task_name", "assignee",
                                          "priority", "status",
                                          "due_date", "created_date"])

  # index=False keeps pandas' automatic row numbers out of the file.
  df_deduped.to_csv(output_path, index=False)
  print(f"Cleaned {len(df)} rows to {len(df_deduped)} rows. "
        f"Saved to {output_path}.")
  return df_deduped


if __name__ == "__main__":
  clean_tasks("messy_tasks.csv", "cleaned_tasks.csv")
