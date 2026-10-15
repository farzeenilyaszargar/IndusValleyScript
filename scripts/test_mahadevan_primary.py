import unittest
from mahadevan_primary import normalize,secondary_audit,book_page

def row(signs,side='0',doc='x',direction='1'):
 f={f'S{i}':signs[i-1] if i<=len(signs) else '' for i in range(1,15)}
 f.update(textnum='1001',sideline=side,dir=direction,fs80=13,inscobj='1',locus='17',level='-3',
          posnum=str(len(signs)),signnum=str(sum(str(s).lstrip('*')!='0' for s in signs)))
 return {'document_id':doc,'fields':f}

class PrimaryTests(unittest.TestCase):
 def test_uncertainty_and_unknown_cardinality_preserved(self):
  x=normalize(row(['*086','0','342']))
  self.assertEqual(x['signs'],['M086','<GAP>','M342'])
  self.assertEqual(x['integer_slots'],[89,1,345])
  self.assertTrue(x['tokens'][0]['doubtful'])
  self.assertIn('unknown_stretch',x['exclusion_reasons']);self.assertIn('doubtful_sign',x['exclusion_reasons'])
 def test_face_and_line_comparison(self):
  rs=[normalize(row(['86'],'11','a')),normalize(row(['342'],'12','b')),normalize(row(['99'],'20','c'))]
  out=secondary_audit(rs,[{'id':'1001-A','seq':[86,342]},{'id':'1001-B','seq':[99]}])
  self.assertEqual(out['counts'],{'same_base_sequence':2})
  self.assertEqual(out['rows_concatenating_primary_lines'],1)
  self.assertIn('not_single_line',rs[0]['exclusion_reasons'])
 def test_slot_and_count_corruption_excluded(self):
  a=row(['86','','342']);a['fields']['signnum']='2'
  x=normalize(a);self.assertIn('discontinuous_slots',x['exclusion_reasons'])
  self.assertIn('count_metadata_mismatch',x['exclusion_reasons'])
 def test_scanned_sign_list_page_boundaries(self):
  self.assertEqual([book_page(i) for i in (1,110,111,219,220,329,330,417)],[43,43,44,44,45,45,46,46])

if __name__=='__main__':unittest.main()
