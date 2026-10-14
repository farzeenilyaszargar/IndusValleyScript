import unittest
from metadata_models import MetadataModel,coarse_type,partition
from analyze import canonical

class MetadataTests(unittest.TestCase):
    def rows(self):return [{'id':str(i),'signs':[str(i),str(i+1)],'site':'S','type':'SEAL:S'} for i in range(50)]

    def test_type_prefix_is_literal_not_interpretation(self):
        self.assertEqual(coarse_type({'type':'TAB:B'}),'TAB')
        self.assertEqual(coarse_type({'type':''}),'<MISSING>')

    def test_mass_and_unseen_metadata_backoff(self):
        m=MetadataModel(self.rows(),'site_type',5,20);row=self.rows()[0]
        self.assertAlmostEqual(sum(m.prob(s,'<BOS>',row) for s in m.base.vocab),1)
        unknown=dict(row,site='unseen')
        for s in m.base.vocab:self.assertAlmostEqual(m.prob(s,'<BOS>',unknown),m.base.prob(s,['<BOS>']))

    def test_duplicate_and_reverse_texts_keep_metadata_together(self):
        rows=self.rows();rows.extend([dict(rows[0],id='copy',type='TAB:B'),
                                     dict(rows[0],id='reverse',signs=rows[0]['signs'][::-1],site='other')])
        parts=partition(rows);sets=[{canonical(r['signs']) for r in p} for p in parts]
        for i in range(3):
            for j in range(i):self.assertFalse(sets[i]&sets[j])

if __name__=='__main__':unittest.main()
