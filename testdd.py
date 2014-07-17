import dd
import unittest
import numpy
from IPython import embed

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

    def test_getSignal(self):
        sf = dd.shotfile()
        sf.open('DCN', 29708)
        self.assertEqual(sf('H-1', tBegin=0, tEnd=0).data[0], numpy.float32(4.1904756e+17))
        self.assertEqual(sf.getSignal('H-1').dtype, numpy.int16)
        self.assertEqual(sf.getSignal('H-1', dtype=numpy.float32).dtype, numpy.float32)
        self.assertEqual(sf.getSignal('H-1', dtype=numpy.float64).dtype, numpy.float64)
        self.assertEqual(sf.getSignal('H-1').size, 100000)
        self.assertEqual(sf.getSignal('H-1', dtype=numpy.float32).size, 100000)
        self.assertEqual(sf.getSignal('H-1', dtype=numpy.float64).size, 100000)
        del sf

    def test_getSignalCalibrated(self):
        sf = dd.shotfile()
        sf.open('DCN', 29708)
        data, unit = sf.getSignalCalibrated('H-1')
        self.assertEqual(data.dtype, numpy.float32)
        self.assertEqual(data.size, 100000)
        self.assertEqual(unit, '1/m^3')
        data, unit = sf.getSignalCalibrated('H-1', dtype=numpy.float32)
        self.assertEqual(data.dtype, numpy.float32)
        self.assertEqual(data.size, 100000)
        self.assertEqual(unit, '1/m^3')
        data, unit = sf.getSignalCalibrated('H-1', dtype=numpy.float64)
        self.assertEqual(data.dtype, numpy.float64)
        self.assertEqual(data.size, 100000)
        self.assertEqual(unit, '1/m^3')
        del sf

    def test_tb_calib(self):
# a=Integer TB in [ns], b="calibrated" in float,[s]
        sf = dd.shotfile()
        sf.open('MSX', 28053)
# Gives segmentation fault
        b = sf.getTimeBase('TIME-AD0',dtype=numpy.float32)
        sf.close()
        self.assertFalse(sf.status)
        del sf
        tol = 1e-5
        self.assertTrue(numpy.abs(b[0] + 0.6550321) < tol)
        self.assertTrue(numpy.abs(b[-1] -11.34496403) < tol)

    def test_sig_calib(self):
        sf = dd.shotfile()
        sf.open('DCN', 28053)
        a = sf.getSignal('H-1')
        b = sf.getSignalCalibrated('H-1')
        sf.close()
        self.assertFalse(sf.status)
        del sf
        tol = 1e-5
        self.assertTrue(numpy.abs(a[0] + 1) < tol)
        self.assertTrue(numpy.abs(a[-1] -11) < tol)
        tol *= 1e17
        self.assertTrue(numpy.abs(b[0][0] - 1.39682516e+17) < tol)
        self.assertTrue(numpy.abs(b[0][-1] + 1.53650771e+18) < tol)

    def test_char_sgr(self):
        sf = dd.shotfile()
        sf.open('EQI', 28053)
        a = sf.getSignalGroup('SSQnam')
        sf.close()
        self.assertFalse(sf.status)
        del sf
        mystr = "".join(a[0]).strip()
        self.assertEqual(mystr,'Rsquad')

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
        self.assertEqual(a, 30434)
        self.assertEqual(b, 30436)

    def test_getrelations(self):
        sf = dd.shotfile()
        sf.open('CEZ', 30407)
        rel = sf.getRelations('Ti')
        sf.close()
        self.assertFalse(sf.status)
        del sf
        self.assertEqual(rel.txt[0],'time')
        self.assertEqual(rel.txt[1],'R_time')

    def test_getInfo(self):
        sf = dd.shotfile()
        sf.open('CEC', 30133)
        info = sf.getInfo('Trad-A')
        sf.close()
        self.assertFalse(sf.status)
        del sf
        self.assertEqual(dd.__obj__[info.objtyp], 'Sig_Group')
        self.assertEqual(info.level, 1)
        self.assertEqual(info.status, 0)
        self.assertEqual(info.error, 0)
        self.assertEqual(info.bytlen,62914560)
        self.assertEqual(dd.__dataformat__[info.fmt], numpy.float32)
        self.assertEqual(info.units, 'eV')
        self.assertEqual(info.ind[0], 114685)
        self.assertEqual(info.ind[1], 60)
        self.assertEqual(info.ind[2], 1)
        self.assertEqual(info.ind[3], 1)
        self.assertEqual(info.rels,['time-A', 'parms-A'])

    def test_getParameter(self):
        sf = dd.shotfile()
        sf.open('NIS', 30133)
        tol = 1e-4
        spec1 = sf.getParameter('INJ1','SPEC')
        self.assertTrue(numpy.abs(spec1.data[0] - 20.214462) < tol)
        sf.open('TTH', 30133)
        law = sf.getParameter('scal_par','descript')
        self.assertEqual(law.data[0].rstrip(), 'ITERL-89P(tot), Wtot/Ptot')

if __name__=='__main__':
    unittest.main()
