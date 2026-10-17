import unittest
from reference_candidates import candidates,partition

class ReferenceTests(unittest.TestCase):
 def test_candidate_does_not_join_another_face(self):
  refs=[{'cisi_object':'M-1','fc_raw':'1067','uncertain_digits':False}]
  ps=[{'id':'M-1A','signs':['P1'],'exclusion_reasons':[]}]
  ms=[{'textnum':'1067','side':1,'line':0,'document_id':'a','signs':['M1'],'exclusion_reasons':[]}]
  pairs,rejected=candidates(refs,ps,ms)
  self.assertFalse(pairs);self.assertEqual(rejected[0]['reason'],'missing_or_ambiguous_primary_single_side_line')
 def test_uncertain_reference_excluded(self):
  refs=[{'cisi_object':'M-4','fc_raw':'0108','uncertain_digits':True}]
  _,rejected=candidates(refs,[],[]);self.assertEqual(rejected[0]['reason'],'uncertain_reference_digits')
 def test_pilot_and_duplicate_group_stay_in_train(self):
  pairs=[{'object':f'M-{i}','parpola_signs':[f'P{i}'],'mahadevan_signs':[f'M{i}']} for i in range(1,16)]
  pairs.append({'object':'M-99','parpola_signs':['P1'],'mahadevan_signs':['M99']})
  parts,_=partition(pairs);train={p['object'] for p in parts[0]}
  self.assertTrue({'M-1','M-99'}<=train)
  self.assertTrue(all('M-1' not in {p['object'] for p in part} for part in parts[1:]))

if __name__=='__main__':unittest.main()
