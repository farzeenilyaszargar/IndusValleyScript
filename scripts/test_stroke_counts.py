import collections
import random
import unittest
from stroke_counts import mutual_information,permuted,COUNTS

class StrokeTests(unittest.TestCase):
    def test_information_independence_and_perfect_dependency(self):
        independent=[{'stroke_count':n,'follower':s} for n in (1,2) for s in ('a','b')]
        dependent=[{'stroke_count':1,'follower':'a'},{'stroke_count':2,'follower':'b'}]
        self.assertAlmostEqual(mutual_information(independent),0)
        self.assertAlmostEqual(mutual_information(dependent),1)

    def test_permutation_preserves_strata_marginals_and_followers(self):
        es=[{'stroke_count':n,'follower':str(i),'height':h,'position_role':p} for i,(n,h,p) in enumerate([
            (1,'short','initial'),(2,'short','initial'),(3,'short','medial'),(4,'short','medial'),(1,'tall','medial')])]
        out=permuted(es,random.Random(17))
        self.assertEqual([e['follower'] for e in es],[e['follower'] for e in out])
        for h,p in {(e['height'],e['position_role']) for e in es}:
            marginal=lambda xs:collections.Counter(e['stroke_count'] for e in xs if (e['height'],e['position_role'])==(h,p))
            self.assertEqual(marginal(es),marginal(out))

    def test_short_and_tall_counts_remain_distinct(self):
        self.assertEqual(COUNTS['P123'],('short',3));self.assertEqual(COUNTS['P147'],('tall',3))
        self.assertNotIn('P143',COUNTS)  # decorated multi-row count not guessed

if __name__=='__main__':unittest.main()
