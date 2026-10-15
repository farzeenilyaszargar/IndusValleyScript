import unittest
from fish_rebus_audit import extract_events

class FishAuditTests(unittest.TestCase):
    def test_explicit_stored_order_and_no_artifact_crossing(self):
        rows=[{'id':'a','cisi':'H-9','signs':['220','017']},
              {'id':'b','cisi':'x','signs':['017','220']},
              {'id':'c','cisi':'x','signs':['220']},{'id':'d','cisi':'x','signs':['017']}]
        events=extract_events(rows,{'017':7})
        self.assertEqual([(e['row_id'],e['head_id'],e['described_count']) for e in events],[('a','220',7)])
        self.assertEqual(extract_events(rows,{'017':7},True)[0]['row_id'],'b')

    def test_adjacent_strokes_not_mislabeled_as_heads(self):
        rows=[{'id':'a','cisi':'x','signs':['220','006','017']}]
        es=extract_events(rows,{'006':6,'017':7});self.assertEqual(len(es),1)
        self.assertEqual(es[0]['stroke_id'],'006')

if __name__=='__main__':unittest.main()
