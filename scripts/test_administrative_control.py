import unittest
from administrative_control import generate,licenses,audit,templates

class ControlTests(unittest.TestCase):
    def test_lengths_determinism_and_role_contract(self):
        lengths=list(range(1,31))*3
        a=generate(lengths,17)
        self.assertEqual(a,generate(lengths,17))
        self.assertEqual([len(r['signs']) for r in a],lengths)
        self.assertNotEqual(a,generate(lengths,29))
        audit(a,licenses())
        self.assertTrue(all(set(t)=={'sign','role','value'} for r in a for t in r['semantics']))
    def test_template_lengths(self):
        for length in range(1,50):
            self.assertTrue(templates(length))
            for (i,o,l,t),weight in templates(length):
                self.assertEqual(i+2*o+2*l+t,length);self.assertGreater(weight,0)
    def test_semantic_corruption_is_detected(self):
        rows=generate([20],17)
        t=next(t for t in rows[0]['semantics'] if t['role']=='quantity');t['value']=999
        with self.assertRaises(AssertionError):audit(rows,licenses())

if __name__=='__main__':unittest.main()
