import unittest
from uncertainty_sensitivity import broader_eligible,eligible_additions

def row(i,signs,damage=0,uncertainty=0,reasons=None):
    return {'id':i,'signs':signs,'exclusion_reasons':reasons or [],
            'allographs':[{'id':s,'features':[damage,1,uncertainty]} for s in signs]}

class UncertaintyTests(unittest.TestCase):
    def test_unknown_and_multiline_not_promoted(self):
        self.assertTrue(broader_eligible(row('a',['P1'],reasons=['damage_or_uncertainty'])))
        for reason in ('unknown','multiline_or_empty','short_feature_vector'):
            self.assertFalse(broader_eligible(row('a',['P1'],reasons=[reason])))

    def test_holdout_objects_and_reverse_copies_never_added(self):
        test=[row('held',['P1','P2'])]
        rs=[test[0],row('copy',['P2','P1'],10,10,['damage_or_uncertainty']),row('new',['P3','P4'],20,20,['damage_or_uncertainty'])]
        self.assertEqual([r['id'] for r in eligible_additions(rs,[],test,25)],['new'])

    def test_literal_raw_code_limit_does_not_decode_location(self):
        r=row('x',['P1'],1410,10,['damage_or_uncertainty'])
        self.assertFalse(eligible_additions([r],[],[],25))
        self.assertEqual(len(eligible_additions([r],[],[],None)),1)

if __name__=='__main__':unittest.main()
