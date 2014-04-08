import numpy
import ctypes
import os
import copy
import warnings
import getpass

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
                    2:numpy.character,
                    3:numpy.int16,
                    4:numpy.int32,
                    5:numpy.float32,
                    6:numpy.float64,
                    7:numpy.bool,
                    9:numpy.uint16,
                    13:numpy.int64,
                    14:numpy.uint32,
                    15:numpy.uint64,
                    1794:numpy.dtype('S8')}

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
            warnings.warn(text.value.strip(), RuntimeWarning)

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

class parameterSetInfo(object):
    def __init__(self, setName, names, items, format, devsig):
        object.__init__(self)
        self.setName = setName
        self.names = names
        self.items = items
        self.format = format
        self.devsig = devsig

    def __getitem__(self, i):
        return parameterInfo(self.setName, self.names[i], self.items[i], self.format[i])

class parameterInfo(object):
    def __init__(self, setName, parName, items, format):
        object.__init__(self)
        self.setName = setName
        self.parName = parName
        self.items = items
        self.format = format

class mappingInfo(object):
    def __init__(self, name, device, channel):
        object.__init__(self)
        self.name = name
        self.device = device
        self.channel = channel

class parameter(object):
    def __init__(self, setName, parName, data, unit):
        object.__init__(self)
        self.setName = setName
        self.name = parName
        self.data = data
        self.unit = unit

class parameterSet(dict):
    def __init__(self, setName):
        dict.__init__(self)
        self.name = setName

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
            raise Exception('Shotfile not open!')
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
            raise Exception('Shotfile not open!')
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
            raise Exception('Shotfile not open!')
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

    def __call__(self, name, dtype=None, tBegin=None, tEnd=None, calibrated=True):
        """ Unified function to read data from a signal, signalgroup or timebase.
        Keywords:
           dtype: If desired the datatype of the output can be specified. If no dtype is specified,
                  the data will be returned as float32 in case of calibrated data and in the format
                  used in the shotfile in case of uncalibrated data.
           tBegin: Sets the starting point from which time data will be read. Note here that for signals
                   without a time dependence or in case of signal groups where the time index is not the
                   first index this keyword has no effect.
           tEnd: Similar to tBegin but this sets the time until which the data will be read.
           calibrated: If True calibrated data together with the unit will be returned. If False the data
                       as written in the shotfile will be returned.
        """
        if not self.status:
            raise Exception('Shotfile not open!')
        objectType = self.getObjectValue(name, 'objtype')
        if objectType==4:
            return self.getParameterSet(name, dtype=dtype)
        elif objectType==5:
            raise Exception('Mapping function not yet implemented.')
        elif objectType==6:
            if calibrated:
                return self.getSignalGroupCalibrated(name, dtype=dtype, tBegin=tBegin, tEnd=tEnd)
            else:
                return self.getSignalGroup(name, dtype=dtype, tBegin=tBegin, tEnd=tEnd)
        elif objectType==7:
            if calibrated:
                if dtype not in [numpy.float32, numpy.float64]:
                    dtype=numpy.float32
                return self.getSignalCalibrated(name, dtype=dtype, tBegin=tBegin, tEnd=tEnd)
            else:
                return self.getSignal(name, dtype=dtype, tBegin=tBegin, tEnd=tEnd)
        elif objectType==8:
            if dtype not in [numpy.float32, numpy.float64]:
                dtype=numpy.float32
            return self.getTimeBase(name, dtype=dtype, tBegin=tBegin, tEnd=tEnd)
        elif objectType==13:
            raise Exception('Area Base not yet implemented.')
        else:
            raise Exception('Unsupported object type %d for object %s' % (objectType, name))

    def getSignal(self, name, dtype=None, tBegin=None, tEnd=None):
        """ Return uncalibrated signal. If dtype is specified the data is
        converted accordingly, else the data is returned in the format used
        in the shotfile. """
        if not self.status:
            raise Exception('Shotfile not open!')
        info = self.getSignalInfo(name)
        try:
            tInfo = self.getTimeBaseInfo(name)
            if tBegin==None:
                tBegin = tInfo.tBegin
            if tEnd==None:
                tEnd = tInfo.tEnd
            if tInfo.ntVal==info.index[0]:
                k1, k2 = self.getTimeBaseIndices(name, tBegin, tEnd)
            else:
                k1 = 1
                k2 = info.index[0]
        except Exception:
            k1 = 1
            k2 = info.index[0]
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
            raise Exception('Shotfile not open!')
        info = self.getSignalInfo(name)
        try:
            tInfo = self.getTimeBaseInfo(name)
            if tBegin==None:
                tBegin = tInfo.tBegin
            if tEnd==None:
                tEnd = tInfo.tEnd
            if tInfo.ntVal==info.index[0]:
                k1, k2 = self.getTimeBaseIndices(name, tBegin, tEnd)
            else:
                k1 = 1
                k2 = info.index[0]
        except Exception:
            k1 = 1
            k2 = info.index[0]
        if dtype not in [numpy.float32, numpy.float64]:
            dtype=numpy.float32
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
            raise Exception('Shotfile not open!')
        info = self.getSignalInfo(name)
        try:
            tInfo = self.getTimeBaseInfo(name)
            if tBegin==None:
                tBegin = tInfo.tBegin
            if tEnd==None:
                tEnd = tInfo.tEnd
            if info.index[0]==tInfo.ntVal:
                k1, k2 = self.getTimeBaseIndices(name, tBegin, tEnd)
            else:
                k1 = 1
                k2 = info.index[0]
        except Exception:
            k1 = 1
            k2 = info.index[0]
        size = info.size/info.index[0]*(k2-k1+1)
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
        getError(error.value)
        index1 = numpy.uint32(k2.value-k1.value+1)
        index = numpy.append(index1, info.index[1:])
        return data.reshape(tuple(index[:info.nDim]), order='F')

    def getSignalGroupCalibrated(self, name, dtype=numpy.float32, tBegin=None, tEnd=None):
        if not self.status:
            raise Exception('Shotfile not open!')
        info = self.getSignalInfo(name)
        try:
            tInfo = self.getTimeBaseInfo(name)
            if tBegin==None:
                tBegin = tInfo.tBegin
            if tEnd==None:
                tEnd = tInfo.tEnd
            if info.index[0]==info.ntVal:
                k1, k2 = self.getTimeBaseIndices(name, tBegin, tEnd)
            else:
                k1 = 1
                k2 = info.index[0]
        except Exception:
            k1 = 1
            k2 = info.index[0]
        size = info.size/info.index[0]*(k2-k1+1)
        if dtype not in [numpy.float32, numpy.float64]:
            dtype=numpy.float32
        typ = ctypes.c_uint32(__type__[dtype])
        data = numpy.zeros(size, dtype=dtype)
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
        __libddww__.ddcsgrp_(ctypes.byref(error), ctypes.byref(self.diaref), sigName, ctypes.byref(k1), ctypes.byref(k2), 
                             ctypes.byref(typ), ctypes.byref(lbuf), data.ctypes.data_as(ctypes.c_void_p), ctypes.byref(leng), 
                             ctypes.byref(ncal), ctypes.c_char_p(physdim), lname, ctypes.c_uint64(8))
        getError(error.value)
        index1 = numpy.uint32(k2.value-k1.value+1)
        index = numpy.append(index1, info.index[1:])
        return data.reshape(tuple(index[:info.nDim]), order='F'), physdim.replace('\x00', '').strip()


    def getTimeBaseInfo(self, name):
        """ Return information regarding timebase corresponding to name. """
        if not self.status:
            raise Exception('Shotfile not open!')
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
            raise Exception('Shotfile not open!')
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
        if dtype not in [numpy.float32, numpy.float64]:
            dtype = numpy.float32
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
            raise Exception('Shotfile not open!')
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

    def getParameterSetInfo(self, name):
        if not self.status:
            raise Exception('Shotfile not open!')
        error = ctypes.c_int32(0)
        try:
            parName = ctypes.c_char_p(name)
        except TypeError:
            parName = ctypes.c_char_p(name.encode())
        lname = ctypes.c_uint64(len(name))
        info = self.getObjectValue(name, 'items')
        nrec = ctypes.c_int32(info)
        rname = b' '*8*info
        items = numpy.zeros(info, dtype=numpy.uint32)
        format = numpy.zeros(info, dtype=numpy.uint16)
        devsig = numpy.zeros(info, dtype=numpy.int32)
        __libddww__.ddprinfo_(ctypes.byref(error), ctypes.byref(self.diaref), parName, ctypes.byref(nrec), 
                              ctypes.c_char_p(rname), items.ctypes.data_as(ctypes.c_void_p), 
                              format.ctypes.data_as(ctypes.c_void_p), devsig.ctypes.data_as(ctypes.c_void_p) ,lname)
        getError(error.value)
        names = []
        for i in xrange(info):
            names.append(rname[i*8:(i+1)*8].replace('\x00','').strip())
        return parameterSetInfo(name, names, items, format, devsig)

    def getParameterInfo(self, setName, parName):
        if not self.status:
            raise Exception('Shotfile not open!')
        error = ctypes.c_int32(0)
        try:
            set = ctypes.c_char_p(setName)
        except TypeError:
            set = ctypes.c_char_p(setName.encode())
        lset = ctypes.c_uint64(len(setName))
        try:
            par = ctypes.c_char_p(parName)
        except TypeError:
            par = ctypes.c_char_p(parName.encode())
        lpar = ctypes.c_uint64(len(parName))
        item = ctypes.c_uint32(0)
        format = ctypes.c_uint16(0)
        __libddww__.dd_prinfo_(ctypes.byref(error), ctypes.byref(self.diaref), set, par, ctypes.byref(item), 
                               ctypes.byref(format), lset, lpar)
        getError(error.value)
        return parameterInfo(setName, parName, numpy.uint32(item.value), numpy.uint16(format.value))

    def getParameter(self, setName, parName, dtype=None):
        if not self.status:
            raise Exception('Shotfile not open!')
        info = self.getParameterInfo(setName, parName)
        error = ctypes.c_int32(0)
        try:
            name = ctypes.c_char_p(setName)
        except TypeError:
            name = ctypes.c_char_p(setName.encode())
        lname = ctypes.c_uint64(len(setName))
        try:
            pname = ctypes.c_char_p(parName)
        except TypeError:
            pname = ctypes.c_char_p(parName.encode())
        lpname = ctypes.c_uint64(len(parName))
        try:
            typ = ctypes.c_uint32(__type__[dtype])
            data = numpy.zeros(info.items, dtype=dtype)
        except KeyError, Error:
            typ = ctypes.c_uint32(0)
            data = numpy.zeros(info.items, dtype=__dataformat__[info.format])
        lbuf = ctypes.c_int32(info.items)
        physunit = ctypes.c_int32(0)
        __libddww__.ddparm_(ctypes.byref(error), ctypes.byref(self.diaref), name, pname, ctypes.byref(typ), ctypes.byref(lbuf), 
                            data.ctypes.data_as(ctypes.c_void_p), ctypes.byref(physunit), lname, lpname)
        getError(error.value)
        if data.size==1:
            return parameter(setName, parName, data[0], getPhysicalDimension(physunit.value))
        else:
            return parameter(setName, parName, data, getPhysicalDimension(physunit.value))

    def getParameterSet(self, setName, dtype=None):
        if not self.status:
            raise Exception('Shotfile not open!')
        info = self.getParameterSetInfo(setName)
        output = parameterSet(setName)
        for name in info.names:
            output[name] = self.getParameter(setName, name, dtype=dtype)
        return output

    def getList(self, name):
        if not self.status:
            raise Exception('Shotfile not open!')
        try:
            nam = ctypes.c_char_p(name)
        except TypeError:
            nam = ctypes.c_char_p(name.encode())
        lname = ctypes.c_uint64(len(name))
        error = ctypes.c_int32(0)
        listlen = ctypes.c_int32(256)
        nlist = numpy.zeros(256, dtype=numpy.dtype('S9'))
        __libddww__.ddlnames_(ctypes.byref(error), ctypes.byref(self.diaref), nam, ctypes.byref(listlen), 
                              nlist.ctypes.data_as(ctypes.c_void_p), lname, ctypes.c_uint64(9*256))
        getError(error.value)
        output = []
        for i in xrange(listlen.value):
            output.append(nlist[i].replace('\x00','').strip())
        return output

    def getMappingInfo(self, name, indices=None):
        if not self.status:
            raise Exception('Shotfile not open!')
        if indices==None:
            indices = numpy.ones(3, dtype=numpy.uint32)
        else:
            indices = numpy.uint32(indices)
        try:
            nam = ctypes.c_char_p(name)
        except TypeError:
            nam = ctypes.c_char_p(name.encode())
        lname = ctypes.c_uint64(len(name))
        error = ctypes.c_int32(0)
        devname = b' '*8
        channel = ctypes.c_int32(0)
        __libddww__.ddmapinfo_(ctypes.byref(error), ctypes.byref(self.diaref), nam, indices.ctypes.data_as(ctypes.c_void_p), 
                               ctypes.c_char_p(devname), ctypes.byref(channel), lname, ctypes.c_uint64(8))
        getError(error.value)
        return mappingInfo(name, devname.replace('\x00', ''), numpy.int32(channel.value))

    def GetSignal(self, name, cal=False):
        warnings.warn('GetSignal will be removed in the future.')
        if not self.status:
            raise Exception('Shotfile not open!')
        objectType = self.getObjectValue(name, 'objtype')
        if objectType==6:
            if cal:
                return self.getSignalGroupCalibrated(name)[0]
            else:
                return self.getSignalGroup(name)
        elif objectType==7:
            if cal:
                return self.getSignalCalibrated(name)[0]
            else:
                return self.getSignal(name)
        else:
            raise Exception('Unsupported object type: %d' % objectType)


# to not annoy users that don't even use this library with e-mails,
# collect usernames of users in /afs/ipp/u/abock/pub/pyUsage/dd/
def touch(fname, times=None):
    fhandle = file(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()
touch('/afs/ipp/u/abock/pub/pyUsage/dd/%s'%getpass.getuser())




