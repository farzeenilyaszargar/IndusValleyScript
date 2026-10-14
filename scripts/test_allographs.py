import unittest
from allographs import VariantHistory,partition,variant
from analyze import canonical

def record(name,gs):
    return {'id':name,'signs':[g['id'] for g in gs],'allographs':gs}

def glyph(sign,custom):return {'id':sign,'features':[0,1,0,custom]}

class AllographTests(unittest.TestCase):
    def test_variant_excludes_layout_and_confidence(self):
        g=glyph('P050',2);other={'id':'P050','features':[5,4,90,2]}
        self.assertEqual(variant(g),variant(other))
        self.assertNotEqual(variant(g),variant(glyph('P050',3)))

    def test_variant_probabilities_normalize_and_unseen_history_backs_off(self):
        rows=[record('a',[glyph('P050',1),glyph('P144',1)]),record('b',[glyph('P050',2)])]
        m=VariantHistory(rows,5,20)
        for bp,vp in (('<BOS>','<BOS>'),('P050','P050:1'),('P050','unseen')):
            self.assertAlmostEqual(sum(m.prob(s,bp,vp) for s in m.base.vocab),1)
        for s in m.base.vocab:self.assertAlmostEqual(m.prob(s,'P050','unseen'),m.base.prob(s,['P050']))

    def test_base_duplicate_variants_share_split(self):
        rows=[record(str(i),[glyph(f'P{i:03}',1),glyph(f'P{i+1:03}',2)]) for i in range(50)]
        rows.append(record('duplicate',[glyph('P000',9),glyph('P001',9)]))
        parts=partition(rows,42);sets=[{canonical(r['signs']) for r in p} for p in parts]
        for i in range(3):
            for j in range(i):self.assertFalse(sets[i]&sets[j])

    def test_target_morphology_does_not_change_its_own_prediction(self):
        m=VariantHistory([record('train',[glyph('P050',1)])],5,20)
        a=record('test',[glyph('P050',1)]);b=record('test',[glyph('P050',9)])
        # First-token prediction is independent of the target's own variant.
        self.assertEqual(m.prob(a['signs'][0],'<BOS>','<BOS>'),m.prob(b['signs'][0],'<BOS>','<BOS>'))

if __name__=='__main__':unittest.main()
