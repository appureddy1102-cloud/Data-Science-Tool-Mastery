# Data quality and preprocessing report

## Source and scope
The original UCI workbook `Online Retail.xlsx` has 541,909 rows and 8 columns, covering 1 Dec 2010–9 Dec 2011. Raw workbook and original archive are kept under `datasets/raw/`; source attribution/licence are in README.

## Audited actions (computed from original workbook)
- Exact full-row duplicates: 5,268 removed (clean audit table: 536,641 rows). Duplicate rows were identified by equality across all source fields; no key-based deduplication assumption was made.
- `InvoiceNo`, `StockCode`, `Description`, and `Country` standardized as trimmed strings; text labels uppercased for descriptions/codes and title-cased country names.
- `InvoiceDate` parsed to timestamp; quantity/price numeric; CustomerID nullable integer representation.
- 1,454 missing descriptions replaced by `UNKNOWN PRODUCT` so line-level sales and other dimensions remain usable; no product identity is fabricated.
- 135,037 missing CustomerID values remain missing (not imputed): identity is not recoverable. Customer-level analysis excludes these observations; transaction and geography analysis retains them.
- 9,251 cancellation rows remain in the clean audit ledger (`InvoiceNo` begins C). Negative/zero quantities and nonpositive prices remain for audit and signed reconciliation.
- KPI and forecasting sales subset: exclude cancellation invoices, nonpositive quantity or nonpositive unit price. Define gross line sales as Quantity × UnitPrice, GBP; this is not net sales or profit.
- No automatic IQR deletion: unusual orders/line amounts may reflect genuine bulk transactions. Chart displays may cap at 95th/99th percentiles purely for readability; calculations use uncapped data.
- Daily series fills absent calendar dates with zero sales to align time-series lags. Test split is chronological (no shuffle), and lag/rolling features use prior days only.

See `datasets/processed/data_profile.json` for source/clean shape, types, missingness and duplicate counts. Run `python src/run_analysis.py` to regenerate outputs.
