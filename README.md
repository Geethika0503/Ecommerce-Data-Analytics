
# E-Commerce Sales & Customer Behaviour Analysis

## Project Overview

This project focuses on analyzing real-world e-commerce transactions to understand sales performance, customer purchasing behaviour, revenue trends and customer segmentation.

The project uses Python, SQL, Excel and Streamlit to transform raw transactional data into meaningful business insights and support data-driven decision-making.

## Features

- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- Sales and revenue analysis
- Monthly sales trend analysis
- Product and stock code performance analysis
- Country-wise sales analysis
- Repeat customer analysis
- RFM customer segmentation
- SQL-based business analysis
- Interactive Streamlit dashboard
- Excel business reporting

## Technologies Used

- Python
- Pandas
- NumPy
- SQL
- SQLite
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Microsoft Excel
- Jupyter Notebook
- Git and GitHub

## Dataset

The project uses the UCI Online Retail Dataset, which contains real-world transactions from a UK-based online retail business.

| Dataset Information | Details |
|---|---|
| Dataset | Online Retail |
| Source | UCI Machine Learning Repository |
| Total Records | 541,909 |
| Number of Columns | 8 |
| Duration | December 2010 – December 2011 |
| Currency | British Pounds (£) |

Dataset Link: [UCI Online Retail Dataset]\(https\://archive.ics.uci.edu/dataset/352/online-retail)

## Data Cleaning and Preprocessing

- Audited duplicate records.
- Identified missing customer IDs.
- Validated numerical and categorical columns.
- Converted invoice dates into datetime format.
- Separated purchase and return transactions.
- Identified invalid quantities and prices.
- Calculated transaction revenue.
- Prepared data for further analysis and visualization.

## Dashboard Overview

The interactive Streamlit dashboard provides an overview of business performance through KPI cards, monthly sales trends, country filters and customer segmentation.

![Dashboard Overview]\(images/dashboard_overview\.png)

## Key Performance Indicators

| Metric | Result |
|---|---:|
| Gross Sales | £10,666,685 |
| Net Recorded Value | £9,769,872 |
| Recorded Returns | £896,813 |
| Purchase Invoices | 19,960 |
| Known Customers | 4,338 |
| Average Invoice Value | £534.40 |
| Repeat Customer Rate | 65.58% |

## Sales and Customer Analysis

### 1. Monthly Sales Analysis

- Analyzed monthly revenue trends.
- Identified peak sales periods.
- Evaluated month-over-month revenue growth.
- November 2011 recorded the highest monthly gross sales of approximately £1.51 million.

### 2. Product Performance Analysis\

Identified the top 10 revenue-generating stock codes to understand sales performance.

![Product Analysis]\(images/product_analysis.png)

Some stock codes represent postage and miscellaneous charges rather than physical products.

### 3. Country-wise Sales Analysis

Analyzed revenue across different geographical markets to identify the highest-performing countries.

![Country Analysis]\(images/country_analysis.png)

The United Kingdom contributed approximately 84.61% of total gross sales, followed by the Netherlands, Ireland, Germany and France.

### 4. RFM Customer Segmentation

Customers were categorized using the RFM analysis technique:

- \*\*Recency:\*\* How recently a customer made a purchase.
- \*\*Frequency:\*\* How frequently a customer made purchases.
- \*\*Monetary:\*\* How much a customer spent.

![Customer Segmentation]\(images/customer_segmentation.png)

### 5. Customer Segment Distribution

![Customer Distribution]\(images/customer_distribution.png)

| Customer Segment | Number of Customers |
|---|---:|
| Other Customers | 1,561 |
| Champions | 911 |
| Recent Customers | 837 |
| At Risk | 765 |
| Frequent Customers | 264 |
| Total | 4,338 |

### Customer Segment Summary

![Customer Summary]\(images/customer_summary.png)

## SQL Analysis

SQL queries were implemented using SQLite to analyze:

- Overall business performance
- Monthly sales and revenue
- Top revenue-generating stock codes
- Country-wise sales performance
- Repeat customer rate
- Month-over-month growth
- Customer segment performance
- Recorded returns and net recorded value

SQL concepts used include aggregate functions, joins, GROUP BY, ORDER BY, Common Table Expressions (CTEs), window functions and LAG functions.

## Key Business Insights

- The business generated approximately £10.67 million in gross sales.
- November 2011 recorded the highest monthly gross sales of £1.51 million.
- Monthly gross sales increased by 30.69% in November compared with October 2011.
- The United Kingdom accounted for 84.61% of total gross sales.
- Approximately 65.58% of known purchasing customers made repeat purchases.
- Champion customers contributed approximately £5.69 million in gross sales.
- 765 customers were identified as at risk through RFM segmentation.
- Recorded returns accounted for approximately 8.41% of gross sales.

## Business Recommendations

- Introduce loyalty programs for high-value customers.
- Develop targeted campaigns to re-engage at-risk customers.
- Encourage recent customers to make repeat purchases.
- Improve inventory planning during peak sales periods.
- Explore opportunities in international markets.
- Investigate the reasons behind recorded returns.
- Monitor business performance through interactive dashboards.

## Learning Outcomes

Through this project, I gained practical experience in:

- Working with large real-world datasets.
- Data cleaning and preprocessing using Python and Pandas.
- Performing exploratory data analysis.
- Writing analytical SQL queries.
- Calculating business KPIs.
- Implementing RFM customer segmentation.
- Creating interactive dashboards using Streamlit and Plotly.
- Understanding customer purchasing behaviour.
- Generating actionable business insights.
- Data storytelling and business reporting.

## Future Improvements

- Sales forecasting using time-series analysis.
- Customer lifetime value analysis.
- Market basket analysis.
- Customer churn prediction.
- Power BI dashboard implementation.
- Automated business reporting.

## Data Limitations

- December 2011 contains partial-month data.
- Revenue represents sales value, not profit.
- RFM segmentation is based on historical purchasing behaviour.
- Recorded returns are not matched to original purchase invoices.
- Repeat customer rate does not represent cohort retention.

## Dataset Acknowledgement

- Source: UCI Machine Learning Repository – Online Retail Dataset
- Author: Daqing Chen (2015)
- DOI: https\://doi.org/10.24432/C5BW33
- License: CC BY 4.0