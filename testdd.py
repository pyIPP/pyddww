import dd
import unittest

class testdd(unittest.TestCase):
    def test_init(self):
        sf = dd.shotfile('DCN', 30336, 'AUGD', 0)
        self.assertTrue(sf.status)
        del sf

    def test_open(self):
        sf = dd.shotfile()
        sf.open('DCN', 30336)
        self.assertTrue(sf.status)
        del sf

    def test_close(self):
        sf = dd.shotfile()
        sf.open('DCN', 30336)
        self.assertTrue(sf.status)
        sf.close()
        self.assertFalse(sf.status)
        del sf

if __name__=='__main__':
    unittest.main()


