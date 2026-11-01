# Quality assurance checklist

- [x] Downloaded the genuine UCI Online Retail workbook from the UCI repository; attribution and CC BY 4.0 noted.
- [x] Source dimensions verified as 541,909 × 8; source dtypes, missing counts and duplicate count recorded.
- [x] Reproducible analysis executed; exact duplicates removed, missing customer identifiers retained, missing descriptions explicitly labeled.
- [x] Clean audit ledger, daily features, RFM table, Excel workbook, results JSON and IQR audit produced.
- [x] KPI definitions exclude cancellations/nonpositive quantities/prices; all outputs computed from actual source workbook.
- [x] 16 charts generated; monthly trend, forecast comparison, correlations, dashboard preview visually reviewed; dashboard axes/labels adjusted.
- [x] Notebook executed end-to-end with zero stored cell errors; includes Python, NumPy, Pandas, cleaning, EDA, SQL, BI, ML, and tool comparison.
- [x] MySQL 8 schema/query/normalization scripts parse with SQLGlot's MySQL dialect (13, 27, and 6 statements); no live MySQL server/Workbench available for database execution.
- [x] Forecast uses chronological split and lagged features; compared with weekly-naive baseline. Model does not outperform the baseline; disclosed in report.
- [x] Word report OOXML package opens; 10 data-backed insights included; business results reconcile to JSON.
- [x] CSV/Excel/ZIP file integrity checked; no unreported credential in project files.
- [x] Power BI DAX and build guide plus static preview included.
- [ ] Native Power BI `.pbix` is not included: Power BI Desktop/service is unavailable in this environment. Static PNG is explicitly not represented as an interactive dashboard.
- [ ] Remote GitHub repository/asset links verified only after push; record the actual URLs below.

## Deliverables and current remote status
Repo: Pending verified upload.
Report: `reports/Data_Science_Tool_Mastery_Report.docx`
Executed notebook: `notebooks/Data_Science_Tool_Mastery.ipynb`
Dataset package: `datasets/retail_analytics_data.zip`
Visualization package: `visualizations/visualizations.zip`

A missing PBIX is a platform-capability limitation, not a fabricated deliverable. SQL is statically parsed but should also be executed in MySQL Workbench locally.