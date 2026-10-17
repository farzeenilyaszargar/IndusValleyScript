import unittest
from graphic_variants import expand,lookup

class GraphicTests(unittest.TestCase):
 def test_continuation_and_section_ids(self):
  s={'source_url':'https://example.org/book.pdf','segments':[
   {'section':'main','base':245,'pdf_page':798,'printed_page':789,'column':'L','references':['1001','1002'],'uncertain_ordinals':[]},
   {'section':'main','base':245,'pdf_page':798,'printed_page':789,'column':'R','references':['1003'],'uncertain_ordinals':[]},
   {'section':'addendum','base':245,'pdf_page':801,'printed_page':792,'column':'R','references':['1001'],'uncertain_ordinals':[]}]}
  r=expand(s);self.assertEqual([x['family_ordinal'] for x in r],[1,2,3,1]);self.assertEqual(len({x['id'] for x in r}),4)
  self.assertEqual([x['integer'] for x in r],[4,5,6,7])
 def test_repeated_occurrences_are_not_assigned(self):
  r={'document_id':'d','side':1,'line':2,'exclusion_reasons':['doubtful_sign'],
     'tokens':[{'sign':'M051','slot':1,'doubtful':False},{'sign':'M051','slot':3,'doubtful':True}]}
  out=lookup({'base_id':'M051','citation_raw':'2918','citation_uncertain':False},{'2918':[r]})
  self.assertEqual(out['status'],'multiple_base_occurrences');self.assertFalse(out['automatic_assignment'])
  self.assertTrue(out['candidates'][1]['doubtful']);self.assertEqual(out['candidates'][1]['slot'],3)
 def test_literal_suffix_and_missing_base(self):
  f={'base_id':'M051','citation_raw':'2918(?)','citation_uncertain':False}
  out=lookup(f,{});self.assertEqual(out['status'],'unresolved_suffix');self.assertEqual(out['suffix_raw'],'(?)')
  f['citation_raw']='2918';self.assertEqual(lookup(f,{})['status'],'missing_text')
  self.assertEqual(lookup(f,{'2918':[{'tokens':[]}]})['status'],'base_absent')

if __name__=='__main__':unittest.main()
