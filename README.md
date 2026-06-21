# Superstore Sales Analysis — Week 1

This project uses the Sample Superstore dataset to clean the data and create summary outputs for a sales analysis report.

## What is included

- `SampleSuperstore.csv` — source dataset
- `eda.py` — Python script for cleaning and summarizing the data
- `README.md` — project overview and instructions

## What the script does

`eda.py` loads the dataset, converts dates, fixes numeric fields, removes duplicates, and adds simple summary calculations.

It also saves cleaned data and CSV summary files into an `outputs/` folder so the results are ready for use in charts or reports.

## Run the script

From the project folder, install `pandas` if needed and run:

```powershell
pip install pandas
python eda.py
```

If you want to use a separate virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
pip install pandas
python eda.py
```

## Output files

The script writes these files to `outputs/`:

- `cleaned_superstore.csv`
- `sales_by_category.csv`
- `profit_by_region.csv`
- `top_states_by_sales.csv`
- `monthly_sales_trend.csv`

## Why this is useful

These outputs make it easier to build charts, dashboards, or reports without reprocessing the raw dataset.

## Notes

Keep `SampleSuperstore.csv` in the project folder and run `eda.py` from the same location. The script is designed for a simple Week 1 analytics submission.
