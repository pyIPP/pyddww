import numpy
import ctypes
import os
import copy
import warnings
warnings.simplefilter('always', DeprecationWarning)
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

__dataformat__ = { 1:numpy.uint8,
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

__obj__ = { 1: 'Diagnostic', 2: 'List',       3: 'Device',      4: 'Param_Set', \
            5: 'Map_Func',   6: 'Sig_Group',  7: 'Signal',      8: 'Time_Base', \
            9: 'SF_List',   10: 'Algorithm', 11: 'Update_Set', 12: 'Loc_Timer', \
           13: 'Area_Base', 14: 'Qualifier', 15: 'ModObj',     16: 'Map_Extd',  \
           17: 'Resource'}

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

class dd_info(object):
    def __init__(self):
        object.__init__(self)
        self.status = False

class objectHeader(object):
    def __init__(self, name, data, text):
        object.__init__(self)
        self.name = name
        self.text = text
        self.data = data

    def buffer():
        def fget(self):
            warnings.warn('buffer will be removed in the future, please use data.', DeprecationWarning)
            return self.data
        return locals()
    buffer = property(**buffer())

    def objectType():
        def fget(self):
            return __obj__[self.data[0]]
        return locals()
    objectType = property(**objectType())

    def level():
        def fget(self):
            return self.data[1]
        return locals()
    level = property(**level())

    def status():
        def fget(self):
            return self.data[2]
        return locals()
    status = property(**status())

    def error():
        def fget(self):
            return self.data[3]
        return locals()
    error = property(**error())

    def relations():
        def fget(self):
            return self.data[4:4+8][self.data[4:4+8]!=65535]
        return locals()
    relations = property(**relations())

    def address():
        def fget(self):
            return self.data[12]
        return locals()
    address = property(**address())

    def length():
        def fget(self):
            return self.data[13]
        return locals()
    length = property(**length())

    def dataFormat():
        def fget(self):
            return __dataformat__[self.data[14]]
        return locals()
    dataFormat = property(**dataFormat())

class signalHeader(objectHeader):
    def __init__(self, name, data, text):
        objectHeader.__init__(self, name, data, text)

    def unit():
        def fget(self):
            return getPhysicalDimension(self.data[15])
        return locals()
    unit = property(**unit())

class signalGroupHeader(objectHeader):        
    def __init__(self, name, data, text):
        objectHeader.__init__(self, name, data, text)

    def unit():
        def fget(self):
            return getPhysicalDimension(self.data[15])
        return locals()
    unit = property(**unit())

    def indices():
        def fget(self):
            return self.data[18:22][self.data[18:22]>1][::-1]
        return locals()
    indices = property(**indices())

class areaBaseHeader(objectHeader):
    def __init__(self, name, data, text):
        objectHeader.__init__(self, name, data, text)

    def unit():
        def fget(self):
            return getPhysicalDimension(self.data[15])
        return locals()
    unit = property(**unit())

class qualifierHeader(objectHeader):
    def __init__(self, name, data, text):
        objectHeader.__init__(self, name, data, text)

class timeBaseHeader(objectHeader):
    def __init__(self, name, data, text):
        objectHeader.__init__(self, name, data, text)

__headers__ = { 6:signalGroupHeader,
                7:signalHeader,
                8:timeBaseHeader,
                13:areaBaseHeader,
                14:qualifierHeader }

class signalInfo(object):
    """ Class storing the general information of a Signal. """
    def __init__(self, name, type, index, timeBase):
        """ Constructor initializing the signalInfo object. """
        object.__init__(self)
        self.name = name
        self.type = type
        self.index = index
        self.timeBase = timeBase

    def ndim():
        doc = """ Number of dimension of the signal. """
        def fget(self):
            return numpy.size(filter(lambda i: self.index[i]>1, xrange(self.index.size)))
        return locals()
    ndim = property(**ndim())

    def size():
        doc = """ Number of total datapoints in the signal. """
        def fget(self):
            return self.index[:self.ndim].prod()
        return locals()
    size = property(**size())

class timeBaseInfo(object):
    """ Class storing the general information for a timebase. """
    def __init__(self, name, ntVal, nPreTrig, tBegin, tEnd):
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

class qualifierInfo(object):
    def __init__(self, name, exists, indices, maxSection):
        object.__init__(self)
        self.name = name
        self.exists = exists
        self.indices = indices
        self.maxSection = maxSection

    def ndim():
        def fget(self):
            return self.indices[self.indices>1].size
        return locals()
    ndim = property(**ndim())

    def size():
        def fget(self):
            return self.indices[self.indices>1].prod()
        return locals()
    size = property(**size())

class qualifier(object):
    def __init__(self, name, status, data):
        object.__init__(self)
        self.name = name
        self.status = status
        self.data = data

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

class signal(object):
    def __init__(self, name, data, time=None, unit=''):
        object.__init__(self)
        self.name = name
        self.data = data
        self.time = time
        self.unit = unit

    def __call__(self, tBegin, tEnd):
        if self.time==None:
            raise Exception('Signal is not time dependent.')
        index = numpy.arange(self.time.size)[(self.time >= tBegin)*(self.time <= tEnd)]
        return signal(self.name, self.data[index], self.time[index], self.unit)

    def max(self):
        return numpy.nanmax(self.data)

    def min(self):
        return numpy.nanmin(self.data)

    def median(self):
        return numpy.median(self.data)

    def mean(self):
        return numpy.mean(self.data)

    def std(self):
        return numpy.std(self.data)

    def size():
        def fget(self):
            return self.data.size
        return locals()
    size = property(**size())

    def removeNaN(self):
        index = self.data==self.data
        self.data = self.data[index]
        if self.time!=None:
            self.time = self.time[index]

    def removeInvalid(self):
        self.removeNaN()
        index = numpy.isfinite(self.data)
        self.time = self.time[index]
        self.data = self.data[index]

    def __iadd__(self, rhs):
        try:
            self.data += numpy.interp(self.time, rhs.time, rhs.data)
            self.name = '(%s + %s)' % (self.name, rhs.name)
        except AttributeError, Error:
            self.data += rhs
        return self

    def __add__(self, rhs):
        try:
            return signal('(%s + %s)' % (self.name, rhs.name), self.data + numpy.interp(self.time, rhs.time, rhs.data), self.time)
        except AttributeError:
            return signal(self.name, self.data + rhs, self.time)

    def __radd__(self, rhs):
        return self.__add__(rhs)

    def __isub__(self, rhs):
        try:
            self.data -= numpy.interp(self.time, rhs.time, rhs.data)
            self.name = '(%s - %s)' % (self.name, rhs.name)
        except AttributeError:
            self.data -= rhs
        return self

    def __sub__(self, rhs):
        try:
            return signal('(%s - %s)' % (self.name, rhs.name), self.data - numpy.interp(self.time, rhs.time, rhs.data), self.time)
        except AttributeError:
            return signal(self.name, self.data - rhs, self.time)

    def __rsub__(self, rhs):
        return signal(self.name, rhs-self.data, self.time)

    def __pow__(self, exponent):
        return signal(self.name, self.data**exponent, self.time)

    def __imul__(self, rhs):
        try:
            self.data *= numpy.interp(self.time, rhs.time, rhs.data)
            self.name = '(%s * %s)' % (self.name, rhs.name)
        except AttributeError:
            self.data *= rhs
        return self

    def __mul__(self, rhs):
        try:
            return signal('(%s * %s)' % (self.name, rhs.name), self.data * numpy.interp(self.time, rhs.time, rhs.data), self.time)
        except AttributeError:
            return signal(self.name, self.data * rhs, self.time)

    def __rmul__(self, rhs):
        return self.__mul__(rhs)

    def __idiv__(self, rhs):
        try:
            self.data /= numpy.interp(self.time, rhs.time, rhs.data)
            self.name = '(%s / %s)' % (self.name, rhs.name)
        except AttributeError:
            self.data /= rhs
        return self

    def __div__(self, rhs):
        try:
            return signal('%s / %s' % (self.name, rhs.name), self.data / numpy.interp(self.time, rhs.time, rhs.data), self.time)
        except AttributeError:
            return signal(self.name, self.time / rhs, self.time)
        
    def __rdiv__(self, rhs):
        return signal(self.name, rhs/self.data, self.time)
            


class signalGroup(object):
    def __init__(self, name, data, time=None, unit=''):
        object.__init__(self)
        self.name = name
        self.data = data
        self.time = time
        self.unit = unit

    def __call__(self, tBegin, tEnd):
        if self.time==None:
            raise Exception('SignalGroup is not time dependent.')
        index = numpy.arange(self.time.size)[(self.time >= tBegin)*(self.time <= tEnd)]
        return signal(self.name, self.data[index], self.time[index], self.unit)

    def __getitem__(self, indices):
        if self.time==None:
            if self.data.ndim == numpy.size(indices):
                return signal(self.name, self.data[indices], None, self.unit)
            else:
                raise Exception('Wrong number of indices provided. Get %d needed %d.' % (numpy.size(indices), self.data.ndim))
        else:
            if self.data.ndim-1 == numpy.size(indices):
                if numpy.size(indices)==1:
                    try:
                        return signal(self.name, self.data[:,indices[0]], self.time, self.unit)
                    except Exception:
                        return signal(self.name, self.data[:, indices], self.time, self.unit)
                elif numpy.size(indices)==2:
                    return signal(self.name, self.data[:,indices[0], indices[1]], self.time, self.unit)
                elif numpy.size(indices)==3:
                    return signal(self.name, self.data[:,indices[0], indices[1], indices[2]], self.time, self.unit)
                else:
                    raise Exception('Invalid number of indices: Got %d needed %d' % (numpy.size(indices), (self.data.nnim-1)))

    def max(self, axis=None):
        return numpy.nanmax(self.data, axis=axis)
    
    def min(self, axis=None):
        return numpy.nanmin(self.data, axis=axis)

    def median(self, axis=None):
        return numpy.median(self.data, axis=axis)

    def mean(self, axis=None):
        return numpy.mean(self.data, axis=axis)

    def shape():
        def fget(self):
            return self.data.shape
        return locals()
    shape = property(**shape())

    def size():
        def fget(self):
            return self.data.size
        return locals()
    size = property(**size())

    def ndim():
        def fget(self):
            return self.data.ndim
        return locals()
    ndim = property(**ndim())

class areaBaseInfo(object):
    def __init__(self, name, sizes, dimensions, index):
        object.__init__(self)
        self.name = name
        self.sizes = sizes
        self.dimensions = dimensions
        self.index = index

    def ndim():
        def fget(self):
            return self.sizes[self.sizes>1].size
        return locals()
    ndim = property(**ndim())

    def size():
        def fget(self):
            return self.sizes[self.sizes>1].prod()
        return locals()
    size = property(**size())


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

    def getSignalNames(self):
        """ Return list of all signal names in the shotfile. """
        if not self.status:
            raise Exception('Shotfile not open!')
        output = []
        names = self.getObjectNames()
        for key in names.keys():
            name = names[key]
            if self.getObjectValue(name, 'objtype')==7:
                output.append(name)
        return output

    def getSignalGroupNames(self):
        """ Return list of all signalgroup names in the shotfile. """
        if not self.status:
            raise Exception('Shotfile not open!')
        output = []
        names = self.getObjectNames()
        for key in names.keys():
            name = names[key]
            if self.getObjectValue(name, 'objtype')==6:
                output.append(name)
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
                data, unit = self.getSignalGroupCalibrated(name, dtype=dtype, tBegin=tBegin, tEnd=tEnd)
            else:
                data = self.getSignalGroup(name, dtype=dtype, tBegin=tBegin, tEnd=tEnd)
                unit = ''
            try:
                time = self.getTimeBase(name, tBegin=tBegin, tEnd=tEnd)
            except Exception:
                time = None
            return signalGroup(name, data, time, unit)
        elif objectType==7:
            if calibrated:
                if dtype not in [numpy.float32, numpy.float64]:
                    dtype=numpy.float32
                data, unit = self.getSignalCalibrated(name, dtype=dtype, tBegin=tBegin, tEnd=tEnd)
            else:
                data = self.getSignal(name, dtype=dtype, tBegin=tBegin, tEnd=tEnd)
                unit = ''
            try:
                time = self.getTimeBase(name, tBegin=tBegin, tEnd=tEnd)
            except Exception:
                time = None
            return signal(name, data, time=time, unit=unit)
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
                warnings.warn(
                'Length of time base and first index of signal group "%s" not matching. Ignoring tBegin/tEnd.'%name,
                RuntimeWarning)
                k1 = 1
                k2 = info.index[0]
        except Exception:
            k1 = 1
            k2 = info.index[0]
        size = info.size/info.index[0]*(k2-k1+1)
        index = numpy.append(k2-k1+1, info.index[1:])
        try:
            typ = ctypes.c_uint32(__type__[dtype])
            data = numpy.zeros(index[:info.ndim], dtype=dtype, order='F')
        except KeyError, Error:
            dataformat = self.getObjectValue(name, 'dataformat')
            typ = ctypes.c_uint32(0)
            data = numpy.zeros(index[:info.ndim], dtype=__dataformat__[dataformat], order='F')
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
        return data

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
            if info.index[0]==tInfo.ntVal:
                k1, k2 = self.getTimeBaseIndices(name, tBegin, tEnd)
            else:
                warnings.warn(
                'Length of time base and first index of signal group "%s" not matching. Ignoring tBegin/tEnd.'%name,
                RuntimeWarning)
                k1 = 1
                k2 = info.index[0]
        except Exception, Error:
            k1 = 1
            k2 = info.index[0]
        index = numpy.append(k2-k1+1, info.index[1:])
        if dtype not in [numpy.float32, numpy.float64]:
            dtype=numpy.float32
        typ = ctypes.c_uint32(__type__[dtype])
        data = numpy.zeros(index[:info.ndim], dtype=dtype, order='F')
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
        return data, physdim.replace('\x00', '').strip()


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
        if info.index[0]==tInfo.ntVal:
            k1, k2 = self.getTimeBaseIndices(name, tBegin, tEnd)
        else:
            k1 = 1
            k2 = info.index[0]
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
        warnings.warn('GetSignal will be removed in the future.', DeprecationWarning)
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

    def getAreaBaseInfo(self, name):
        if not self.status:
            raise Exception('Shotfile not open!')
        error = ctypes.c_int32(0)
        sizes = numpy.zeros(3, dtype=numpy.uint32)
        adim = numpy.zeros(3, dtype=numpy.uint32)
        index = ctypes.c_int32(0)
        lname = ctypes.c_uint64(len(name))
        try:
            sigName = ctypes.c_char_p(name)
        except TypeError:
            sigName = ctypes.c_char_p(name.encode())
        lname = ctypes.c_uint64(len(name))
        __libddww__.ddainfo_(ctypes.byref(error) , ctypes.byref(self.diaref), sigName , sizes.ctypes.data_as(ctypes.c_void_p),
                             adim.ctypes.data_as(ctypes.c_void_p), ctypes.byref(index) , lname)
        getError(error.value)
        return areaBaseInfo(name, sizes, adim, numpy.int32(index.value))

    def getAreaBase(self, name, dtype=numpy.float32, tBegin=None, tEnd=None):
        if not self.status:
            raise Exception('Shotfile not open')
        info = self.getSignalInfo(name)
        aInfo = self.getAreaBaseInfo(name)
        error = ctypes.c_int32(0)
        if aInfo.index==0:
            index = aInfo.sizes[:aInfo.ndim]
            k1 = 1
            k2 = index[0]
        else:
            tInfo = self.getTimeBaseInfo(name)
            if tBegin==None:
                tBegin = tInfo.tBegin
            if tEnd==None:
                tEnd = tInfo.tEnd
            k1, k2 = self.getTimeBaseIndices(name, tBegin, tEnd)
            if aInfo.index==1:
                index = numpy.append(k2-k1+1, aInfo.sizes[:aInfo.ndim])
            elif aInfo.index in [2,3]:
                index = numpy.append(aInfo.sizes[:aInfo.ndim], k2-k1+1)
            else:
                raise Exception('Invalid area base index.')
        try:
            sigName = ctypes.c_char_p(name)
        except TypeError:
            sigName = ctypes.c_char_p(name.encode())
        lname = ctypes.c_uint64(len(name))
        if dtype not in [numpy.float32, numpy.float64]:
            dtype = numpy.float32
        typ = ctypes.c_uint32(__type__[dtype])
        data = numpy.zeros(index, dtype=dtype, order='F')
        albuf = ctypes.c_uint32(aInfo.sizes[0])
        length = ctypes.c_uint32(0)
        k1 = ctypes.c_uint32(k1)
        k2 = ctypes.c_uint32(k2)
        __libddww__.ddagroup_(ctypes.byref(error), ctypes.byref(self.diaref), sigName, ctypes.byref(k1), ctypes.byref(k2),
                              ctypes.byref(typ), ctypes.byref(albuf), data.ctypes.data_as(ctypes.c_void_p), ctypes.byref(length),
                              lname)
        getError(error.value)
        return data

    def getQualifierInfo(self, name):
        if not self.status:
            raise Exception('Shotfile not open!')
        error = ctypes.c_int32(0)
        try:
            sigName = ctypes.c_char_p(name)
        except TypeError:
            sigName = ctypes.c_char_p(name.encode())
        lname = ctypes.c_uint64(len(name))
        exist = ctypes.c_int32(0)
        indices = numpy.zeros(3, dtype=numpy.int32)
        maxsection = ctypes.c_uint32(0)
        __libddww__.ddqinfo_(ctypes.byref(error), ctypes.byref(self.diaref), sigName, ctypes.byref(exist),
                             indices.ctypes.data_as(ctypes.c_void_p), ctypes.byref(maxsection), lname)
        getError(error.value)
        return qualifierInfo(name, numpy.int32(exist.value), indices, numpy.uint32(maxsection.value))

    def getQualifier(self, name):
        if not self.status:
            raise Exception('Shotfile not open!')
        error = ctypes.c_int32(0)
        info = self.getQualifierInfo(name)
        try:
            sigName = ctypes.c_char_p(name)
        except TypeError:
            sigName = ctypes.c_char_p(name.encode())
        lname = ctypes.c_uint64(len(name))
        data = numpy.zeros(info.indices[:info.ndim], dtype=numpy.int32, order='F')
        lbuf = ctypes.c_int32(info.size)
        status = ctypes.c_int32(0)
        __libddww__.ddqget_(ctypes.byref(error), ctypes.byref(self.diaref), sigName, ctypes.byref(status),
                            ctypes.byref(lbuf), data.ctypes.data_as(ctypes.c_void_p), lname)
        getError(error.value)
        return qualifier(name, numpy.int32(status.value), data)



    def getObjectHeader(self, name):
        """ Returns the object header of a given object."""
        if not self.status:
            raise Exception('Shotfile not open!')
        text = 64*b' '
        error   = ctypes.c_int32(0)
        try:
            _name = ctypes.c_char_p(name)
        except TypeError:
            _name = ctypes.c_char_p(name.encode())
        buffer = numpy.zeros(26, dtype=numpy.int32)
        lname = ctypes.c_uint64(len(name))
        ltext = ctypes.c_uint64(len(text))
        result = __libddww__.ddobjhdr_(ctypes.byref(error), ctypes.byref(self.diaref), _name, 
                                       buffer.ctypes.data_as(ctypes.c_void_p), ctypes.c_char_p(text), 
                                       lname, ltext)
        getError(error)
        try:
            return __headers__[buffer[0]](name, buffer, text.replace('\x00','').strip())
        except Exception, Error:
            print Error
            return objectHeader(name, buffer, text.replace('\x00','').strip())

    def GetObjectHeader(self, name):
        warnings.warn('GetObjectHeader will be removed in the future, please use getObjectHeader.', DeprecationWarning)
        return self.getObjectHeader(name)

    def getRelations(self, name):
        """ Returns all relations of a given object."""
        if not self.status:
            raise Exception('Shotfile not open!')

        rel_out = dd_info()
        head = self.getObjectHeader(name)
        rel_out.error = head.error
        if head.error == 0:
            ids = head.buffer[4:12]
            rel_out.id  = []
            rel_out.typ = []
            rel_out.txt = []
            for objid in ids:
                if objid != 65535:
                    rel_out.id.append(objid)
                    tname = self.getObjectName(objid)
                    rel_out.typ.append(self.getObjectValue(tname, 'objtype'))
                    rel_out.txt.append(tname)
        return rel_out

    def GetRelations(self, name):
        warnings.warn('GetRelations will be removed in the future, please use getRelations.', DeprecationWarning)
        return self.getRelations(name)

    def getInfo(self, name):
        """ Returns information about the specified signal."""
        if not self.status:
            raise Exception('Shotfile not open!')

        output = dd_info()
        rel = self.getRelations(name)
        output.rels = rel.txt
        output.error = rel.error
        output.tname = None
        output.aname = None
        output.tlen = None
        output.index = None
        output.units = None
        output.address = None
        output.bytlen = None
        output.level = None
        output.status = None
        output.error = None
        output.ind = None
        if rel.error == 0:
            jtime = None
            jarea = None
            for jid, id in enumerate(rel.typ):
                if id == 8:
                    jtime = jid
                    output.tname = rel.txt[jid]
                if id == 13:
                    jarea = jid
                    output.aname = rel.txt[jid]

            head = self.getObjectHeader(name)
            buf_str = ''
            for hb in head.buffer:
                buf_str += str(hb)+' '
            output.error = head.error
            if head.error == 0:
                output.buf = head.buffer
                output.objtyp = output.buf[0]
                output.level = output.buf[1]
                output.status = output.buf[2]
                output.error = output.buf[3]
                output.address = output.buf[12]
                output.bytlen = output.buf[13]
                if output.objtyp in (6, 7, 8, 13):
                    output.units = getPhysicalDimension(output.buf[15])
                    output.estatus = output.buf[17]
                    output.fmt = output.buf[14]
                    if output.objtyp in (6, 7):
                        output.index = output.buf[1]
                        dims = numpy.array(output.buf[18:22][::-1], dtype=numpy.int32)
                        output.ind = numpy.array(dims[dims > 0])

                    if output.objtyp == 8: # If 'name' is a TB
                        output.tlen = output.buf[21] # = dims[0]
                        output.tfmt = output.buf[14]
                    else:
                        tlen1 = -1
                        if (output.index == 1) or (output.objtyp == 7):
                            tlen1 = dims[0]
                        elif output.index in (2,3):
                            tlen1 = dims[1]
                        if jtime != None:
                            thead = self.getObjectHeader(rel.txt[jtime])
                            tbuf = thead.buffer
                            output.tlen = tbuf[21]
                            output.tfmt = tbuf[14]
# Check consistency with TB length
                            if output.tlen != tlen1 and tlen1 != -1:
                                output.tlen = -1
                        else:
                            print('No TB found for %s %s' %(obj_d[output.objtyp], name))

                    if output.objtyp == 13: # If 'name' is an AB
                        output.atlen = output.buf[21]
                        output.afmt = output.buf[14]
                        sizes = numpy.array(output.buf[18:21], dtype = numpy.int32)
                        output.sizes = sizes[sizes > 0]
                    else:
# Beware: other than in DDAINFO2, here 'sizes' can have less than
# 3 dims, as the 0-sized are removed. Usually (always?) it has 1 dim.
                        if jarea != None:
                            ahead = self.getObjectHeader(rel.txt[jarea])
                            abuf = ahead.buffer
                            output.atlen = abuf[21] # #time points of AB
                            output.afmt = abuf[14]
                            sizes = numpy.array(abuf[18:21], dtype = numpy.int32)
                            output.sizes = sizes[sizes > 0]

        return output

    def GetInfo(self, name):
        warnings.warn('GetInfo will be removed in the future, please use getInfo.', DeprecationWarning)
        return self.getInfo(name)



# to not annoy users that don't even use this library with e-mails,
# collect usernames of users in /afs/ipp/u/abock/pub/pyUsage/dd/
def touch(fname, times=None):
    fhandle = file(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()
touch('/afs/ipp/u/abock/pub/pyUsage/dd/%s'%getpass.getuser())
