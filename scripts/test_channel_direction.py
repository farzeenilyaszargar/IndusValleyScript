import unittest
from channel_direction import oriented_parts,select,baseline_rows,bootstrap
from homophonic_channel import Channel

class DirectionTests(unittest.TestCase):
 def test_reversal_preserves_row_partition_and_unknown_slots(self):
  parts=[[[0,1,9],[9]],[[4,9,5]],[[6,7]]]
  rev=oriented_parts(parts,True)
  self.assertEqual(rev,[[[9,1,0],[9]],[[5,9,4]],[[7,6]]])
  self.assertEqual(oriented_parts(rev,True),parts);self.assertEqual(parts[0][0],[0,1,9])
 def test_selector_uses_validation_and_declared_ties_only(self):
  candidates=[{'direction_index':0,'start_index':0,'validation_bits':2.,'test_bits':900.},
              {'direction_index':1,'start_index':0,'validation_bits':2.,'test_bits':0.},
              {'direction_index':1,'start_index':1,'validation_bits':1.,'test_bits':1000.}]
  self.assertEqual(select(candidates),2);self.assertEqual(select(candidates[:2]),0)
 def test_source_unigram_reversal_and_grouped_gain(self):
  parts=[[[0,1,0,2],[1,0]],[[0,2]],[[0,1,2]]];u=[1.,2.,3.];b=[[1.]*3 for _ in range(3)]
  a=Channel(parts[0],2,u,b);rev=oriented_parts(parts,True);z=Channel(rev[0],2,u,b)
  self.assertAlmostEqual(baseline_rows(a,parts[2])[0]['unigram_total_bits'],baseline_rows(z,rev[2])[0]['unigram_total_bits'])
  r=bootstrap([{'component':7,'tokens':2,'channel_total_bits':2.,'unigram_total_bits':6.},
               {'component':7,'tokens':3,'channel_total_bits':3.,'unigram_total_bits':9.}], 'unigram_total_bits',100)
  self.assertEqual(len(r['groups']),1);self.assertEqual(r['percentile95'],[2.,2.])

if __name__=='__main__':unittest.main()
