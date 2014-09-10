from __future__ import absolute_import
import inspect
import collections

__all__ = ['VProperty']


class VProperty(object):
    """Enchanced Python property, supporting 
    
    @TODO: Allow the function names for the class to be specified as
        either 'fget'/'getter', 'fset'/'setter', 'fdel'/'deleter', 'fval'/'validator'
    @TODO: Allow additional methods to be provided on a decorated class. Essentially
        anything not causing a conflict. basically I would like the class defined in
        the decorator to be in the method-resolution order for the new vproperty descriptor.
        (* complication: need to rename getter/setter/deleter/validator to fget/fset etc)
    
    """
    def __init__(self, *fargs, **fkwargs):
        """Check if used as a decorator for a class, or if used
        conventionally.
        """
        (self.fget,
         self.fset,
         self.fdel,
         self.fval,
         self.__doc__) = self.validate(*fargs, **fkwargs)
         
    def validate(self, *fargs, **fkwargs):
        if len(fargs)==1 and len(fkwargs)==0:
            if inspect.isclass(fargs[0]):
                return self._validate_from_class(fargs[0])
        return self._validate_from_args(*fargs, **fkwargs)
    def _validate_from_args(self, fget=None, fset=None, fdel=None, fval=None, doc=None):
        """This is basically a validation function. Consider renaming?"""
        if doc is None and fget is not None:
            doc = fget.__doc__
        return fget, fset, fdel, fval, doc
    def _validate_from_class(self, klass):
        fget=_tryget(klass, ('fget', '_get', 'getter'), default=None)
        fset=_tryget(klass, ('fset', '_set', 'setter'), default=None)
        fdel=_tryget(klass, ('fdel', '_del', 'deleter'), default=None)
        fval=_tryget(klass, ('fval', '_val', 'validator'), default=None)
        doc =_tryget(klass, '__doc__', default=None)
        if doc is None and fget is not None:
            doc = fget.__doc__
        return fget, fset, fdel, fval, doc
    #----- Descriptors
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        if self.fval is not None: #Validate, if possible
            value = self.fval(obj, value)
        self.fset(obj, value)
    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)
    #----- Decorators
    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.fval, self.__doc__)
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.fval, self.__doc__)
    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.fval, self.__doc__)
    def validator(self, fval):
        return type(self)(self.fget, self.fset, self.fdel, fval, self.__doc__)



#==============================================================================
#    Local Utility Sections
#==============================================================================
def _ensure_tuple(obj):
    """Ensure that object is a tuple, or is wrapped in one. 
    Also handles some special cases.
    Tuples are unchanged; NonStringSequences and Iterators are converted into
    a tuple containing the same elements; all others are wrapped by a tuple.
    """
    #Tuples - unchanged
    if isinstance(obj, tuple):
        return obj
    #Sequences - convert to tuple containing same elements.
    elif isinstance(obj, collections.Sequence) and not isinstance(obj, basestring):
        return tuple(obj)
    #Iterators & Generators - consume into a tuple
    elif isinstance(obj, collections.Iterator):
        return tuple(obj)
    #Other Iterables, Strings, and non-Iterables - wrap in iterable first
    else:
        return tuple([obj])

class NotPassed(object):    pass    #alternative to None

class TryGetError(LookupError): pass #

def _tryget(objects, attributes, default=NotPassed):
    objects = _ensure_tuple(objects)
    attributes = _ensure_tuple(attributes)
    for obj in objects:
        for attr in attributes:
            try:
                return obj.__getattribute__(obj, attr)
            except AttributeError:
                pass
    if default is NotPassed:
        raise AttributeError("Could not find attributes: "+str(attributes))
    else:
        return default