import unittest
from full_target_audit import coarsen_counts,make_cipher,UNK

class FullTargetTests(unittest.TestCase):
 def test_coarse_counts_keep_unknown_slots_and_edges(self):
  p={'units':['a','b','c'],'unigram_counts':[2,3,4,0],
     'bigram_counts':[[1,2,3,0],[4,5,6,0],[7,8,9,0],[0,0,0,0]]}
  u,b=coarsen_counts(p,['a']);self.assertEqual(u,[2,7]);self.assertEqual(b,[[1,5],[11,28]])
 def test_known_alias_cipher_round_trip_and_unknown_positions(self):
  source=[[0,1,2,3],[2,1,0]];cipher,truth=make_cipher(source,3)
  self.assertEqual([[truth[s] if s!=UNK else 3 for s in row] for row in cipher],source)
  self.assertEqual(len(truth),6);self.assertEqual(cipher[0][3],UNK)
 def test_same_seed_preserves_all_lengths_and_determinism(self):
  source=[[i%5 for i in range(n)] for n in range(1,15)]
  a,_=make_cipher(source,5);b,_=make_cipher(source,5)
  self.assertEqual(a,b);self.assertEqual(list(map(len,a)),list(map(len,source)))

if __name__=='__main__':unittest.main()
