from __future__ import absolute_import
import abc
import collections



class Record(object):
    """
    Root ABC for all record-types. Record types generalizes Sequence and Mapping,
    representing item-containing objects.

    @todo Add Mixins
    """
    __metaclass__ = abc.ABCMeta
    __getitem__ = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Record:
            if _meets(subclass, cls) and not isinstance(subclass, basestring):
                return True
        return NotImplemented

class MutableRecord(Record):
    """
    @todo Add Mixins
    """
    __metaclass__ = abc.ABCMeta
    __setitem__ = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    __delitem__ = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is MutableRecord:
            if _meets(subclass, cls) and not isinstance(subclass, basestring):
                return True
        return NotImplemented

class Discrete(collections.Sized, collections.Iterable):
    """
    ABC for collections of finite size, which are iterable. Intended to be used
    with

    IE has abstract methods: __len__, __iter__
    """
    __metaclass__ = abc.ABCMeta
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Discrete:
            if _meets(subclass, cls) and not isinstance(subclass, basestring):
                return True
        return NotImplemented

class DiscreteRecord(Record, Discrete):
    """
    Quandry: Should DiscreteRecord inherit from Container?
        Context: Sequence, Set, and Mapping inherit from Sized, Iterable, and Container.
    """
    __metaclass__ = abc.ABCMeta
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is DiscreteRecord:
            if _meets(subclass, cls) and not isinstance(subclass, basestring):
                return True
        return NotImplemented

class DiscreteMutableRecord(MutableRecord, Discrete):
    __metaclass__ = abc.ABCMeta
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is DiscreteMutableRecord:
            if _meets(subclass, cls) and not isinstance(subclass, basestring):
                return True
        return NotImplemented

#------------------------------------------------------------------------------
#        Local Utility
#------------------------------------------------------------------------------
def _hasattr(subklass, attr):
    """Determine if subklass, or any ancestor class, has an attribute.
    Copied shamelessly from the abc portion of collections.py.
    """
    try:
        return any(attr in B.__dict__ for B in subklass.__mro__)
    except AttributeError:
        # Old-style class
        return hasattr(subklass, attr)

def _meets(obj, abstract):
    """Determines if an object meets an abstract interface (from abc module)."""
    return all(
        _hasattr(obj, attr) for attr in abstract.__abstractmethods__
    )
