"""Checks for leakage, probability normalization and damaged-sign handling."""
import collections
import math
import unittest
from analyze import Model, canonical, conditional_entropy, shuffled, split
from normalize import icit_parse
from extended import SlotModel
from reproduce import equivalent
import random

class PipelineTests(unittest.TestCase):
    def test_cross_platform_comparison_rejects_material_drift(self):
        equivalent({'ids':['a'],'n':2,'p':0.5},{'ids':['a'],'n':2,'p':0.5+1e-14})
        for changed in ({'ids':['b'],'n':2,'p':0.5},{'ids':['a'],'n':3,'p':0.5},
                        {'ids':['a'],'n':2,'p':0.51}):
            with self.assertRaises(ValueError):equivalent({'ids':['a'],'n':2,'p':0.5},changed)

    def test_damaged_and_multiline_rejected(self):
        for text in ('+740-000+',']740-033+','+740/033+','+740-999+'):
            self.assertTrue(icit_parse({'text':text})[1])
        self.assertEqual(icit_parse({'text':'+740-033+'}),(['740','033'],[]))

    def test_split_excludes_exact_and_reverse_leakage(self):
        texts=[[str(i),str(i+1)] for i in range(100)]
        texts+=texts+list(map(lambda t:list(reversed(t)),texts))
        sets=[{canonical(t) for t in part} for part in split(texts,42)]
        for i in range(3):
            for j in range(i):self.assertFalse(sets[i]&sets[j])

    def test_probability_mass(self):
        for order in (1,2,3):
            m=Model([['a','b'],['a','c'],['b']],order)
            for context in (['<BOS>','<BOS>'],['a','b'],['unseen','unseen']):
                self.assertAlmostEqual(sum(m.prob(s,context) for s in m.vocab),1)
        s=SlotModel([['a','b'],['b']])
        for i,n in ((0,2),(1,2),(0,1),(1,3)):
            self.assertAlmostEqual(sum(s.prob(x,i,n) for x in s.base.vocab if x!='<EOS>'),1)

    def test_shuffles_preserve_required_marginals(self):
        ts=[['a','b'],['c','d'],['a','d','e'],['b','c','f']]
        for kind in ('within_text','global_frequency','length_position'):
            out=shuffled(ts,kind,random.Random(42))
            self.assertEqual(list(map(len,ts)),list(map(len,out)))
            self.assertEqual(collections.Counter(x for t in ts for x in t),collections.Counter(x for t in out for x in t))
            if kind=='length_position':
                for n in (2,3):
                    for i in range(n):
                        self.assertEqual(collections.Counter(t[i] for t in ts if len(t)==n),collections.Counter(t[i] for t in out if len(t)==n))

    def test_relabel_invariant(self):
        ts=[['a','b','a'],['a','c']]
        self.assertAlmostEqual(conditional_entropy(ts),conditional_entropy([[{'a':'x','b':'y','c':'z'}[s] for s in t] for t in ts]))

if __name__=='__main__':unittest.main()
