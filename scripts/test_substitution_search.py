import itertools
import unittest
from substitution_search import statistics,objective,swap_delta,optimize,rank_key

class SubstitutionTests(unittest.TestCase):
 def test_swap_delta_matches_full_objective(self):
  s=statistics([[0,1,2,3,0],[2,2,1],[3]],4);u=[1.,2.,3.,4.];b=[[float((i+1)*(j+2))/7 for j in range(4)] for i in range(4)]
  for p in itertools.permutations(range(3)):
   k=list(p)+[3]
   for a,bn in itertools.combinations(range(3),2):
    other=k.copy();other[a],other[bn]=other[bn],other[a]
    self.assertAlmostEqual(swap_delta(s,k,a,bn,u,b),objective(s,other,u,b)-objective(s,k,u,b),places=7)
 def test_unknown_slots_do_not_bridge_context(self):
  s=statistics([[0,3,1]],4);self.assertEqual(s['bi'][0][1],0);self.assertEqual(s['bi'][0][3],1);self.assertEqual(s['bi'][3][1],1)
 def test_search_preserves_bijection_and_fixed_unknown(self):
  s=statistics([[0,1,0,2],[0,1,0]],4);u=[1.,2.,3.,4.];b=[[float(abs(i-j)+1) for j in range(4)] for i in range(4)];start=[2,0,1,3]
  k=optimize(s,start,u,b,17,steps=100)
  self.assertEqual(sorted(k[:3]),[0,1,2]);self.assertEqual(k[3],3)
  self.assertLessEqual(objective(s,k,u,b),objective(s,start,u,b)+1e-6)
  self.assertEqual(rank_key([[2,2,1,3]],3)[3],3)

if __name__=='__main__':unittest.main()
