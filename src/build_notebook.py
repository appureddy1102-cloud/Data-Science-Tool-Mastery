from pathlib import Path
import nbformat as nbf
R=Path(__file__).resolve().parents[1]
nb=nbf.v4.new_notebook(); c=[]
def md(s): c.append(nbf.v4.new_markdown_cell(s))
def code(s): c.append(nbf.v4.new_code_cell(s))
md('# Data Science Tool Mastery: Retail Analytics Portfolio\n\n**Dataset:** UCI Online Retail, real historical transactions, CC BY 4.0. Analysis is observational; business descriptions are not causal claims. Source: https://archive.ics.uci.edu/dataset/352/online+retail')
md('## Dataset and business case\nThis data records transaction line items for a UK non-store retailer, 1 Dec 2010–9 Dec 2011. Source metadata lists 541,909 instances and eight columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country. Questions: sales concentration, customer repeat behavior, product mix, and whether a basic time-series regression beats a simple weekly-naive baseline.')
code('from pathlib import Path\nimport json, runpy\nimport numpy as np, pandas as pd\nimport matplotlib.pyplot as plt, seaborn as sns\nfrom scipy import stats\nfrom sklearn.model_selection import TimeSeriesSplit\nROOT=Path.cwd()\nif not (ROOT/"datasets").exists(): ROOT=ROOT.parent\nprint("Root:",ROOT)')
md('## 1. Python Fundamentals\nDemonstrate typed variables, conditionals, loops, functions, collection types, exceptions, and file handling.')
code('''# Variables and data types
project="Retail analytics"; revenue=125.50; is_valid=True
print(type(project).__name__, type(revenue).__name__, type(is_valid).__name__)
# if, loop, function
status="high" if revenue>=100 else "low"
for x in [1,2,3]: print(x, end=" ")
def safe_average(values):
    try: return sum(values)/len(values)
    except ZeroDivisionError: return None
print("\\nstatus",status,"avg",safe_average([1,2,3]),"empty",safe_average([]))
# list, tuple, dict, set
items=["tea","gift"]; point=(1,2); kpi={"revenue":revenue}; unique=set(items+items)
print(items,point,kpi,unique)
# exception and file IO
try: int("not-a-number")
except ValueError as exc: print("Handled:",type(exc).__name__)
tmp=ROOT/"module1_example.txt"; tmp.write_text("portfolio file I/O demo")
print(tmp.read_text()); tmp.unlink()''')
md('## 2. NumPy\nArray creation, indexing, vectorization, aggregation, missing-value handling and matrix multiplication.')
code('''a=np.array([[1.,2.,np.nan],[4.,5.,6.]])
print("shape",a.shape,"slice",a[:,1:])
print("mean by col ignoring NaN",np.nanmean(a,axis=0))
filled=np.where(np.isnan(a),np.nanmean(a,axis=0),a)
print("vector x 2",filled*2,"sum",np.sum(filled))
print("matrix product",np.array([[1,2],[3,4]])@np.array([[2],[1]]).ravel())''')
md('## 3. Pandas\nRead the cleaned transaction-line CSV, inspect, filter/sort/group, merge, and export. Dataset load and cleaning trace are reproducible with `python src/run_analysis.py`.')
code('''clean=pd.read_csv(ROOT/"datasets/processed/online_retail_clean.csv",parse_dates=["InvoiceDate"])
print(clean.shape); display(clean.head()); display(clean.dtypes); display(clean.describe(include="all").T.head(10))
valid=clean.query("IsCancellation == False and Quantity > 0 and UnitPrice > 0").copy()
print(valid.sort_values("LineRevenue",ascending=False)[["InvoiceNo","Country","LineRevenue"]].head())
country_kpi=valid.groupby("Country",as_index=False).agg(revenue=("LineRevenue","sum"),orders=("InvoiceNo","nunique"))
display(country_kpi.sort_values("revenue",ascending=False).head())
# Join grouped customer KPIs to a small country dimension as a merge demonstration
dim=country_kpi[["Country"]].drop_duplicates(); joined=country_kpi.merge(dim,on="Country",validate="one_to_one")
print("merged rows",len(joined),"missing IDs retained as unknown",clean.CustomerID.isna().sum())''')
md('## 4. SQL and Database Management\nMySQL 8 schema, indexes, 24 analytical queries (CTEs, subqueries, CASE, joins/window functions, views) are in `04_SQL/`. Import the processed CSV with MySQL Workbench. A MySQL server/Workbench was not available in this execution environment; SQL files are MySQL-targeted and local database execution is an evaluator setup step.')
code('print((ROOT/"04_SQL/02_analytical_queries_mysql.sql").read_text()[:2200])')
md('## 5. Data Cleaning and Preprocessing\nExact duplicate rows are removed. IDs retain string semantics, dates parse as timestamps, descriptions/countries are trimmed and cased, missing descriptions become `UNKNOWN PRODUCT`. CustomerID remains null because customer identity cannot be safely inferred; transaction-level country and revenue analysis retains those rows. Cancellation/return rows stay in the audit-clean export but are excluded from positive-sales KPIs. Extreme valid values are retained; plot caps only improve legibility.')
code('''profile=json.load(open(ROOT/"datasets/processed/data_profile.json")); results=json.load(open(ROOT/"datasets/processed/analysis_results.json"))
print(json.dumps(profile,indent=2))
assert clean.duplicated().sum()==0
assert pd.to_datetime(clean.InvoiceDate,errors="coerce").notna().all()
assert (valid.Quantity>0).all() and (valid.UnitPrice>0).all()
print("clean validation passed")
# Encoding/normalization demonstration (not used by the tree model, which is scale-insensitive)
from sklearn.preprocessing import StandardScaler
sample_prep=valid[["Quantity","UnitPrice","Country"]].sample(1000,random_state=42)
encoded_country=pd.get_dummies(sample_prep["Country"],prefix="country",dtype=int)
scaled_num=pd.DataFrame(StandardScaler().fit_transform(sample_prep[["Quantity","UnitPrice"]]),columns=["Quantity_z","UnitPrice_z"])
print("encoded columns",encoded_country.shape[1],"standardized means",scaled_num.mean().round(3).to_dict())''')
md('## 6. EDA and statistical analysis\nKPI totals are gross positive-sales line revenue (not profit); canceled and returned lines are excluded from this metric. Customer RFM excludes records without CustomerID. Associations are descriptive.')
code('''print(json.dumps(results,indent=2))
sample_corr=valid[["Quantity","UnitPrice"]].sample(10000,random_state=42)\nprint("Spearman quantity vs price",stats.spearmanr(sample_corr.Quantity,sample_corr.UnitPrice))
print("No causal interpretation: transaction data are observational.")''')
md('## 7. Data Visualization\nSixteen labeled charts are generated by the analysis script; selected output shown below. The other charts are in `visualizations/`, with descriptive chart-specific titles and axes.')
code('''from IPython.display import display, Image
for f in sorted((ROOT/"visualizations").glob("*.png")):
    print(f.name); display(Image(filename=str(f),width=720))''')
md('## 8. Power BI Dashboard\nDashboard plan: KPI cards for gross sales, orders, units, identified customers, and repeat-customer share; monthly sales trend; top country/product bars; map only if supported by data category; slicers for date, country and product; drill-through to invoice/customer. Power Query steps and DAX are in `08_PowerBI/`. A static preview is included. A native `.pbix` file cannot be generated/validated here because Power BI Desktop is not available in this environment.')
code('from IPython.display import display, Image\ndisplay(Image(filename=str(ROOT/"visualizations/12_kpi_dashboard.png"),width=800))\nprint((ROOT/"08_PowerBI/DAX_measures.dax").read_text())')
md('## 9. Machine Learning Fundamentals\nDaily revenue regression uses time-ordered holdout dates. Lag/rolling predictors are computed from previous days only. Weekly-naive baseline predicts revenue from seven days earlier. Compare MAE/RMSE/R²; the ML model does not outperform this baseline here, so do not deploy it as a forecast. This is a learning exercise, not a production model.')
code('''m=results["forecast_metrics"]
print(json.dumps(m,indent=2))
assert m["test_start"]>m["train_end"]
assert m["MAE_GBP"]>=0 and m["weekly_naive_MAE_GBP"]>=0
print("Model-vs-baseline MAE delta (£):",round(m["MAE_GBP"]-m["weekly_naive_MAE_GBP"],2))''')
md('## 10. Tool Comparison and Conclusion\nUse Excel for small, auditable ad hoc tables; Python for repeatable transformations and modeling. NumPy is efficient for numeric arrays; Pandas adds labeled relational data tools. SQL is best for persistent, set-based filtering/aggregation near a database; Python coordinates analysis and modeling. Power BI provides governed interactive reporting; Matplotlib/Seaborn provide reproducible static figures. Jupyter is a local reproducible artifact; Colab eases cloud setup but requires data governance review. Scikit-learn standardizes model pipelines/validation; direct SciPy/statistical calculations are better for explicit inferential tests.\n\n**Responsible interpretation:** UCI data are historical and observational. No causal impact, margin, current trading behavior, or future forecast reliability is established. Dataset attribution is required under CC BY 4.0.')
nb.cells=c; nb.metadata={"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3"}}
nbf.write(nb,R/'notebooks/Data_Science_Tool_Mastery.ipynb')
print('Wrote',len(c),'cells')
