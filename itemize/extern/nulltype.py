import abc
import types
import collections



__all__ = ['NullType', 'NotPassed', 'NotPassedType']

class NullType(object):
    """Superclass of NoneType, NotPassed, and optional."""
    __metaclass__ = abc.ABCMeta
NullType.register(types.NoneType)

class NotPassedType(NullType):
    """Represents non-passed arguments. Alternative to using None, useful
    in cases where you want to distinguish passing in the value of 'None' from
    'No-value-was-provided'."""
    def __init__(self):
        pass
NotPassed = NotPassedType()
