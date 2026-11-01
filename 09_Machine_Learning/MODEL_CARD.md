# Daily gross revenue forecasting exercise — model card

- **Task:** regression of daily positive gross sales in GBP.
- **Data:** UCI Online Retail, calendar dates with missing dates filled as zero sales; historical 2010–2011.
- **Outcome:** day gross line revenue (Quantity × UnitPrice), non-cancellation, positive quantity/price only.
- **Features:** weekday, month, day-of-month; lags 1/7/14/28 days; shifted rolling means over 7/28 days. Feature windows use prior days only.
- **Split:** first 80% of feature-complete dates for training, final 20% chronological holdout (70 test days); no shuffling.
- **Model:** scikit-learn HistGradientBoostingRegressor, fixed random_state 42.
- **Evaluation:** MAE £16,429.54; RMSE £26,809.95; R² 0.2778. Weekly-naive baseline MAE £14,165.99; RMSE £24,334.25.
- **Conclusion:** model underperforms baseline. Not recommended for forecasting deployment.
- **Limitations:** short history, strong calendar/holiday effects, no stock availability, promotions, prices, costs or current data. A single holdout is noisy; further backtesting and seasonal benchmarks are warranted.
- **Intended use:** educational demonstration only; not a financial planning system.
