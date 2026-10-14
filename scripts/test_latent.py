"""Independent small-model checks against exhaustive hidden-state enumeration."""
import itertools
import math
import unittest
from latent_grammar import HMM
from near_copy import components

class LatentTests(unittest.TestCase):
    def model(self):
        m=HMM([['a','b'],['b']],2,17)
        m.start=[.6,.4];m.stop=[.2,.3];m.transition=[[.5,.3],[.2,.5]]
        m.emission=[[.1,.7,.2],[.2,.2,.6]]  # sorted vocab UNK,a,b
        return m

    def test_forward_and_posteriors_against_enumeration(self):
        m=self.model();x=m.encode(['a','b','a']);paths=[]
        for states in itertools.product(range(m.k),repeat=len(x)):
            p=m.start[states[0]]*m.emission[states[0]][x[0]]
            for pos in range(1,len(x)):
                p*=m.transition[states[pos-1]][states[pos]]*m.emission[states[pos]][x[pos]]
            p*=m.stop[states[-1]];paths.append((states,p))
        total=sum(p for _,p in paths)
        gamma,xi,loss=m.posterior(x)
        self.assertAlmostEqual(2**(-loss),total)
        for pos,row in enumerate(gamma):
            for j,actual in enumerate(row):
                expected=sum(p for states,p in paths if states[pos]==j)/total
                self.assertAlmostEqual(actual,expected)
        for pos,matrix in enumerate(xi):
            for i in range(m.k):
                for j in range(m.k):
                    expected=sum(p for states,p in paths if states[pos:pos+2]==(i,j))/total
                    self.assertAlmostEqual(matrix[i][j],expected)

    def test_stop_and_emissions_mass_after_em(self):
        m=self.model();m.step([['a','b'],['b'],['a','a','b']])
        self.assertAlmostEqual(sum(m.start),1)
        for i in range(m.k):
            self.assertAlmostEqual(sum(m.transition[i])+m.stop[i],1)
            self.assertAlmostEqual(sum(m.emission[i]),1)
            self.assertGreater(m.stop[i],0)

    def test_components_keep_mirrored_near_copies_together(self):
        texts=[['a','b','c'],['a','d','c'],['e','d','c'],['c','d','a'],['x','y'],['x','z']]
        gs=components(texts)
        self.assertIn([('a','b','c'),('a','d','c'),('c','d','e')],gs)
        self.assertIn([('x','y')],gs);self.assertIn([('x','z')],gs)

if __name__=='__main__':unittest.main()
