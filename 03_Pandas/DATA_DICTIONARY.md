# UCI Online Retail dataset dictionary

| Field | Type after import | Meaning | Quality/analysis notes |
|---|---|---|---|
| InvoiceNo | String | Invoice identifier; values beginning with C indicate cancellation | Treat as categorical ID; cancellations kept for audit |
| StockCode | String | Product/item identifier | Keep leading zeros/letters; not a numeric measure |
| Description | String | Product name | 1,454 raw missing descriptions filled with `UNKNOWN PRODUCT`; standardized uppercase |
| Quantity | Integer | Units on the line | Negative values indicate returns/adjustments; retain in audit data |
| InvoiceDate | Date/time | Transaction timestamp | Parsed to datetime; source dates span 2010-12-01–2011-12-09 |
| UnitPrice | Decimal GBP | Price per unit | Nonpositive values excluded from gross-sales KPI; retained in audit table |
| CustomerID | Nullable integer | Customer identifier | Raw missing IDs retained; never imputed |
| Country | String | Customer country | Whitespace trimmed and case standardized |
| IsCancellation | Boolean (engineered) | InvoiceNo starts with C | Cancellation row flag |
| LineRevenue | Decimal GBP (engineered) | Quantity × UnitPrice with signed quantity | Includes returns/cancellation line sign in audit ledger |
| Date | Date (engineered) | Calendar date extracted from InvoiceDate | Daily grouping |

Gross-sales analytical cohort = non-cancellation rows with Quantity > 0 and UnitPrice > 0; revenue is line quantity × unit price. The cost/margin/profit variables are absent. Source has one invoice item per record, not one row per invoice/customer. Refer to UCI repository for source details and CC BY 4.0 attribution.