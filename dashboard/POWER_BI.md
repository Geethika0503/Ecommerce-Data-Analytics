# Power BI Desktop build guide
1. Run pipeline.py. Open Power BI Desktop > Get Data > Text/CSV. Import data/processed/sales.csv, returns.csv, rfm.csv.
2. In Power Query set InvoiceNo, StockCode, CustomerID to Text, InvoiceDate to Date/Time, Revenue to Decimal Number; rename tables sales, returns, rfm. Load.
3. Create measures (one at a time):
```dax
Gross Sales = SUM(sales[Revenue])
Purchase Invoices = DISTINCTCOUNT(sales[InvoiceNo])
Known Customers = DISTINCTCOUNTNOBLANK(sales[CustomerID])
Average Invoice = DIVIDE([Gross Sales], [Purchase Invoices])
Recorded Returns = -SUM(returns[Revenue])
Net Recorded Value = [Gross Sales] - [Recorded Returns]
```
4. Create a month dimension using New Table: `Months = DISTINCT(UNION(SELECTCOLUMNS(sales,"Month",sales[Month]),SELECTCOLUMNS(returns,"Month",returns[Month])))`. Create one-to-many single-direction relationships from Months[Month] to both fact tables. Likewise create `Countries = DISTINCT(UNION(SELECTCOLUMNS(sales,"Country",sales[Country]),SELECTCOLUMNS(returns,"Country",returns[Country])))` and connect Country to both facts. Use dimension fields for slicers.
5. Sales overview: KPI cards for measures, line chart Month vs Gross Sales, bar chart Country vs Gross Sales, product bar chart StockCode vs Gross Sales (Top N 10).
6. Customer page: use rfm[Segment] and count of CustomerID; scatter Frequency vs Monetary with Recency as size. This page is full-period; do not imply date filtering.
7. Format currency as GBP. Add a note about incomplete final month and return methodology. Save dashboard/ecommerce_dashboard.pbix. Export a screenshot to images/dashboard_preview.png.
