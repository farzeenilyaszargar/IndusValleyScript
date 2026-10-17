import unittest
from novel_pattern_substitution import retain_novel,interval

class NovelPatternsTests(unittest.TestCase):
 def test_reversed_collisions_removed_without_changing_train(self):
  parts=[[[0,32,1]],[[1,32,0],[2,32,3]],[[3,32,2],[4,32,5],[5,32,4],[1,32,0]]]
  kept,reasons=retain_novel(parts)
  self.assertEqual(kept,[[0],[1],[1,2]])
  self.assertEqual(reasons[2],['validation_pattern','retained','retained','training_pattern'])
 def test_unknown_slots_and_full_lengths_define_patterns(self):
  parts=[[[0,32,1]],[[0,1]],[[0,32,32,1]]]
  self.assertEqual(retain_novel(parts)[0],[[0],[0],[0]])
  self.assertEqual(parts[2][0],[0,32,32,1])
 def test_bootstrap_uses_total_bits_and_tokens(self):
  rows=[{'encoded':[0,1],'baseline_total_bits':6.,'selected_total_bits':2.,'tokens':2},
        {'encoded':[1,0],'baseline_total_bits':6.,'selected_total_bits':2.,'tokens':2},
        {'encoded':[3],'baseline_total_bits':3.,'selected_total_bits':1.,'tokens':1}]
  r=interval(rows,trials=100)
  self.assertEqual(r['groups'],2);self.assertEqual(r['gain_bits_per_token'],2.)
  self.assertEqual(r['percentile95'],[2.,2.])

if __name__=='__main__':unittest.main()
