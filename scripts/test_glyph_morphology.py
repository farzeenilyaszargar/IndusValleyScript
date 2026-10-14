"""Optional Pillow checks for independent synthetic masks."""
import unittest
from PIL import Image,ImageDraw
from glyph_morphology import components,descriptors

class GlyphTests(unittest.TestCase):
    def test_eight_connected_components(self):
        self.assertEqual(components({(0,0),(1,1),(9,9)}),[2,1])

    def test_component_counts_and_translation_invariance(self):
        a=Image.new('L',(20,20),255);d=ImageDraw.Draw(a)
        d.rectangle((2,2,3,12),fill=0);d.rectangle((8,2,9,12),fill=0)
        b=Image.new('L',(30,30),255);b.paste(a,(5,7))
        x,y=descriptors(a),descriptors(b)
        self.assertEqual(x['connected_components_8'],2)
        for key in ('bbox_aspect','bbox_ink_fraction','centroid_x','centroid_y','second_moment_xx','second_moment_yy'):
            self.assertAlmostEqual(x[key],y[key])

if __name__=='__main__':unittest.main()
