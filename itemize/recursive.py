"""
This is basically all recursive "paths" related stuff.
It really need a paths set of getters & setters
(and those will be different than itemize's iter_get, get functions)

The recursive versions are best structued in a module like itemize's:
recursor/
    basics.py
        iter_get()
        get()


Core functions are basically just the magic methods on recursive version
of Record
    __iter__
    __getitem__
    __setitem__
    __delitem__
    __eq__
    __missing__
    __contains__
    __len__

@todo: Turn recursive into its own package, themed on itemize

"""
import collections

from . import basics
from . import interfaces
from . import shared



def rec_compare(record_a, record_b):
    """
    One-way recursive comparison of two Records.
    @type: record_a: Record
    @type: record_b: Record
    @rtype: bool
    """
    for path in rec_paths(record_a):  # terminal paths in record_a
        elm_a = basics.get(record_a, path)
        try:
            elm_b = basics.get(record_b, path)
        except LookupError:
            return False

        if elm_a != elm_b:
            return False
    return True


def rec_eq(record_a, record_b):
    """
    Binary recursive comparison of two Records.
    @type: record_a: Record
    @type: record_b: Record
    @rtype: bool
    """
    if rec_compare(record_a, record_b):
        if rec_compare(record_b, record_a):
            return True
    # Fallthrough
    return False







def rec_iter(record):
    """
    @type: record: Record[Any, Any]
    @rtype: Iterator[Tuple[Sequence[Any], Any]]
    """
    path = tuple()
    history = set()

    return _rec_iter(record, path, history)

def _rec_iter(obj, path, history):
    """
    @type: obj: Record[Any, Any]
    @type: path: Tuple[Any]
    @type: history: Set[Any]
    @rtype: Iterator[Tuple[Sequence[Any], Any]]

    @todo: Fix problem: rec_iter is returning incorrect obj, but correct paths
    """
    if isinstance(obj, interfaces.DiscreteRecord):
        iterator = basics.pairs(obj)
        identity = id(obj)

        if identity not in history:
            history.add(identity)
            for index, elm in iterator:
                for result in _rec_iter(elm, path+(index, ), history):
                    yield result
            history.remove(identity)
        # else... terminate branch and return nothing
    else:
        yield path, obj

def rec_paths(record):
    """
    Retreive terminal paths only (not elements).
    Terminal paths lead to non-DiscreteRecords
    """
    for path, _ in rec_iter(record):
        yield path


def iter_pairs(record, paths=shared.NotPassed):
    """
    Returns (path, element) for record
    Example use:
    pairs(record, iter_walk)

    @type: record: interfaces.Record[Any, Any]
    @rtype: Iterator[Tuple[Any, Any]]
    """
    if isinstance(paths, shared.NotPassedType):
        paths = list(rec_paths(record))
    elif isinstance(paths, collections.Iterable) and not isinstance(paths, basestring):
        if isinstance(paths, collections.Iterator):
            paths = list(paths)
        else:
            pass #paths is fine. Usually a sequence of paths
    else:
        paths = [paths]

    for path in paths:
        yield path, basics.get(record, path)


def iter_find(record, predicate=bool, paths=shared.NotPassed):
    """
    @type: record: interfaces.Record
    @rtype: Iterator
    """
    for path, _ in iter_pairs(record, paths=shared.NotPassed):
        if predicate(record):
            yield path

    for path, _ in iter_pairs(record, paths=paths):
        if predicate(record):
            #......
            #
            #UNFINISHED
            #
            pass
