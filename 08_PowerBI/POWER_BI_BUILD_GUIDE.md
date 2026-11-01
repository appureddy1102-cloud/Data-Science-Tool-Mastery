# Power BI dashboard specification

A static KPI preview is `visualizations/12_kpi_dashboard.png`. The `.pbix` binary cannot be authored or verified in this Linux execution environment because Power BI Desktop/Power BI service is unavailable; this guide and working DAX are supplied instead. Do not treat the PNG as an interactive PBIX.

## Import/model
1. Power BI Desktop → Get Data → Text/CSV → `datasets/processed/online_retail_clean.csv`.
2. Set `InvoiceDate` to Date/Time, `CustomerID` whole number (nullable), `Quantity` whole number, `UnitPrice` and `LineRevenue` decimal/currency, and `IsCancellation` Boolean.
3. Create a Calendar table in DAX with `CALENDAR(MIN(Retail[InvoiceDate]), MAX(Retail[InvoiceDate]))`; relate Calendar[Date] one-to-many to `DATE(Retail[InvoiceDate])` (create date-only field in Power Query). Mark as date table.
4. Use one fact table for transaction-line measures. Do not infer cost, margin, or profit: no COGS is present.

## Pages and interactions
- **Overview:** cards for Gross Sales GBP, Order Count, Units Sold, Identified Customers; monthly line chart, top-country bars; date/country slicers.
- **Product & Geography:** top-product/country rankings; drill through to product and country tables; country slicer.
- **Customer behavior:** RFM scatter/table for identified customers, repeat-order share; note unidentified CustomerID rows are excluded from customer-level measures.
- **Reconciliation:** cancellation invoice/line count, negative quantity/return lines, unidentified customer share, signed line revenue. Reconcile separately from positive gross-sales KPI.

DAX measures are in `DAX_measures.dax`. For operational refresh, replace this static historical sample with a governed current source, define currency/returns policy, and test measure results against SQL totals.
