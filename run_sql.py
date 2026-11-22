from pathlib import Path
import sqlite3,pandas as pd
root=Path(__file__).resolve().parent
path=root/'data/processed/retail.db'
if not path.exists(): raise SystemExit('Run pipeline.py first')
with sqlite3.connect(path) as con:
    for query in (root/'sql/business_queries.sql').read_text().split(';'):
        if query.strip(): print(pd.read_sql_query(query,con).to_string(index=False),'\n')
