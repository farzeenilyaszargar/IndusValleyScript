import itertools
import unittest
from analyze import Model
from gap_reconstruction import Reconstructor

class GapTests(unittest.TestCase):
    def test_exact_enumeration(self):
        m=Model([['a','b'],['a','c'],['b','c'],['a','b','c']],2,5)
        r=Reconstructor(m)
        for n in (1,2):
            scores=[]
            for t in itertools.product(('a','b','c'),repeat=n):
                prefix=['<BOS>'];weight=1
                for s in t+('<EOS>',):weight*=m.prob(s,prefix);prefix.append(s)
                scores.append((weight,t))
            total=sum(w for w,_ in scores)
            expected=sorted(scores,key=lambda x:(-x[0],x[1]))
            actual=r.fill('<BOS>','<EOS>',n,k=20)
            self.assertEqual([tuple(x['signs']) for x in actual],[t for _,t in expected])
            for row,(w,_) in zip(actual,expected):self.assertAlmostEqual(row['probability'],w/total)
            self.assertAlmostEqual(sum(x['probability'] for x in actual),1)
    def test_boundaries_unknown_and_rejection(self):
        r=Reconstructor(Model([['a','b'],['b']],2,5))
        self.assertEqual(r.fill('unseen','unseen',2),r.fill('<UNK>','<UNK>',2))
        self.assertTrue(all(set(x['signs'])<= {'a','b'} for x in r.fill('<BOS>','<EOS>',2)))
        with self.assertRaises(ValueError):r.fill('a','b',3)
    def test_unigram_context_invariance(self):
        r=Reconstructor(Model([['a','b'],['b','b']],1,5))
        a=r.fill('<BOS>','<EOS>',2);b=r.fill('b','a',2)
        self.assertEqual([x['signs'] for x in a],[x['signs'] for x in b])
        for x,y in zip(a,b):self.assertAlmostEqual(x['probability'],y['probability'])

if __name__=='__main__':unittest.main()
