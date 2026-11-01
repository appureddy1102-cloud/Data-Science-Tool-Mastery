from pathlib import Path
import json, warnings
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, seaborn as sns
from scipy import stats
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'datasets/raw/Online Retail.xlsx'; OUT=ROOT/'datasets/processed'; VIZ=ROOT/'visualizations'
OUT.mkdir(exist_ok=True); VIZ.mkdir(exist_ok=True)
sns.set_theme(style='whitegrid',palette='deep')
raw=pd.read_excel(RAW,engine='openpyxl')
df=raw.drop_duplicates().copy()
df['InvoiceNo']=df.InvoiceNo.astype(str).str.strip().str.upper(); df['StockCode']=df.StockCode.astype(str).str.strip().str.upper()
df['Description']=df.Description.fillna('Unknown product').astype(str).str.strip().str.upper()
df['Country']=df.Country.astype(str).str.strip().str.title()
df['CustomerID']=df.CustomerID.astype('Int64')
df['InvoiceDate']=pd.to_datetime(df.InvoiceDate,errors='coerce')
df['Quantity']=pd.to_numeric(df.Quantity,errors='coerce'); df['UnitPrice']=pd.to_numeric(df.UnitPrice,errors='coerce')
df['IsCancellation']=df.InvoiceNo.str.startswith('C')
df['LineRevenue']=df.Quantity*df.UnitPrice
# Keep raw-valid transactions in cleaned file; signed returns/cancellations are retained for audit.
df['Date']=df.InvoiceDate.dt.date
# Sales cohort excludes cancellations, nonpositive quantity/prices and missing timestamps; missing customer id allowed for noncustomer aggregates.
sales=df[(~df.IsCancellation)&df.Quantity.gt(0)&df.UnitPrice.gt(0)&df.InvoiceDate.notna()].copy()
sales['GrossRevenue']=sales.Quantity*sales.UnitPrice
df.to_csv(OUT/'online_retail_clean.csv',index=False)
# Date-level time series with complete calendar and causal lag/rolling features
sales['Day']=sales.InvoiceDate.dt.floor('D')
daily=sales.groupby('Day').agg(Revenue=('GrossRevenue','sum'),Orders=('InvoiceNo','nunique'),Units=('Quantity','sum'),Customers=('CustomerID','nunique')).asfreq('D',fill_value=0).rename_axis('Date').reset_index()
# add causal features: past values only
for lag in [1,7,14,28]: daily[f'lag_{lag}']=daily.Revenue.shift(lag)
for win in [7,28]: daily[f'roll_mean_{win}']=daily.Revenue.shift(1).rolling(win).mean()
daily['dow']=daily.Date.dt.dayofweek; daily['month']=daily.Date.dt.month; daily['dayofmonth']=daily.Date.dt.day
modeldata=daily.dropna().copy(); split=int(len(modeldata)*.8); train,test=modeldata.iloc[:split],modeldata.iloc[split:]
features=['lag_1','lag_7','lag_14','lag_28','roll_mean_7','roll_mean_28','dow','month','dayofmonth']
model=HistGradientBoostingRegressor(max_iter=140,max_leaf_nodes=12,l2_regularization=2,random_state=42).fit(train[features],train.Revenue)
pred=np.maximum(0,model.predict(test[features])); naive=test.lag_7.to_numpy()
metrics={'source':'UCI Online Retail','raw_rows':int(len(raw)),'raw_columns':int(raw.shape[1]),'clean_rows':int(len(df)),'duplicate_rows_removed':int(raw.duplicated().sum()),'clean_missing_customer_id':int(df.CustomerID.isna().sum()),'clean_missing_description_filled':int(raw.Description.isna().sum()),'sales_rows':int(len(sales)),'cancellation_rows_retained_clean_table':int(df.IsCancellation.sum()),'sales_start':str(sales.InvoiceDate.min()),'sales_end':str(sales.InvoiceDate.max()),'unique_customers_nonnull':int(sales.CustomerID.nunique()),'countries':int(sales.Country.nunique()),'sales_revenue_gbp':round(float(sales.GrossRevenue.sum()),2),'order_count':int(sales.InvoiceNo.nunique()),'unit_count':int(sales.Quantity.sum()),'daily_mean_revenue':round(float(daily.Revenue.mean()),2),'top_countries':sales.groupby('Country').GrossRevenue.sum().sort_values(ascending=False).head(10).round(2).to_dict(),'top_products':sales.groupby('Description').GrossRevenue.sum().sort_values(ascending=False).head(10).round(2).to_dict(),'top_country_share_pct':round(float(sales.groupby('Country').GrossRevenue.sum().max()/sales.GrossRevenue.sum()*100),2),'test_days':int(len(test)),'forecast_metrics':{'MAE_GBP':round(float(mean_absolute_error(test.Revenue,pred)),2),'RMSE_GBP':round(float(mean_squared_error(test.Revenue,pred)**.5),2),'R2':round(float(r2_score(test.Revenue,pred)),4),'weekly_naive_MAE_GBP':round(float(mean_absolute_error(test.Revenue,naive)),2),'baseline_RMSE_GBP':round(float(mean_squared_error(test.Revenue,naive)**.5),2),'train_end':str(train.Date.max().date()),'test_start':str(test.Date.min().date())}}
# Customer RFM and statistical results
cust=sales[sales.CustomerID.notna()].groupby('CustomerID').agg(LastPurchase=('InvoiceDate','max'),Orders=('InvoiceNo','nunique'),Revenue=('GrossRevenue','sum'),Units=('Quantity','sum'))
ref=sales.InvoiceDate.max()+pd.Timedelta(days=1); cust['RecencyDays']=(ref-cust.LastPurchase).dt.days
cust.to_csv(OUT/'customer_rfm.csv')
metrics['customer_summary']={'customers':int(len(cust)),'median_revenue':round(float(cust.Revenue.median()),2),'mean_orders':round(float(cust.Orders.mean()),2),'repeat_customer_share_pct':round(float((cust.Orders>1).mean()*100),2),'pearson_orders_revenue_r':round(float(cust.Orders.corr(cust.Revenue)),4)}
# charts 16 distinct meaningful visuals
fig,ax=plt.subplots(figsize=(10,5)); sales.groupby(sales.InvoiceDate.dt.to_period('M')).GrossRevenue.sum().plot(ax=ax); ax.set(title='Monthly Gross Sales Revenue',xlabel='Month',ylabel='Revenue (£)');ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,pos:f'£{x/1e6:.1f}m'));fig.autofmt_xdate();fig.tight_layout();fig.savefig(VIZ/'01_monthly_revenue.png',dpi=180);plt.close(fig)
country=sales.groupby('Country').GrossRevenue.sum().nlargest(10).sort_values();fig,ax=plt.subplots(figsize=(9,6));country.plot.barh(ax=ax);ax.set(title='Top 10 Countries by Gross Revenue',xlabel='Revenue (£)',ylabel='Country');fig.tight_layout();fig.savefig(VIZ/'02_top_countries_bar.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5));sns.histplot(sales.GrossRevenue.clip(upper=sales.GrossRevenue.quantile(.99)),bins=60,ax=ax);ax.set(title='Line Revenue Distribution (clipped at 99th percentile for display)',xlabel='Line revenue (£)',ylabel='Line count');fig.tight_layout();fig.savefig(VIZ/'03_revenue_histogram.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5));sns.boxplot(x=sales.GrossRevenue.clip(upper=sales.GrossRevenue.quantile(.99)),ax=ax);ax.set(title='Line Revenue Box Plot (display clipped at 99th percentile)',xlabel='Line revenue (£)');fig.tight_layout();fig.savefig(VIZ/'04_revenue_boxplot.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,5));sns.scatterplot(data=sales.sample(min(6000,len(sales)),random_state=42),x='Quantity',y='UnitPrice',hue='IsCancellation',alpha=.45,ax=ax);ax.set(title='Quantity vs Unit Price (sampled 6,000 rows)',xlabel='Quantity (units)',ylabel='Unit price (£)');fig.tight_layout();fig.savefig(VIZ/'05_quantity_price_scatter.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(10,5));ax.plot(test.Date,test.Revenue,label='Actual',lw=1);ax.plot(test.Date,pred,label='Forecast',lw=1);ax.set(title='Chronological Daily Revenue Forecast (Holdout)',xlabel='Date',ylabel='Revenue (£)');ax.legend();fig.autofmt_xdate();fig.tight_layout();fig.savefig(VIZ/'06_forecast_test.png',dpi=180);plt.close(fig)
# Donut for share top 5 and Other
ct=sales.groupby('Country').GrossRevenue.sum().sort_values(ascending=False); pie=pd.concat([ct.head(5),pd.Series({'Other':ct.iloc[5:].sum()})]);fig,ax=plt.subplots(figsize=(7,7));ax.pie(pie,labels=pie.index,autopct='%1.1f%%',startangle=90,wedgeprops={'width':.42});ax.set_title('Revenue Mix: Top Five Countries vs Other');fig.tight_layout();fig.savefig(VIZ/'07_country_revenue_donut.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,6)); corr=sales[['Quantity','UnitPrice','GrossRevenue']].corr(method='spearman');sns.heatmap(corr,annot=True,cmap='vlag',center=0,ax=ax);ax.set_title('Spearman Correlation of Transaction Metrics');fig.tight_layout();fig.savefig(VIZ/'08_correlation_heatmap.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5)); top=sales.Country.value_counts().head(10);sns.barplot(x=top.values,y=top.index,ax=ax);ax.set(title='Top Countries by Transaction-Line Count',xlabel='Rows',ylabel='Country');fig.tight_layout();fig.savefig(VIZ/'09_country_countplot.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(10,5));topc=sales.groupby('Country').GrossRevenue.sum().nlargest(6).index;sns.violinplot(data=sales[sales.Country.isin(topc)].sample(min(8000,len(sales)),random_state=1),x='Country',y='GrossRevenue',cut=0,ax=ax);ax.set_ylim(0,sales.GrossRevenue.quantile(.95));ax.set(title='Line-Revenue Distributions: Top Countries (95th percentile display limit)',xlabel='Country',ylabel='Line revenue (£)');ax.tick_params(axis='x',rotation=20);fig.tight_layout();fig.savefig(VIZ/'10_country_violin.png',dpi=180);plt.close(fig)
fig,axs=plt.subplots(2,2,figsize=(11,9)); sample=sales[['Quantity','UnitPrice','GrossRevenue']].sample(min(1500,len(sales)),random_state=4);g=sns.pairplot(sample,corner=True,plot_kws={'alpha':.18,'s':10});g.savefig(VIZ/'11_pairplot.png',dpi=160);plt.close('all')
# KPI dashboard static mockup (four KPI cards plus trend and country comparison)
fig=plt.figure(figsize=(14,8),facecolor='#F4F7FB');gs=fig.add_gridspec(3,4,height_ratios=[.9,1.0,2.1],hspace=.38,wspace=.75)
fig.suptitle('Retail KPI Snapshot  |  UCI Online Retail • Historical descriptive view',fontsize=17,fontweight='bold',color='#17365D',y=.97)
card_vals=[f"£{metrics['sales_revenue_gbp']:,.0f}",f"{metrics['order_count']:,}",f"{metrics['unique_customers_nonnull']:,}",f"{metrics['customer_summary']['repeat_customer_share_pct']:.1f}%"]
card_labels=['GROSS SALES GBP','ORDERS','IDENTIFIED CUSTOMERS','REPEAT CUSTOMER RATE']
for i,(val,label) in enumerate(zip(card_vals,card_labels)):
 ax=fig.add_subplot(gs[0,i]);ax.set_facecolor('white');ax.set_xticks([]);ax.set_yticks([]);[sp.set_color('#D9E2F0') for sp in ax.spines.values()]
 ax.text(.07,.70,label,transform=ax.transAxes,fontsize=9,color='#53657D',fontweight='bold');ax.text(.07,.22,val,transform=ax.transAxes,fontsize=20,color='#17365D',fontweight='bold')
ax1=fig.add_subplot(gs[1:,0:2]);ax1.set_facecolor('white');sales.groupby(sales.InvoiceDate.dt.to_period('M')).GrossRevenue.sum().plot(ax=ax1,color='#2E86AB',marker='o',lw=2);ax1.set_title('Monthly Gross Sales Trend',fontweight='bold');ax1.set_xlabel('Month');ax1.set_ylabel('Revenue (£)');ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,pos:f'£{x/1e6:.1f}m'));ax1.tick_params(axis='x',rotation=30)
ax2=fig.add_subplot(gs[1:,2:4]);ax2.set_facecolor('white');sales.groupby('Country').GrossRevenue.sum().nlargest(8).sort_values().plot.barh(ax=ax2,color='#4C9F70');ax2.set_title('Top Countries by Gross Sales',fontweight='bold');ax2.set_xlabel('Revenue (£)');ax2.set_ylabel('');ax2.tick_params(axis='y',labelsize=9);ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,pos:f'£{x/1e6:.1f}m'))
fig.savefig(VIZ/'12_kpi_dashboard.png',dpi=180,bbox_inches='tight');plt.close(fig)
# Additional plots
fig,ax=plt.subplots(figsize=(9,5)); daily.set_index('Date').Revenue.rolling(7).mean().plot(ax=ax,label='7-day moving average');ax.set(title='Daily Revenue Trend with 7-Day Smoothing',xlabel='Date',ylabel='Revenue (£)');ax.legend();fig.tight_layout();fig.savefig(VIZ/'13_revenue_trend.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5));cust.Revenue.clip(upper=cust.Revenue.quantile(.99)).plot.hist(bins=50,ax=ax);ax.set(title='Customer-Level Revenue Distribution (99th percentile display cap)',xlabel='Customer revenue (£)',ylabel='Customers');fig.tight_layout();fig.savefig(VIZ/'14_customer_revenue_hist.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5)); top_p=sales.groupby('Description').GrossRevenue.sum().nlargest(12).sort_values();top_p.plot.barh(ax=ax);ax.set(title='Top Products by Gross Revenue',xlabel='Revenue (£)',ylabel='Product description');fig.tight_layout();fig.savefig(VIZ/'15_top_products.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5));sns.boxplot(data=cust,x='Orders',ax=ax);ax.set(title='Customer Order Count Distribution',xlabel='Distinct invoices per identified customer');fig.tight_layout();fig.savefig(VIZ/'16_customer_orders_box.png',dpi=180);plt.close(fig)
daily.to_csv(OUT/'daily_revenue_features.csv',index=False); json.dump(metrics,open(OUT/'analysis_results.json','w'),indent=2,default=str)
profile={'raw_shape':list(raw.shape),'raw_missing':{k:int(v) for k,v in raw.isna().sum().items()},'raw_duplicates':int(raw.duplicated().sum()),'raw_types':{k:str(v) for k,v in raw.dtypes.items()}}
iqr_audit={}
for col in ['Quantity','UnitPrice','LineRevenue']:
    q1,q3=df[col].quantile([.25,.75]); iqr=q3-q1; lo,hi=q1-1.5*iqr,q3+1.5*iqr
    iqr_audit[col]={'q1':float(q1),'q3':float(q3),'lower_fence':float(lo),'upper_fence':float(hi),'flagged_rows':int(((df[col]<lo)|(df[col]>hi)).sum()),'policy':'flag only; retain valid extremes'}
json.dump(iqr_audit,open(OUT/'iqr_audit.json','w'),indent=2)
profile.update({'clean_shape':list(df.shape),'clean_missing':{k:int(v) for k,v in df.isna().sum().items()},'sales_rows':len(sales),'clean_duplicate_rows':int(df.duplicated().sum()),'dropped_exact_duplicates':int(raw.duplicated().sum()),'outlier_policy':'Revenue outliers retained in analysis; charts cap display range only. Returns/cancellations retained in audit-clean table but excluded from positive-sales forecasting.'})
json.dump(profile,open(OUT/'data_profile.json','w'),indent=2)
print(json.dumps(metrics,indent=2));print('Charts generated:',len(list(VIZ.glob('*.png'))))
