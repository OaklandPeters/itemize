from __future__ import absolute_import
import collections
import functools
from .shared import NotPassed, NotPassedType
from .extern.clsproperty import VProperty


class MethodDispatcher(object):
    """Method-dispatcher.
    Where possible, dispatches to a method on the first argument.
    """
    def __init__(self, selector=NotPassed):
        self.selector = self.validate(selector)

    def __call__(self, func):
        name = func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            target, nargs, nkwargs = self.selector(*args, **kwargs)
            if hasattr(target, name):  # dispatch to method
                method = getattr(target, name)

                try:
                    return method(*nargs, **nkwargs)
                except TypeError:
                    print(TypeError)
                    import pdb
                    pdb.set_trace()
                    print(TypeError)
            else:  # original call
                return func(*args, **kwargs)
        return wrapper

    def validate(self, selector=NotPassed):
        """Validation actually handled via the property on selector."""
        return selector

    @VProperty
    class selector(object):
        def _get(self):
            return self._selector

        def _set(self, value):
            self._selector = value

        def _del(self):
            del self._selector

        def _val(self, value):
            if isinstance(value, collections.Callable):
                return value
            elif isinstance(value, NotPassedType):
                return _make_positional_arg_selector(0)
            elif isinstance(value, int):
                return _make_positional_arg_selector(value)
            elif isinstance(value, basestring):
                return _make_keyword_arg_selector(value)
            else:
                raise TypeError("Invalid 'selector': must be Callable, int, or basestring.")


def _make_positional_arg_selector(index):
    """Function factory.
    (*args, **kwargs) --> (target, new_args, kwargs)
    Make selector into (*args, **kwargs), for a positional index (an integer).

    Essentially, just splices out 'target' from 'args'.
    """
    assert(isinstance(index, int))

    def selector(*args, **kwargs):
        arg_list = list(args)
        target = arg_list.pop(index)
        positionals = tuple(arg_list)
        return (target, positionals, kwargs)
    return selector


def _make_keyword_arg_selector(index):
    """Function factory.
    (*args, **kwargs) --> (target, args, new_kwargs)
    """
    assert(isinstance(index, basestring))

    def selector(*args, **kwargs):
        target = kwargs.pop(index)
        return (target, args, kwargs)
    return selector
