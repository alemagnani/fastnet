# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.7
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.



from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_cudaconv2', [dirname(__file__)])
        except ImportError:
            import _cudaconv2
            return _cudaconv2
        if fp is not None:
            try:
                _mod = imp.load_module('_cudaconv2', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _cudaconv2 = swig_import_helper()
    del swig_import_helper
else:
    import _cudaconv2
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


MODULE_FILTER_IMAGE = _cudaconv2.MODULE_FILTER_IMAGE
FILTER_MODULE_IMAGE = _cudaconv2.FILTER_MODULE_IMAGE

def test(*args):
  return _cudaconv2.test(*args)
test = _cudaconv2.test

def convFilterActs(*args):
  return _cudaconv2.convFilterActs(*args)
convFilterActs = _cudaconv2.convFilterActs

def localFilterActs(*args):
  return _cudaconv2.localFilterActs(*args)
localFilterActs = _cudaconv2.localFilterActs

def convImgActs(*args):
  return _cudaconv2.convImgActs(*args)
convImgActs = _cudaconv2.convImgActs

def localImgActs(*args):
  return _cudaconv2.localImgActs(*args)
localImgActs = _cudaconv2.localImgActs

def convWeightActs(*args):
  return _cudaconv2.convWeightActs(*args)
convWeightActs = _cudaconv2.convWeightActs

def localWeightActs(*args):
  return _cudaconv2.localWeightActs(*args)
localWeightActs = _cudaconv2.localWeightActs

def convFilterActsSparse(*args):
  return _cudaconv2.convFilterActsSparse(*args)
convFilterActsSparse = _cudaconv2.convFilterActsSparse

def localFilterActsSparse(*args):
  return _cudaconv2.localFilterActsSparse(*args)
localFilterActsSparse = _cudaconv2.localFilterActsSparse

def convWeightActsSparse(*args):
  return _cudaconv2.convWeightActsSparse(*args)
convWeightActsSparse = _cudaconv2.convWeightActsSparse

def localWeightActsSparse(*args):
  return _cudaconv2.localWeightActsSparse(*args)
localWeightActsSparse = _cudaconv2.localWeightActsSparse

def convImgActsSparse(*args):
  return _cudaconv2.convImgActsSparse(*args)
convImgActsSparse = _cudaconv2.convImgActsSparse

def localImgActsSparse(*args):
  return _cudaconv2.localImgActsSparse(*args)
localImgActsSparse = _cudaconv2.localImgActsSparse
class NVMatrix(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, NVMatrix, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, NVMatrix, name)
    __repr__ = _swig_repr
    __swig_setmethods__["_numRows"] = _cudaconv2.NVMatrix__numRows_set
    __swig_getmethods__["_numRows"] = _cudaconv2.NVMatrix__numRows_get
    if _newclass:_numRows = _swig_property(_cudaconv2.NVMatrix__numRows_get, _cudaconv2.NVMatrix__numRows_set)
    __swig_setmethods__["_numCols"] = _cudaconv2.NVMatrix__numCols_set
    __swig_getmethods__["_numCols"] = _cudaconv2.NVMatrix__numCols_get
    if _newclass:_numCols = _swig_property(_cudaconv2.NVMatrix__numCols_get, _cudaconv2.NVMatrix__numCols_set)
    __swig_setmethods__["_stride"] = _cudaconv2.NVMatrix__stride_set
    __swig_getmethods__["_stride"] = _cudaconv2.NVMatrix__stride_get
    if _newclass:_stride = _swig_property(_cudaconv2.NVMatrix__stride_get, _cudaconv2.NVMatrix__stride_set)
    __swig_setmethods__["_devData"] = _cudaconv2.NVMatrix__devData_set
    __swig_getmethods__["_devData"] = _cudaconv2.NVMatrix__devData_get
    if _newclass:_devData = _swig_property(_cudaconv2.NVMatrix__devData_get, _cudaconv2.NVMatrix__devData_set)
    def __init__(self, *args): 
        this = _cudaconv2.new_NVMatrix(*args)
        try: self.this.append(this)
        except: self.this = this
    def getNumRows(self): return _cudaconv2.NVMatrix_getNumRows(self)
    def getNumCols(self): return _cudaconv2.NVMatrix_getNumCols(self)
    def getDevData(self): return _cudaconv2.NVMatrix_getDevData(self)
    def getStride(self): return _cudaconv2.NVMatrix_getStride(self)
    def getLeadingDim(self): return _cudaconv2.NVMatrix_getLeadingDim(self)
    def getFollowingDim(self): return _cudaconv2.NVMatrix_getFollowingDim(self)
    def getNumElements(self): return _cudaconv2.NVMatrix_getNumElements(self)
    def isTrans(self): return _cudaconv2.NVMatrix_isTrans(self)
    def isSameDims(self, *args): return _cudaconv2.NVMatrix_isSameDims(self, *args)
    def isContiguous(self): return _cudaconv2.NVMatrix_isContiguous(self)
    def resize(self, *args): return _cudaconv2.NVMatrix_resize(self, *args)
    def addVector(self, *args): return _cudaconv2.NVMatrix_addVector(self, *args)
    __swig_destroy__ = _cudaconv2.delete_NVMatrix
    __del__ = lambda self : None;
NVMatrix_swigregister = _cudaconv2.NVMatrix_swigregister
NVMatrix_swigregister(NVMatrix)


def sum(*args):
  return _cudaconv2.sum(*args)
sum = _cudaconv2.sum

def addVector(*args):
  return _cudaconv2.addVector(*args)
addVector = _cudaconv2.addVector

def convLocalMaxPool(*args):
  return _cudaconv2.convLocalMaxPool(*args)
convLocalMaxPool = _cudaconv2.convLocalMaxPool

def convLocalAvgUndo(*args):
  return _cudaconv2.convLocalAvgUndo(*args)
convLocalAvgUndo = _cudaconv2.convLocalAvgUndo

def convLocalMaxUndo(*args):
  return _cudaconv2.convLocalMaxUndo(*args)
convLocalMaxUndo = _cudaconv2.convLocalMaxUndo

def convResponseNorm(*args):
  return _cudaconv2.convResponseNorm(*args)
convResponseNorm = _cudaconv2.convResponseNorm

def convResponseNormUndo(*args):
  return _cudaconv2.convResponseNormUndo(*args)
convResponseNormUndo = _cudaconv2.convResponseNormUndo

def convContrastNorm(*args):
  return _cudaconv2.convContrastNorm(*args)
convContrastNorm = _cudaconv2.convContrastNorm

def convContrastNormUndo(*args):
  return _cudaconv2.convContrastNormUndo(*args)
convContrastNormUndo = _cudaconv2.convContrastNormUndo

def convGaussianBlur(*args):
  return _cudaconv2.convGaussianBlur(*args)
convGaussianBlur = _cudaconv2.convGaussianBlur

def convBedOfNails(*args):
  return _cudaconv2.convBedOfNails(*args)
convBedOfNails = _cudaconv2.convBedOfNails

def convBedOfNailsUndo(*args):
  return _cudaconv2.convBedOfNailsUndo(*args)
convBedOfNailsUndo = _cudaconv2.convBedOfNailsUndo

def convResizeBilinear(*args):
  return _cudaconv2.convResizeBilinear(*args)
convResizeBilinear = _cudaconv2.convResizeBilinear

def convRGBToYUV(*args):
  return _cudaconv2.convRGBToYUV(*args)
convRGBToYUV = _cudaconv2.convRGBToYUV

def convRGBToLAB(*args):
  return _cudaconv2.convRGBToLAB(*args)
convRGBToLAB = _cudaconv2.convRGBToLAB

def convCrop(*args):
  return _cudaconv2.convCrop(*args)
convCrop = _cudaconv2.convCrop

def normalizeLocalWeights(*args):
  return _cudaconv2.normalizeLocalWeights(*args)
normalizeLocalWeights = _cudaconv2.normalizeLocalWeights

def convTICAGrad(*args):
  return _cudaconv2.convTICAGrad(*args)
convTICAGrad = _cudaconv2.convTICAGrad

def convTICA(*args):
  return _cudaconv2.convTICA(*args)
convTICA = _cudaconv2.convTICA

def convContrastNormCrossMap(*args):
  return _cudaconv2.convContrastNormCrossMap(*args)
convContrastNormCrossMap = _cudaconv2.convContrastNormCrossMap

def convResponseNormCrossMapUndo(*args):
  return _cudaconv2.convResponseNormCrossMapUndo(*args)
convResponseNormCrossMapUndo = _cudaconv2.convResponseNormCrossMapUndo

def convResponseNormCrossMap(*args):
  return _cudaconv2.convResponseNormCrossMap(*args)
convResponseNormCrossMap = _cudaconv2.convResponseNormCrossMap
# This file is compatible with both classic and new-style classes.


