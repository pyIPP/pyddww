import numpy
import ctypes
import os

__libddww__ = ctypes.cdll.LoadLibrary('/afs/ipp-garching.mpg.de/aug/ads/lib64/' + os.environ['SYS'] + '/libddww8.so')

def GetError(error):
    try:
        err = ctypes.c_int32(error)
    except TypeError:
        err = ctypes.c_int32(error.value)
    isError = __libddww__.xxsev_(ctypes.byref(err))==1
    isWarning = __libddww__.xxwarn_(ctypes.byref(err))==1
    if isError or isWarning:
        id = ctypes.c_char_p(b'')
        lid = ctypes.c_uint64(0)
        text = ctypes.c_char_p(b' '*255)
        ltext = ctypes.c_uint64(255)
        unit = ctypes.byref(ctypes.c_int32(-1))
        ctrl = ctypes.byref(ctypes.c_uint32(3))
        __libddww__.xxerrprt_(unit, text, ctypes.byref(err), ctrl, id, ltext, lid);
        if isError:
            raise Exception(text.value.strip())
        else:
            raise Warning(text.value.strip())

def GetLastAUGShotNumber():
    error = ctypes.c_int32(0)
    pulseNumber = ctypes.c_uint32(0)
    __libddww__.ddlastshotnr_(ctypes.byref(error), ctypes.byref(pulseNumber))
    GetError(error)
    return numpy.uint32(pulseNumber.value)

def GetLastShotNumber(Experiment, Diagnostic, PulseNumber=None):
    if PulseNumber==None:
        PulseNumber = GetLastAUGShotNumber()
    try:
        exper = ctypes.c_char_p(Experiment)
    except TypeError:
        exper = ctypes.c_char_p(Experiment.encode())
    lexper = ctypes.c_uint64(len(Experiment))
    try:
        diag = ctypes.c_char_p(Diagnostic)
    except TypeError:
        diag = ctypes.c_char_p(Diagnostic.encode())
    ldiag = ctypes.c_uint64(len(Diagnostic))
    shot = ctypes.c_uint32(PulseNumber)
    cshot = ctypes.c_uint32(0)
    __libddww__.ddcshotnr_(exper, diag, ctypes.byref(shot), ctypes.byref(cshot), lexper, ldiag)
    return numpy.uint32(cshot.value)

def GetPhysicalDimension(Unit):
    try:
        physunit = ctypes.c_int32(Unit)
    except TypeError:
        physunit = ctypes.c_int32(Unit.value)
    error = ctypes.c_int32(0)
    output = b' '*256
    physdim = ctypes.c_char_p(output)
    lphysdim = ctypes.c_uint64(256)
    __libddww__.dddim_(ctypes.byref(error), ctypes.byref(physunit), physdim, lphysdim)
    GetError(error)
    return output.replace('\x00','').strip()


class Shotfile(object):
    def __init__(self, Experiment=None, Diagnostic=None, PulseNumber=None, Edition=0):
        self.diaref = ctypes.c_int32(0)
        if Experiment!=None and Diagnostic!=None and PulseNumber!=None:
            self.Open(Experiment, Diagnostic, PulseNumber, Edition)

    def __del__(self):
        self.Close()

    def status():
        def fget(self):
            return self.diaref.value!=0
        return locals()
    status = property(**status())

    def Open(self, Experiment, Diagnostic, PulseNumber, Edition=0):
        self.Close()
        error = ctypes.c_int32(0)
        edit = ctypes.byref(ctypes.c_int32(Edition))
        cshot = ctypes.byref(ctypes.c_uint32(0))
        shot = ctypes.byref(ctypes.c_uint32(PulseNumber))
        try:
            diag = ctypes.c_char_p(Diagnostic)
        except TypeError:
            diag = ctypes.c_char_p(Diagnostic.encode())
        try:
            exper = ctypes.c_char_p(Experiment)
        except TypeError:
            exper = ctypes.c_char_p(Experiment.encode())
        lexp = ctypes.c_uint64(len(Experiment))
        ldiag = ctypes.c_uint64(len(Diagnostic))
        date = ctypes.c_char_p(b'123456789012345678')
        ldate = ctypes.c_uint64(18)
        result = __libddww__.ddcshotnr_(exper,diag,shot,cshot,lexp,ldiag)
        if result==0 and cshot._obj.value==PulseNumber:
            result = __libddww__.ddopen_(ctypes.byref(error),exper,diag,shot,edit,ctypes.byref(self.diaref),date,lexp,ldiag,ldate)
        GetError(error)

    def Close(self):
        if self.status:
            error = ctypes.c_int32(0)
            result = __libddww__.ddclose_(ctypes.byref(error), ctypes.byref(self.diaref))
            GetError(error)    
            self.diaref.value = 0
