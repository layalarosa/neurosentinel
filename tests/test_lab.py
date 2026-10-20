import sys,unittest
sys.path.insert(0,'src')
from lab import generate,metrics,entropy
class LabTests(unittest.TestCase):
    def test_reproducible(self):self.assertEqual(generate(42,5),generate(42,5))
    def test_split(self):
        rows=generate(42,10)
        self.assertEqual(len(rows),30)
        self.assertEqual(sum(r['split']=='test' for r in rows),6)
    def test_metrics(self):
        rows=[{'label_malicious':1},{'label_malicious':0}]
        self.assertEqual(metrics(rows,[1,0])['f1'],1)
    def test_entropy(self):self.assertEqual(entropy(['a','a']),0)
if __name__=='__main__':unittest.main()
