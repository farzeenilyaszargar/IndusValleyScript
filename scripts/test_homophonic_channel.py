import unittest
from homophonic_channel import Channel,K,prepare

class HomophonicTests(unittest.TestCase):
 def model(self):
  texts=[list(range(K))+[0,0,1,1,0,32,0], [32,1,0]];uni=[1.+i/20 for i in range(K+1)];bi=[[1.+abs(i-j)/13 for j in range(K+1)] for i in range(K+1)]
  return Channel(texts,K+1,uni,bi),texts
 def test_sparse_move_and_swap_deltas_match_full_score(self):
  m,_=self.model();key=list(range(K))+[0,K];f,s=m.groups(key)
  for changes in ({32:1},{0:1},{0:1,1:0},{32:2,2:0}):
   d=m.delta(key,f,s,changes);other=key.copy()
   for i,g in changes.items():other[i]=g
   self.assertAlmostEqual(d,m.objective(other)-m.objective(key),places=7)
   changed=key.copy();cf=f.copy();cs=s.copy();m.apply(changed,cf,cs,changes)
   self.assertEqual(changed,other);self.assertEqual((cf,cs),m.groups(other))
  self.assertIsNone(m.delta(key,f,s,{2:3}))
 def test_emission_and_initial_edge_scores_normalize(self):
  m,texts=self.model();key=list(range(K))+[0,K];f,size=m.groups(key)
  for g in range(K):self.assertAlmostEqual(sum(m.weights[i]/(f[g]+.5*size[g]) for i in range(m.n) if key[i]==g),1.)
  self.assertAlmostEqual(sum(r['total_bits'] for r in m.losses(texts,key)),m.objective(key),places=9)
  self.assertEqual(m.losses([[m.n]],key)[0]['emission_bits'],0.)
 def test_similarity_group_splits_preserve_all_tokens(self):
  texts=[[str(i),str(i+1),str(i+2),str(i+3)] for i in range(80)]+[['0','1','2','x']]
  parts,labels,original,meta=prepare(texts)
  self.assertEqual(sum(map(len,parts)),len(texts));self.assertEqual(sum(len(t) for p in parts for t in p),sum(map(len,texts)))
  seen=[{tuple(t) for t in p}|{tuple(reversed(t)) for t in p} for p in original]
  self.assertFalse(any(seen[i]&seen[j] for i in range(3) for j in range(i)))
  membership={tuple(t):p for p,rows in enumerate(original) for t in rows}
  self.assertEqual(membership[('0','1','2','3')],membership[('0','1','2','x')])

if __name__=='__main__':unittest.main()
