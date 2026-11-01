# Evidence-based business insights

Source dataset: UCI Online Retail; all metrics are recalculated from the downloaded original workbook. Sales KPIs mean non-cancellation rows with positive Quantity and UnitPrice, `Quantity × UnitPrice` in GBP. These are gross line sales, not net sales or profit.

## 1. Revenue scale
**Observation:** Positive, non-cancelled transaction lines total £10,642,110.80 across 524,878 lines and 19,960 invoices.
**Business interpretation:** The historical transaction sample provides sufficient scope for group-level retail reporting.
**Recommendation:** Use consistent gross-sales definition; do not call it profit.
**Limitations:** Historical observational data (2010–2011); results are descriptive, not causal, and may not represent current retail conditions.

## 2. Geographic concentration
**Observation:** United Kingdom accounts for 84.59% of sales; top five countries account for 94.05%.
**Business interpretation:** Revenue in this sample is heavily concentrated in UK customers.
**Recommendation:** Track geographic concentration and test market expansion with current data.
**Limitations:** Historical observational data (2010–2011); results are descriptive, not causal, and may not represent current retail conditions.

## 3. Monthly peak
**Observation:** The highest gross-sales month is 2011-11 (£1,503,866.78); lowest is 2011-02 (£522,545.56).
**Business interpretation:** Demand varies across observed months; the data span only about a year.
**Recommendation:** Use seasonal-aware planning and validate across multiple years before extrapolating.
**Limitations:** Historical observational data (2010–2011); results are descriptive, not causal, and may not represent current retail conditions.

## 4. Repeat customer mix
**Observation:** Among 4,338 identified customers, 65.58% placed more than one distinct invoice.
**Business interpretation:** Repeat purchasing is common in the identified-customer subset.
**Recommendation:** Monitor repeat purchase cohorts; missing identities mean the share is not all shoppers.
**Limitations:** Historical observational data (2010–2011); results are descriptive, not causal, and may not represent current retail conditions.

## 5. Order basket value
**Observation:** Mean gross order value is £533.12 across 19,960 invoices.
**Business interpretation:** Order-level averages can inform descriptive basket monitoring, but are skewed by bulk purchasing.
**Recommendation:** Use median and distribution bands alongside mean; avoid margin/profit claims.
**Limitations:** Historical observational data (2010–2011); results are descriptive, not causal, and may not represent current retail conditions.

## 6. Customer identity missingness
**Observation:** 135,037 cleaned rows have no CustomerID; those sales account for 16.49% of positive sales revenue.
**Business interpretation:** Transaction-level sales is usable, but customer-level segmentation excludes unidentified records.
**Recommendation:** Report customer coverage and do not impute identities.
**Limitations:** Historical observational data (2010–2011); results are descriptive, not causal, and may not represent current retail conditions.

## 7. Top product
**Observation:** DOTCOM POSTAGE is the top gross-revenue product (£206,248.77); top 10 products provide 10.84% of sales.
**Business interpretation:** Revenue spans many products; the top-ten share gives concentration context.
**Recommendation:** Review availability and assortment using inventory/cost data before action.
**Limitations:** Historical observational data (2010–2011); results are descriptive, not causal, and may not represent current retail conditions.

## 8. Cancellation/return audit
**Observation:** The cleaned ledger retains 9,251 cancellation rows and negative-quantity return/adjustment lines; sales KPIs exclude cancellations and nonpositive quantity/price.
**Business interpretation:** Signed adjustments are distinct from gross positive sales and should be visible in reconciliation.
**Recommendation:** Build separate gross sales, returns, and net sales measures; this project reports gross sales only.
**Limitations:** Historical observational data (2010–2011); results are descriptive, not causal, and may not represent current retail conditions.

## 9. Forecast baseline comparison
**Observation:** Chronological 70-day holdout: model MAE £16,429.54, versus weekly-naive MAE £14,165.99; model RMSE £26,809.95 versus baseline £24,334.25.
**Business interpretation:** The tested model does not beat the simple weekly-naive baseline.
**Recommendation:** Do not deploy; investigate features, holiday effects and data stability with robust validation.
**Limitations:** Historical observational data (2010–2011); results are descriptive, not causal, and may not represent current retail conditions.

## 10. Data cleaning
**Observation:** Exact duplicate rows removed: 5,268; cleaned table retains 536,641 rows. Missing customer ID is retained rather than invented.
**Business interpretation:** The retained clean ledger supports transaction analysis without fabricating customer attributes.
**Recommendation:** Keep a reproducible cleaning log and publish a data dictionary.
**Limitations:** Historical observational data (2010–2011); results are descriptive, not causal, and may not represent current retail conditions.