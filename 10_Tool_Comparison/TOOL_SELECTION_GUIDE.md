# Practical tool selection guide

| Compare | Prefer first tool when... | Use this portfolio example |
|---|---|---|
| Python vs Excel | Python when repeatable, multi-step processing or tests are needed; Excel for quick ad hoc review, manual inspection, or handoff | Python generates reproducible analyses; Excel KPI workbook is a review surface |
| Pandas vs NumPy | Pandas for labeled tables, joins, groups and dates; NumPy for vectorized arrays and numerical kernels | Group sales by country (Pandas); NaN-aware array calculations (NumPy) |
| SQL vs Python | SQL for set-based selection/aggregation close to a relational database; Python for orchestration, statistics and ML | MySQL query suite vs scikit-learn model |
| Power BI vs Matplotlib | Power BI for interactive filters, drill-down and shared dashboards; Matplotlib/Seaborn for reproducible static charts | Dashboard spec and DAX plus static chart outputs |
| Jupyter vs Colab | Jupyter for local files and controlled environments; Colab for frictionless cloud notebooks and collaboration (after data policy review) | Executed local notebook |
| Scikit-learn vs manual statistics | scikit-learn for standardized predictive pipelines/metrics; SciPy/manual formulas when explicit inferential statistic assumptions matter | Forecast holdout model vs SciPy summaries/correlations |

Do not choose a tool because it is fashionable: consider refresh, scale, governance, reproducibility, users, and deployment environment.