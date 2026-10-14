import unittest
from language_compare import words,clusters,conllu_documents,sample_windows

class LanguageCompareTests(unittest.TestCase):
    def test_canonical_letter_marks_and_tamil_spacing_marks(self):
        self.assertEqual(words('PŪRVA, pu\u0304rva!'),['pūrva','pūrva'])
        self.assertEqual(clusters(['pu\u0304rva']),['p','ū','r','v','a'])
        self.assertEqual(clusters(words('கா க்')),['கா','க்'])
        self.assertEqual(words('க\u200cா'),['கா'])

    def test_conllu_excludes_ranges_empty_nodes_and_punctuation(self):
        raw='# sent_id = example\n1-2\tab\t_\t_\t_\t_\t_\t_\t_\t_\n1\ta\t_\tNOUN\t_\t_\t0\troot\t_\t_\n2\tb\t_\tNOUN\t_\t_\t1\tdep\t_\t_\n2.1\tx\t_\tNOUN\t_\t_\t_\t_\t_\t_\n3\t.\t_\tPUNCT\t_\t_\t1\tpunct\t_\t_\n'
        d=conllu_documents(raw,'test')
        self.assertEqual(d[0]['words'],['a','b']);self.assertEqual(d[0]['id'],'example')

    def test_windows_exact_lengths_no_document_crossing(self):
        docs=[{'tokens':[1,2,3]},{'tokens':[8,9]}]
        texts,windows=sample_windows(docs,[1,2,3,2],17)
        self.assertEqual(list(map(len,texts)),[1,2,3,2])
        for t,w in zip(texts,windows):
            self.assertEqual(t,docs[w['document_index']]['tokens'][w['offset']:w['offset']+len(t)])
        self.assertEqual((texts,windows),sample_windows(docs,[1,2,3,2],17))

if __name__=='__main__':unittest.main()
