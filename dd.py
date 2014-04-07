import numpy
import ctypes
import os
import copy

__libddww__ = ctypes.cdll.LoadLibrary('/afs/ipp-garching.mpg.de/aug/ads/lib64/' + os.environ['SYS'] + '/libddww8.so')

__type__ = {numpy.int32:1, numpy.float32:2, numpy.float64:3, numpy.complex:4, numpy.bool:5, 
            numpy.byte:6, numpy.int64:10, numpy.int16:11, numpy.uint16:12, numpy.uint32:13, 
            numpy.uint64:14}

__fields__ = {'version': lambda: numpy.int32(0), 'level': lambda: numpy.int32(0), 'status': lambda: numpy.int32(0),
              'error': lambda: numpy.int32(0), 'relations': lambda: numpy.zeros(8, dtype=numpy.int32), 
              'address': lambda: numpy.int32(0), 'length': lambda: numpy.int32(0), 'objnr': lambda: numpy.int32(0), 
              'format': lambda: numpy.zeros(3, dtype=numpy.int32), 'dataformat': lambda: numpy.int32(0), 
              'objtype': lambda: numpy.int32(0), 'text': lambda: 64*b' ', 'size': lambda: numpy.int32(0), 
              'indices': lambda: numpy.zeros(3, dtype=numpy.int32), 'items': lambda: numpy.int32(0)}

__dataformat__ = {  1:numpy.uint8,
                    2:numpy.char,
                    3:numpy.int16,
                    4:numpy.int32,
                    5:numpy.float32,
                    6:numpy.float64,
                    7:numpy.bool,
                    9:numpy.uint16,
                    13:numpy.int64,
                    14:numpy.uint32,
                    15:numpy.uint64}

def getError(error):
    """ Check if an error/warning occured. """
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
            raise UserWarning(text.value.strip())

def getLastAUGShotNumber():
    """ Returns the current shotnumber of ASDEX Upgrade """
    error = ctypes.c_int32(0)
    pulseNumber = ctypes.c_uint32(0)
    __libddww__.ddlastshotnr_(ctypes.byref(error), ctypes.byref(pulseNumber))
    getError(error)
    return numpy.uint32(pulseNumber.value)

def getLastShotNumber(diagnostic, pulseNumber=None, experiment='AUGD'):
    """ Returns the highest available shotnumber of the specified diagnostic.
    If pulseNumber is specified, the search starts from there. """
    if pulseNumber==None:
        pulseNumber = getLastAUGShotNumber()
    try:
        exper = ctypes.c_char_p(experiment)
    except TypeError:
        exper = ctypes.c_char_p(experiment.encode())
    lexper = ctypes.c_uint64(len(experiment))
    try:
        diag = ctypes.c_char_p(diagnostic)
    except TypeError:
        diag = ctypes.c_char_p(diagnostic.encode())
    ldiag = ctypes.c_uint64(len(diagnostic))
    shot = ctypes.c_uint32(pulseNumber)
    cshot = ctypes.c_uint32(0)
    __libddww__.ddcshotnr_(exper, diag, ctypes.byref(shot), ctypes.byref(cshot), lexper, ldiag)
    return numpy.uint32(cshot.value)

def getPhysicalDimension(Unit):
    """ Returns human readable physical dimension of Unit. """
    try:
        physunit = ctypes.c_int32(Unit)
    except TypeError:
        physunit = ctypes.c_int32(Unit.value)
    error = ctypes.c_int32(0)
    output = b' '*256
    physdim = ctypes.c_char_p(output)
    lphysdim = ctypes.c_uint64(256)
    __libddww__.dddim_(ctypes.byref(error), ctypes.byref(physunit), physdim, lphysdim)
    getError(error)
    return output.replace('\x00','').strip()

class signalInfo(object):
    """ Class storing the general information of a Signal. """
    def __init__(self, name, type, index, timeBase):
        """ Constructor initializing the signalInfo object. """
        object.__init__(self)
        self.name = name
        self.type = type
        self.index = index
        self.timeBase = timeBase

    def nDim():
        doc = """ Number of dimension of the signal. """
        def fget(self):
            return numpy.size(filter(lambda i: self.index[i]>1, xrange(self.index.size)))
        return locals()
    nDim = property(**nDim())

    def size():
        doc = """ Number of total datapoints in the signal. """
        def fget(self):
            return self.index[:self.nDim].prod()
        return locals()
    size = property(**size())

class timeBaseInfo(object):
    """ Class storing the general information for a timebase. """
    def __init__(self, name,  ntVal, nPreTrig, tBegin, tEnd):
        """ Constructor initializing the timeBaseInfo object. """
        object.__init__(self)
        self.name = name
        self.ntVal = ntVal
        self.nPreTrig = nPreTrig
        self.tBegin = tBegin
        self.tEnd = tEnd    

class shotfile(object):
    """ Class to load the data from the shotfile. """
    def __init__(self, diagnostic=None, pulseNumber=None, experiment='AUGD', edition=0):
        """ Basic constructor. If a diagnostic is specified the shotfile is opened. """
        self.diaref = ctypes.c_int32(0)
        if diagnostic!=None and pulseNumber!=None:
            self.open(diagnostic, pulseNumber, experiment, edition)

    def __del__(self):
        """ Basic destructor closing the shotfile. """
        self.close()

    def status():
        doc = """ Status showing if shotfile is open. """
        def fget(self):
            return self.diaref.value!=0
        return locals()
    status = property(**status())

    def open(self, diagnostic, pulseNumber, experiment='AUGD', edition=0):
        """ Function opening the specified shotfile. """
        self.close()
        error = ctypes.c_int32(0)
        edit = ctypes.byref(ctypes.c_int32(edition))
        cshot = ctypes.byref(ctypes.c_uint32(0))
        shot = ctypes.byref(ctypes.c_uint32(pulseNumber))
        try:
            diag = ctypes.c_char_p(diagnostic)
        except TypeError:
            diag = ctypes.c_char_p(diagnostic.encode())
        try:
            exper = ctypes.c_char_p(experiment)
        except TypeError:
            exper = ctypes.c_char_p(experiment.encode())
        lexp = ctypes.c_uint64(len(experiment))
        ldiag = ctypes.c_uint64(len(diagnostic))
        date = ctypes.c_char_p(b'123456789012345678')
        ldate = ctypes.c_uint64(18)
        result = __libddww__.ddcshotnr_(exper,diag,shot,cshot,lexp,ldiag)
        if result==0 and cshot._obj.value==pulseNumber:
            result = __libddww__.ddopen_(ctypes.byref(error),exper,diag,shot,edit,ctypes.byref(self.diaref),
                                         date,lexp,ldiag,ldate)
        getError(error)

    def close(self):
        """ Close the shotfile. """
        if self.status:
            error = ctypes.c_int32(0)
            result = __libddww__.ddclose_(ctypes.byref(error), ctypes.byref(self.diaref))
            getError(error)    
            self.diaref.value = 0
               
    def getObjectName(self, objectNumber):
        """ Return name of object """
        if not self.status:
            raise Exception('ddww: Shotfile not open!')
        error = ctypes.c_int32(0)
        lname = ctypes.c_uint64(8)
        try:
            obj = ctypes.c_int32(objectNumber)
        except TypeError:
            obj = ctypes.c_int32(objectNumber.value)
        name = b' '*8
        __libddww__.ddobjname_(ctypes.byref(error), ctypes.byref(self.diaref), ctypes.byref(obj), 
                               ctypes.c_char_p(name), lname)
        getError(error)
        return name.replace('\x00','').strip()

    def getObjectNames(self):
        """ Return list of all object names in the shotfile. """
        if not self.status:
            raise Exception('ddww: Shotfile not open!')
        output = {}
        counter = 0
        while True:
            try:
                name = self.getObjectName(counter)
                output[counter] = name.encode()
                counter += 1  
            except Exception:
                return output

    def getSignalInfo(self, name):
        """ Returns a signalInfo object containing the information of the signal name """
        if not self.status:
            raise Exception('ddww::shotfile: Shotfile not open!')
        error = ctypes.c_int32(0)
        lsig = ctypes.c_uint64(len(name))
        typ = ctypes.c_int32(0)
        tname = b' '*8
        ltname = ctypes.c_uint64(len(tname))
        ind = numpy.zeros(4, dtype=numpy.uint32)
        try:
            sigName = ctypes.c_char_p(name)
        except TypeError:
            sigName = ctypes.c_char_p(name.encode())
        try:
            tName = ctypes.c_char_p(tname)
        except TypeError:
            tName = ctypes.c_char_p(tname.encode())
        __libddww__.ddsinfo_(ctypes.byref(error), ctypes.byref(self.diaref) , sigName, ctypes.byref(typ), 
                             tName, ind.ctypes.data_as(ctypes.c_void_p) , lsig , ltname)
        getError(error.value)
        return signalInfo(name.replace('\x00', '').strip(), numpy.uint32(typ.value), ind, 
                          tname.replace('\x00','').strip())

    def getObjectValue(self, name, field):
        """ Returns the value for the specified field for the given object name. """
        if not self.status:
            raise Exception('Shotfile not open')
        error = ctypes.c_int32(0)
        data = __fields__[field]()
        try:
            value = ctypes.c_char_p(data)
        except TypeError:
            try:
                value = data.ctypes.data_as(ctypes.c_void_p)
            except AttributeError:
                del data
                val = ctypes.c_int32(0)
                value = ctypes.byref(val)
        try:
            _name = ctypes.c_char_p(name)
        except TypeError:
            _name = ctypes.c_char_p(name.encode())
        try:
            _field = ctypes.c_char_p(field)
        except TypeError:
            _field = ctypes.c_char_p(field.encode())
        lname = ctypes.c_uint64(len(name))
        lfield = ctypes.c_uint64(len(field))
        result = __libddww__.ddobjval_(ctypes.byref(error),ctypes.byref(self.diaref),_name,_field, value,
                                       lname,lfield)
        getError(error)
        try:
            return data
        except Exception, Error:
            return numpy.int32(val.value)

    def getSignal(self, name, dtype=None, tBegin=None, tEnd=None):
        """ Return uncalibrated signal. If dtype is specified the data is
        converted accordingly, else the data is returned in the format used
        in the shotfile. """
        if not self.status:
            raise Exception('ddww::shotfile: Shotfile not open!')
        info = self.getSignalInfo(name)
        tInfo = self.getTimeBaseInfo(name)
        if tBegin==None:
            tBegin = tInfo.tBegin
        if tEnd==None:
            tEnd = tInfo.tEnd
        k1, k2 = self.getTimeBaseIndices(name, tBegin, tEnd)
        try:
            typ = ctypes.c_uint32(__type__[dtype])
            data = numpy.zeros(k2-k1+1, dtype=dtype)
        except KeyError, Error:
            dataformat = self.getObjectValue(name, 'dataformat')
            typ = ctypes.c_uint32(0)
            data = numpy.zeros(k2-k1+1, dtype=__dataformat__[dataformat])
        try:
            sigName = ctypes.c_char_p(name)
        except TypeError:
            sigName = ctypes.c_char_p(name.encode())
        error = ctypes.c_int32(0)
        leng = ctypes.c_uint32(0)
        lbuf = ctypes.c_uint32(k2-k1+1)
        k1 = ctypes.c_uint32(k1)
        k2 = ctypes.c_uint32(k2)
        lsigname = ctypes.c_uint64(len(name))
        result = __libddww__.ddsignal_(ctypes.byref(error), ctypes.byref(self.diaref), sigName, ctypes.byref(k1), 
                                       ctypes.byref(k2), ctypes.byref(typ) ,ctypes.byref(lbuf) , 
                                       data.ctypes.data_as(ctypes.c_void_p), ctypes.byref(leng), lsigname)
        getError(error)
        return data

    def getSignalCalibrated(self, name, dtype=numpy.float32, tBegin=None, tEnd=None):
        """ Return calibrated signal. If dtype is specified the data is
        converted accordingly, else the data is returned as numpy.float32. """
        if not self.status:
            raise Exception('ddww::shotfile: Shotfile not open!')
        info = self.getSignalInfo(name)
        tInfo = self.getTimeBaseInfo(name)
        if tBegin==None:
            tBegin = tInfo.tBegin
        if tEnd==None:
            tEnd = tInfo.tEnd
        k1, k2 = self.getTimeBaseIndices(name, tBegin, tEnd)
        typ = ctypes.c_uint32(__type__[dtype])
        data = numpy.zeros(k2-k1+1, dtype=dtype)
        try:
            sigName = ctypes.c_char_p(name)
        except TypeError:
            sigName = ctypes.c_char_p(name.encode())
        error = ctypes.c_int32(0)
        leng = ctypes.c_uint32(0)
        lbuf = ctypes.c_uint32(k2-k1+1)
        k1 = ctypes.c_uint32(k1)
        k2 = ctypes.c_uint32(k2)
        ncal = ctypes.c_int32(0)
        lname = ctypes.c_uint64(len(name))
        physdim = b' '*8
        __libddww__.ddcsgnl_(ctypes.byref(error), ctypes.byref(self.diaref), sigName, ctypes.byref(k1), ctypes.byref(k2), 
                             ctypes.byref(typ), ctypes.byref(lbuf), data.ctypes.data_as(ctypes.c_void_p), ctypes.byref(leng), 
                             ctypes.byref(ncal), ctypes.c_char_p(physdim), lname, ctypes.c_uint64(8))
        getError(error.value)
        return data, physdim.replace('\x00', '').strip()

    def getSignalGroup(self, name, dtype=None, tBegin=None, tEnd=None):       
        """ Return uncalibrated signalgroup. If dtype is specified the data is
        converted accordingly, else the data is returned in the format used 
        in the shotfile. """
        if not self.status:
            raise Exception('ddww::shotfile: Shotfile not open!')
        info = self.getSignalInfo(name)
        tInfo = self.getTimeBaseInfo(name)
        if tBegin==None:
            tBegin = tInfo.tBegin
        if tEnd==None:
            tEnd = tInfo.tEnd
        k1, k2 = self.getTimeBaseIndices(name, tBegin, tEnd)
        if info.index[0]!=tInfo.ntVal:
            k1 = 1
            k2 = info.index[0]
        size = info.size/info.index[0]*(k2-k1+1)
        print info.size, size
        try:
            typ = ctypes.c_uint32(__type__[dtype])
            data = numpy.zeros(size, dtype=dtype)
        except KeyError, Error:
            dataformat = self.getObjectValue(name, 'dataformat')
            typ = ctypes.c_uint32(0)
            data = numpy.zeros(size, dtype=__dataformat__[dataformat])
        try:
            sigName = ctypes.c_char_p(name)
        except TypeError:
            sigName = ctypes.c_char_p(name.encode())
        error = ctypes.c_int32(0)
        leng = ctypes.c_uint32(0)
        lbuf = ctypes.c_uint32(k2-k1+1)
        k1 = ctypes.c_uint32(k1)
        k2 = ctypes.c_uint32(k2)
        lname = ctypes.c_uint64(len(name))
        __libddww__.ddsgroup_(ctypes.byref(error), ctypes.byref(self.diaref), sigName, ctypes.byref(k1), 
                              ctypes.byref(k2), ctypes.byref(typ), ctypes.byref(lbuf), data.ctypes.data_as(ctypes.c_void_p), 
                              ctypes.byref(leng), lname)
        try:
            getError(error.value)
        finally:
            index1 = numpy.uint32(k2.value-k1.value+1)
            index = numpy.append(index1, info.index[1:])
            return data.reshape(tuple(index[:info.nDim]), order='F')

    def getTimeBaseInfo(self, name):
        """ Return information regarding timebase corresponding to name. """
        if not self.status:
            raise Exception('ddww::shotfile: Shotfile not open!')
        signalInfo = self.getSignalInfo(name)
        error = ctypes.c_int32(0)
        lsig = ctypes.c_uint64(len(name))
        typ = ctypes.c_int32(0)
        ind = numpy.zeros(4, dtype=numpy.uint32)
        lsig = ctypes.c_uint64(len(name))
        ntval = ctypes.c_uint32(0)
        npretrig = ctypes.c_uint32(0)
        time1 = ctypes.c_float(0.0)
        time2 = ctypes.c_float(0.0)
        try:
            sigName = ctypes.c_char_p(name)
        except TypeError:
            sigName = ctypes.c_char_p(name.encode())
        result = __libddww__.ddtrange_(ctypes.byref(error), ctypes.byref(self.diaref), sigName, ctypes.byref(time1), 
                                       ctypes.byref(time2), ctypes.byref(ntval), ctypes.byref(npretrig) ,lsig)
        getError(error.value)
        return timeBaseInfo(signalInfo.timeBase, numpy.uint32(ntval.value), numpy.uint32(npretrig.value), time1.value, time2.value)

    def getTimeBase(self, name, dtype=numpy.float32, tBegin=None, tEnd=None):
        """ Return timebase corresponding to name. """
        if not self.status:
            raise Exception('ddww::shotfile: Shotfile not open!')
        info = self.getSignalInfo(name)
        tInfo = self.getTimeBaseInfo(name)
        if tBegin==None:
            tBegin = tInfo.tBegin
        if tEnd==None:
            tEnd = tInfo.tEnd
        typ = ctypes.c_uint32(__type__[dtype])
        error = ctypes.c_int32(0)
        lsigname = ctypes.c_uint64(len(name))
        k1, k2 = self.getTimeBaseIndices(name, tBegin, tEnd)
        data = numpy.zeros(k2-k1+1, dtype=dtype)
        lbuf = ctypes.c_uint32(data.size)
        k1 = ctypes.c_uint32(k1)
        k2 = ctypes.c_uint32(k2)
        length = ctypes.c_uint32(0)
        try:
            sigName = ctypes.c_char_p(name)
        except TypeError:
            sigName = ctypes.c_char_p(name.encode())
        result = __libddww__.ddtbase_(ctypes.byref(error), ctypes.byref(self.diaref), sigName, ctypes.byref(k1), 
                                      ctypes.byref(k2), ctypes.byref(typ), ctypes.byref(lbuf), data.ctypes.data_as(ctypes.c_void_p), 
                                      ctypes.byref(length) ,lsigname)
        getError(error.value)
        return data

    def getTimeBaseIndices(self, name, tBegin, tEnd):
        """ Return time indices of name corresponding to tBegin and tEnd """
        if not self.status:
            raise Exception('ddww::shotfile: Shotfile not open!')
        try:
            sigName = ctypes.c_char_p(name)
        except TypeError:
            sigName = ctypes.c_char_p(name.encode())
        error = ctypes.c_int32(0)
        info = self.getTimeBaseInfo(name)
        if tEnd < tBegin:
            temp = tEnd
            tEnd = tBegin
            tBegin = temp
        if tBegin < info.tBegin:
            tBegin = info.tBegin
        if tEnd > info.tEnd:
            tEnd = info.tEnd
        try:
            time1 = ctypes.c_float(tBegin)
        except TypeError:
            time1 = ctypes.c_float(tBegin.value)
        try:
            time2 = ctypes.c_float(tEnd)
        except TypeError:
            time2 = ctypes.c_float(tEnd.value)
        k1 = ctypes.c_uint32(0)
        k2 = ctypes.c_uint32(0)
        lname = ctypes.c_uint64(len(name))
        __libddww__.ddtindex_(ctypes.byref(error), ctypes.byref(self.diaref), sigName, ctypes.byref(time1), 
                              ctypes.byref(time2), ctypes.byref(k1), ctypes.byref(k2), lname)
        getError(error.value)
        return numpy.uint32(k1.value), numpy.uint32(k2.value)

