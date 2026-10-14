import unittest
from catalogue_correspondence import pair_records,grouped_split,aligned,fit,evaluate
from analyze import canonical

class CorrespondenceTests(unittest.TestCase):
    def test_strict_pair_rejects_ambiguity_and_length_disagreement(self):
        p={'id':'M-1A','signs':['P001'],'allographs':[],'exclusion_reasons':[]}
        x={'site':'Mohenjo-daro','cisi':'M-1','id':'1.1','signs':['001'],'exclusion_reasons':[]}
        self.assertEqual(len(pair_records([p],[x])[0]),1)
        self.assertEqual(pair_records([p],[x,x])[1][0]['reason'],'ambiguous_object_rows')
        self.assertEqual(pair_records([p],[dict(x,signs=['001','002'])])[1][0]['reason'],'unequal_lengths')

    def test_alignment_does_not_mutate_source(self):
        p={'icit_signs':['001','002'],'parpola_signs':['P003','P004']}
        self.assertEqual(aligned(p,'reversed'),[('002','P003'),('001','P004')])
        self.assertEqual(p['icit_signs'],['001','002'])

    def test_both_catalogue_identities_share_partitions(self):
        ps=[{'object':str(i),'icit_signs':[str(i),str(i+1)],'parpola_signs':[f'P{i}',f'P{i+1}']} for i in range(50)]
        ps.append(dict(ps[0],object='copy',parpola_signs=['different','pair']))
        parts,_=grouped_split(ps)
        for namespace in ('icit_signs','parpola_signs'):
            sets=[{canonical(p[namespace]) for p in part} for part in parts]
            for i in range(3):
                for j in range(i):self.assertFalse(sets[i]&sets[j])

    def test_unknown_ids_count_as_failures(self):
        p={'object':'train','icit_signs':['001'],'parpola_signs':['P001']}
        counts,_=fit([p],'direct');test=dict(p,object='test',icit_signs=['unknown'])
        result=evaluate([test],'direct',counts)
        self.assertEqual(result['top1_rate_all_positions'],0);self.assertEqual(result['known_coverage'],0)

if __name__=='__main__':unittest.main()
