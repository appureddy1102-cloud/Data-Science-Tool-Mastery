# Data Science Tool Mastery — Retail Analytics Portfolio

An end-to-end, reproducible portfolio demonstrating Python, NumPy, Pandas, SQL/MySQL, EDA, statistics, visualization, Power BI design, Excel, and beginner ML on a **real UCI dataset**.

## Data provenance, context, and license
**UCI Online Retail**: https://archive.ics.uci.edu/dataset/352/online+retail (DOI [10.24432/C5BW33](https://doi.org/10.24432/C5BW33)), CC BY 4.0. UCI describes transaction lines for a UK-based non-store online retailer, covering 2010-12-01 to 2011-12-09. Original file: 541,909 rows × 8 columns: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`. The downloaded source workbook is in `datasets/raw/`. Attribution is required when reusing the data.

**Business questions:** What are historical sales patterns by month, geography, and product? What share of customers repeat? How should cancellation/returns and missing IDs be represented? Can a basic time-series model beat a weekly-naive baseline?

## Key measured results
All values are calculated by `src/run_analysis.py`; analytical cohort means non-cancellation transactions with positive quantity and unit price. Gross sales = `Quantity × UnitPrice` in GBP; this is **not** net sales, profit, or margin.

- Raw 541,909 × 8; 5,268 exact duplicate rows removed; cleaned audit ledger 536,641 rows.
- 135,037 CustomerID values remain null by design; no identities were imputed. 1,454 missing descriptions use `UNKNOWN PRODUCT`.
- Positive sales subset: 524,878 line records, 19,960 invoices, 4,338 identified customers, 38 countries; £10,642,110.80 gross line sales.
- UK is 84.59% of positive sales; top five countries comprise 94.05%.
- Among identified customers, 65.58% have more than one invoice; this excludes unknown customer IDs.
- Forecast exercise uses chronological holdout (70 days, train through 2011-09-30, test starts 2011-10-01). HistGradientBoosting MAE £16,429.54 vs weekly-naive MAE £14,165.99; model is worse than baseline and is **not recommended for deployment**.

More than ten computed interpretations and recommendations are in `reports/BUSINESS_INSIGHTS.md`. All observations are descriptive and historical, not causal or representative of current commerce.

## Modules and deliverables
- `01_Python_Fundamentals/`, `02_NumPy/`, `03_Pandas/`: exercises; the executed notebook includes hands-on examples.
- `04_SQL/`: MySQL 8 schema and 26 analytical examples (CTEs, joins, subqueries, window functions, CASE and views). Static MySQL-dialect parsing passed. No MySQL server/Workbench is installed here; runtime execution is a local follow-up.
- `05_Data_Cleaning/`: data-quality decisions and audit notes.
- `06_EDA/`, `07_Data_Visualization/`: 16 180-DPI visualizations and interpretation.
- `08_PowerBI/`: model/page build guide, DAX measures, static KPI preview. **Power BI Desktop is unavailable in this environment, so no native `.pbix` is included or claimed.**
- `09_Machine_Learning/`: ML details and holdout results.
- `10_Tool_Comparison/`: practical tool selection notes.
- `notebooks/Data_Science_Tool_Mastery.ipynb`: executed notebook across ten modules.
- `reports/Data_Science_Tool_Mastery_Report.docx`: formatted Word report; `reports/BUSINESS_INSIGHTS.md`: 10 evidence-based insights.
- `datasets/processed/online_retail_clean.csv`, `daily_revenue_features.csv`, `customer_rfm.csv`, and Excel workbook.
- `visualizations/`: charts, including KPI dashboard mockup.

## Reproduce
Python 3.10+:
```bash
python -m pip install -r requirements.txt
python src/run_analysis.py
python src/build_notebook.py
jupyter nbconvert --to notebook --execute --inplace notebooks/Data_Science_Tool_Mastery.ipynb
python src/build_report.py
```
The original UCI workbook is included, so running the analysis does not require a download. Main fixed random states are 42 where sampling/model randomness is used. The time split is chronological, not shuffled.

### MySQL Workbench
1. Start MySQL 8 and run `04_SQL/01_schema_mysql.sql`.
2. Workbench **Table Data Import Wizard** → `datasets/processed/online_retail_clean.csv` → import into `retail_analytics.retail_transactions`; map `IsCancellation` to Boolean/TINYINT and allow nullable CustomerID.
3. Optionally populate the normalized star schema via `04_SQL/03_normalize_mysql.sql` (dimensions first, then fact, with PK/FK constraints).
4. Run query examples from `04_SQL/02_analytical_queries_mysql.sql`. The schema and query scripts passed MySQL-dialect static parsing, but were not executed against a live MySQL instance in this environment.

### Power BI
Follow `08_PowerBI/POWER_BI_BUILD_GUIDE.md`, load the processed CSV, create the Calendar relationship, and add `DAX_measures.dax`. The supplied image is only a static preview, not an interactive PBIX.

## Responsible use and limitations
The data contains historical transaction records, not current operational data. Missing customer IDs are material and may be non-random; customer analyses are limited to identified records. No product costs or margins exist. Cancellations and returns are retained for audit but excluded from positive gross-sales measures. Top products/geographies are observational; recommendations should be validated with current, governed data. The forecasting model underperforms the baseline. No causal claims are made.
