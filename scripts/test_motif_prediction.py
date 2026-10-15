import unittest
from motif_prediction import partition,target_map,Predictor

def row(doc,obj,signs,field='13'):
 return {'document_id':doc,'textnum':obj,'signs':signs,'field_symbol_code':field,'object_code':'1','side':0,'line':0}

class MotifTests(unittest.TestCase):
 def test_transitive_face_and_reverse_groups(self):
  rows=[row('a','1001',['A','B']),row('b','1001',['C']),row('c','1002',['B','A']),row('d','1003',['D'])]
  parts,groups=partition(rows);members=[{r['document_id'] for r in g} for g in groups.values()]
  self.assertIn({'a','b','c'},members);self.assertIn({'d'},members)
 def test_target_threshold_counts_objects_not_faces(self):
  rows=[row(str(i),'1001',['A']) for i in range(20)]
  self.assertEqual(target_map(rows),{'13':'RARE'})
  rows=[row(str(i),str(1001+i),['A']) for i in range(20)]
  self.assertEqual(target_map(rows),{'13':'13'})
 def test_probability_and_unknown_evidence(self):
  train=[row('a','1001',['A'],'11'),row('b','1002',['B'],'13')]
  m=Predictor(train,{'11':'11','13':'13'},5)
  r=row('c','1003',['UNSEEN'],'999')
  self.assertEqual(m.target(r),'RARE')
  self.assertEqual(m.probabilities(r,0),m.probabilities(r,2))
  self.assertAlmostEqual(sum(m.probabilities(train[0],1).values()),1)
  self.assertGreater(m.probabilities(train[0],1)['11'],m.probabilities(train[0],0)['11'])

if __name__=='__main__':unittest.main()
