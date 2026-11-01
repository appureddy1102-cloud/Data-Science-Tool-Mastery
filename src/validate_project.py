from pathlib import Path
import json, zipfile
import pandas as pd, nbformat, sqlglot
R=Path(__file__).resolve().parents[1]
raw=pd.read_excel(R/'datasets/raw/Online Retail.xlsx',engine='openpyxl')
clean=pd.read_csv(R/'datasets/processed/online_retail_clean.csv',low_memory=False)
assert raw.shape==(541909,8),raw.shape
assert clean.shape==(536641,11),clean.shape
assert clean.duplicated().sum()==0
assert clean.CustomerID.isna().sum()==135037
assert (clean.IsCancellation == clean.InvoiceNo.astype(str).str.startswith('C')).all()
sales=clean[(~clean.IsCancellation)&(clean.Quantity>0)&(clean.UnitPrice>0)]
assert len(sales)==524878
res=json.load(open(R/'datasets/processed/analysis_results.json'))
assert round((sales.Quantity*sales.UnitPrice).sum(),2)==res['sales_revenue_gbp']
assert len(list((R/'visualizations').glob('*.png')))==16
nb=nbformat.read(R/'notebooks/Data_Science_Tool_Mastery.ipynb',as_version=4)
errs=[o for c in nb.cells for o in c.get('outputs',[]) if o.get('output_type')=='error']
assert not errs,errs
for f in ['01_schema_mysql.sql','02_analytical_queries_mysql.sql','03_normalize_mysql.sql']:
 assert sqlglot.parse((R/'04_SQL'/f).read_text(),read='mysql')
for f in [R/'reports/Data_Science_Tool_Mastery_Report.docx',R/'datasets/retail_analytics_data.zip',R/'visualizations/visualizations.zip']:
 with zipfile.ZipFile(f) as z: assert z.testzip() is None
print('PASS raw',raw.shape,'clean',clean.shape,'sales lines',len(sales),'revenue',res['sales_revenue_gbp'],'charts',16,'notebook errors',len(errs),'MySQL files parse')
