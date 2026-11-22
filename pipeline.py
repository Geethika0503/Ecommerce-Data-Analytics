from pathlib import Path
import argparse, sqlite3, urllib.request, zipfile, io
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
RAW=ROOT/'data/raw/Online Retail.xlsx'
OUT=ROOT/'data/processed'
URL='https://archive.ics.uci.edu/static/public/352/online+retail.zip'

def download():
    if RAW.exists(): return
    RAW.parent.mkdir(parents=True,exist_ok=True)
    with urllib.request.urlopen(URL,timeout=120) as response:
        with zipfile.ZipFile(io.BytesIO(response.read())) as z:
            name=next(n for n in z.namelist() if n.lower().endswith('.xlsx'))
            RAW.write_bytes(z.read(name))

def clean(df):
    df=df.copy()
    df.columns=df.columns.str.strip()
    for c in ['InvoiceNo','StockCode','Description','Country','CustomerID']:
        df[c]=df[c].astype('string').str.strip().replace('',pd.NA)
    df['CustomerID']=df.CustomerID.str.replace(r'\.0$','',regex=True)
    df['InvoiceDate']=pd.to_datetime(df.InvoiceDate,errors='coerce')
    for c in ['Quantity','UnitPrice']: df[c]=pd.to_numeric(df[c],errors='coerce')
    audit={'raw_rows':len(df),'exact_duplicate_rows':int(df.duplicated().sum()),'missing_customer_rows':int(df.CustomerID.isna().sum())}
    # Exact duplicates retained: identical invoice lines can represent real purchases.
    valid=df[['InvoiceNo','StockCode','InvoiceDate','Quantity','UnitPrice']].notna().all(axis=1)&np.isfinite(df.Quantity)&np.isfinite(df.UnitPrice)&(df.UnitPrice>0)
    cancelled=df.InvoiceNo.str.upper().str.startswith('C',na=False)
    sales=df[valid & ~cancelled & (df.Quantity>0)].copy()
    returns=df[valid & (df.Quantity<0)].copy()
    for frame in [sales,returns]:
        frame['Description']=frame.Description.fillna('Unknown product')
        frame['Country']=frame.Country.fillna('Unknown')
        frame['Revenue']=frame.Quantity*frame.UnitPrice
        frame['Month']=frame.InvoiceDate.dt.strftime('%Y-%m')
    audit.update(sales_rows=len(sales),return_rows=len(returns),excluded_rows=len(df)-len(sales)-len(returns))
    return sales,returns,pd.DataFrame(audit.items(),columns=['Metric','Value'])

def summarize(s,r):
    known=s.dropna(subset=['CustomerID']); reference=s.InvoiceDate.max().normalize()+pd.Timedelta(days=1)
    rfm=known.groupby('CustomerID').agg(LastPurchase=('InvoiceDate','max'),Frequency=('InvoiceNo','nunique'),Monetary=('Revenue','sum')).reset_index()
    rfm['Recency']=(reference-rfm.LastPurchase.dt.normalize()).dt.days
    for col,score,ascending in [('Recency','R',False),('Frequency','F',True),('Monetary','M',True)]:
        rfm[score]=np.ceil(rfm[col].rank(method='average',pct=True,ascending=ascending)*5).astype(int)
    rfm['Segment']=np.select([(rfm.R>=4)&(rfm.F>=4)&(rfm.M>=4),(rfm.R<=2)&(rfm.F>=3),rfm.R>=4,rfm.F>=4],['Champions','At risk','Recent customers','Frequent customers'],default='Other')
    monthly=s.groupby('Month').Revenue.sum().rename('GrossRevenue').to_frame().join((-r.groupby('Month').Revenue.sum()).rename('ReturnValue'),how='outer').fillna(0).sort_index().reset_index()
    monthly['NetRecordedValue']=monthly.GrossRevenue-monthly.ReturnValue
    monthly['GrowthPct']=monthly.GrossRevenue.pct_change()*100
    products=s.groupby('StockCode').agg(Units=('Quantity','sum'),Revenue=('Revenue','sum')).sort_values('Revenue',ascending=False).reset_index()
    countries=s.groupby('Country').Revenue.sum().sort_values(ascending=False).reset_index()
    orders=s.InvoiceNo.nunique(); gross=s.Revenue.sum(); returned=-r.Revenue.sum()
    kpis=pd.DataFrame({'Metric':['Gross sales (£)','Recorded returns (£)','Net recorded value (£)','Purchase invoices','Known customers','Average invoice value (£)','Repeat customer rate (%)'],'Value':[gross,returned,gross-returned,orders,len(rfm),gross/orders if orders else 0,100*(rfm.Frequency>1).mean() if len(rfm) else 0]})
    return {'kpis':kpis,'monthly':monthly,'products':products,'countries':countries,'rfm':rfm}

def run(path):
    OUT.mkdir(parents=True,exist_ok=True)
    for folder in ['images','excel','reports']: (ROOT/folder).mkdir(exist_ok=True)
    raw=pd.read_excel(path,engine='openpyxl') if str(path).lower().endswith('.xlsx') else pd.read_csv(path)
    s,r,a=clean(raw)
    if s.empty: raise ValueError('No valid purchase lines found')
    tables={'sales':s,'returns':r,'quality':a,**summarize(s,r)}
    with sqlite3.connect(OUT/'retail.db') as con:
        for name,table in tables.items():
            table.to_csv(OUT/f'{name}.csv',index=False)
            table.to_sql(name,con,if_exists='replace',index=False)
    with pd.ExcelWriter(ROOT/'excel/retail_report.xlsx',engine='openpyxl') as writer:
        for name in ['kpis','monthly','products','countries','rfm','quality']:
            tables[name].to_excel(writer,sheet_name=name,index=False)
            ws=writer.sheets[name]; ws.freeze_panes='A2'; ws.auto_filter.ref=ws.dimensions
            from openpyxl.styles import Font, PatternFill
            for cell in ws[1]: cell.font=Font(bold=True,color='FFFFFF'); cell.fill=PatternFill('solid',fgColor='17365D')
            for col in ws.columns:
                ws.column_dimensions[col[0].column_letter].width=min(42,max(15,len(str(col[0].value))+3))
    for name,table,x,y,title in [('monthly',tables['monthly'],'Month','GrossRevenue','Monthly gross sales (£)'),('products',tables['products'].head(10),'StockCode','Revenue','Top 10 products by gross sales (£)'),('countries',tables['countries'].head(10),'Country','Revenue','Top 10 countries by gross sales (£)')]:
        fig,ax=plt.subplots(figsize=(10,5)); ax.bar(table[x],table[y]); ax.set_title(title); ax.tick_params(axis='x',rotation=45); fig.tight_layout(); fig.savefig(ROOT/f'images/{name}.png',dpi=140); plt.close(fig)
    k=tables['kpis']; top=tables['countries'].iloc[0]; best=tables['products'].iloc[0]
    lines=['# Business findings','',*[f'- {m}: {v:,.2f}' for m,v in zip(k.Metric,k.Value)],'',f'Largest market: {top.Country} (£{top.Revenue:,.2f}).',f'Highest revenue product code: {best.StockCode} (£{best.Revenue:,.2f}).','','Recommendations: investigate demand and inventory for high-revenue products; test retention campaigns for at-risk known customers; investigate return reasons before acting. These are hypotheses, not causal findings. December 2011 is partial; avoid comparing it directly with full months.']
    (ROOT/'reports/business_insights.md').write_text('\n'.join(lines),encoding='utf-8')
    print(k.to_string(index=False))
    return tables

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--input',type=Path,default=RAW); p.add_argument('--download',action='store_true'); args=p.parse_args()
    if args.download: download()
    if not args.input.exists(): p.error('Dataset missing. Use --download or place Online Retail.xlsx in data/raw.')
    run(args.input)
