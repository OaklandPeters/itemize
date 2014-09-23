"""
Shared data objects (primarily exceptions), used by several sub-modules.

Principles:
(1) These can not import any non-Python-standard modules.
(2) These must be *simple*
"""
import collections

from .extern.nulltype import NotPassed, NotPassedType

#==============================================================================
#    Exceptions
#==============================================================================
class RecordError(LookupError):
    """Base exception type for all exception in this package."""
    pass

class RecordDefaultError(RecordError):
    """Raised by ChainRecord.default(), if no default information was provided
    during initialization (via keywords)."""
    pass

class NoDispatch(Exception):
    """Represents failure in dispatching, and is used for flow-control, 
    somewhat similarly to the way the iterators use StopIteration.
    """
    pass


#==============================================================================
#    Utility Functions
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