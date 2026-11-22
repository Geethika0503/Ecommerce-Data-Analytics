import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import clean,summarize
import pandas as pd
class Tests(unittest.TestCase):
    def test_totals(self):
        df=pd.DataFrame([['1','A','A',2,'2011-01-01',5,1,'UK'],['2','A','A',1,'2011-02-01',5,1,'UK'],['C3','A','A',-1,'2011-02-01',5,1,'UK'],['4','B','B',1,'2011-02-01',4,None,'UK']],columns=['InvoiceNo','StockCode','Description','Quantity','InvoiceDate','UnitPrice','CustomerID','Country'])
        s,r,a=clean(df); t=summarize(s,r); self.assertEqual(s.Revenue.sum(),19); self.assertEqual(r.Revenue.sum(),-5); self.assertEqual(len(t['rfm']),1); self.assertEqual(t['rfm'].Frequency.iloc[0],2)
if __name__=='__main__': unittest.main()
