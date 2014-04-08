import dd
import unittest
import numpy

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

    def test_tb_calib(self):
# a=Integer TB in [ns], b="calibrated" in float,[s]
        sf = dd.shotfile()
        sf.open('MSX', 28053)
#        a = sf.getTimeBase('TIME-AD0',dtype=numpy.int64)
# Gives segmentation fault
        b = sf.getTimeBase('TIME-AD0',dtype=numpy.float32)
        sf.close()
        self.assertFalse(sf.status)
        del sf
#        print a
        print b

    def test_sig_calib(self):
        sf = dd.shotfile()
        sf.open('DCN', 28053)
        a = sf.getSignal('H-1')
        b = sf.getSignalCalibrated('H-1')
        sf.close()
        self.assertFalse(sf.status)
        del sf
        print a
        print b

    def test_char_sgr(self):
        sf = dd.shotfile()
        sf.open('EQI', 28053)
        a = sf.getSignalGroup('SSQnam')
        sf.close()
        self.assertFalse(sf.status)
        del sf
        print a

    def test_int_sgr_noTB(self):
        sf = dd.shotfile()
        sf.open('CFR', 30407)
        a = sf.getSignalGroup('CCD_DATA')
        sf.close()
        self.assertFalse(sf.status)
        del sf

    def test_lastshot(self):
        a = dd.getLastShotNumber('LBO',pulseNumber=30435)
        b = dd.getLastShotNumber('LBO',pulseNumber=30436)
        print('%d %d' %(a,b))

if __name__=='__main__':
    unittest.main()


