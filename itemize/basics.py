"""
Core functions for the 'itemize' package.

Guiding Principles:
(1) Unity: These should depend on the core argument meeting
    interfaces.Record (thus having __getitem__)
(2) Restraint: These should not depend on the Record being mutable. Any
    function needing mutablitity should be moved to recursive.py


Note on type-hints: most locations where 'Any' is used, should be a generic type,
    as described in PEP 483 and PEP 484. For example, instaed of:
        def _first(iterable): # type: Callable[[Iterable[Any], Any]]
    It would be:
        T = typing.typevar('T')
        def _first(iterable): # type: Callable[[Iterable[T]], T]
    However, since this is written before the `typing` module is released, this
    is not possible.
"""
from __future__ import absolute_import

import collections

from .shared import NotPassed, _ensure_tuple, RecordError
from .interfaces import Record, MutableRecord  # pylint: disable=unused-import

from .extern.unroll import compr, unroll


__all__ = [
    'missing',
    'has',
    'assert_missing',
    'iterget',
    'get',
    'get_all',
    'merge',
    'pairs',
    'indexes',
    'elements',
]


def missing(record, indexes):
    """Return list of indexes which are not present in record.

    Note: because this accepts Records, and not Mappings, it cannot
        simply check 'index in record'.
    Note #2: For Records with default values (such as defaultdict),
        this function will not report any values as missing.

    @type: record: Record[Any, Any]
    @type: indexes: Union[Sequence[Any], Any]
    @rtype: Sequence[Any]
    """
    @compr(list)
    def missing_indexes():
        """ mylist['string'] raises TypeError """
        for index in indexes:
            try:
                value = record[index]
            except (LookupError, TypeError):
                yield index
    return missing_indexes

def has(record, indexes):
    """Predicate.
    @type: record: Record[Any, Any]
    @type: indexes: Union[Sequence[Any], Any]
    @rtype: bool
    """
    return len(missing(record, indexes)) == 0

def assert_missing(record, indexes, name='object'):
    """
    @type: record: Record[Any, Any]
    @type: indexes: Union[Sequence[Any], Any]
    @rtype: Record[Any, Any]
    @raises: AssertionError
    """
    missing_indexes = missing(record, indexes)
    if len(missing_indexes) == 0:
        return record
    else:
        raise AssertionError(str.format(
            "'{0}' is missing required indexes: {1}",
            name, ", ".join(indexes)
        ))

def iterget(record, indexes, default=NotPassed):
    """
    @type: record: Record[Any, Any]
    @type: indexes: Union[Sequence, Any]
    @type: default: Union[NotPassed, Any]
    @rtype: Iterator[Any]
    """
    indexes = _ensure_tuple(indexes)
    yielded = False
    for index in indexes:
        try:
            yield record[index]
            yielded = True
        except (LookupError, TypeError):
            pass
    if not yielded:
        if default is NotPassed:
            raise RecordError(str.format(
                "Indexes not found: {0}",
                ", ".join(repr(index) for index in indexes)
            ))
        else:
            yield default

@unroll(_first)
def get(record, indexes, default=NotPassed):
    """
    @type: record: Record[Any, Any]
    @type: indexes: Union[Sequence, Any]
    @type: default: Union[NotPassed, Any]
    @rtype: Any
    """
    return iterget(record, indexes, default)

@unroll(list)
def get_all(record, indexes, default=NotPassed):
    """
    @type: record: Record[Any, Any]
    @type: indexes: Union[Sequence[Any], Any]
    @type: default: Union[Any, NotPassed]
    @rtype: List[Any]
    """
    #return list(iterget(record, indexes, default))
    return iterget(record, indexes, default)

def merge(*records):
    """
    Combines records into a dictionary, with later records potentially
    overriding earlier ones.
    @type: records: Tuple[Record[Any, Any]]
    @rtype: Dict[Any, Any]
    """
    return dict(
        (index, element)
        for record in reversed(records)
        for index, element in pairs(record)
    )

def pairs(record):
    """
    Generalization of Mapping.items().
    @type: record: Record[Any, Any]
    @rtype: List[Tuple[Any, Any]]
    @raises: TypeError
    """
    if isinstance(record, collections.Mapping):
        if hasattr(record, 'items'):
            return record.items()
        else:
            return collections.Mapping.items(record)
    elif isinstance(record, collections.Sequence) and not isinstance(record, basestring):
        return list(enumerate(record))
    else:
        raise TypeError("'record' should be a Mapping or Sequence.")

def indexes(record):
    """
    Generalization of Mapping.keys().
    @type: record: Record[Any, Any]
    @rtype: Iterable[]
    """
    if isinstance(record, collections.Mapping):
        if hasattr(record, 'keys'):
            return record.keys()
        else:
            return collections.Mapping.keys(record)
    elif isinstance(record, collections.Sequence) and not isinstance(record, basestring):
        return list(index for index, elm in enumerate(record))
    else:
        raise TypeError("'record' should be a Mapping or Sequence.")

def elements(record):
    """Generalization of .values().
    @type: record: Record[Any, Any]
    @rtype: Iterable[Any]
    """
    if isinstance(record, collections.Mapping):
        if hasattr(record, 'values'):
            return record.values()
        else:
            return collections.Mapping.values(record)
    elif isinstance(record, collections.Sequence) and not isinstance(record, basestring):
        return list(elm for index, elm in enumerate(record))
    else:
        raise TypeError("'record' should be a Mapping or Sequence.")

# Local utility functions
def _first(iterable):
    """
    @type: iterable: Iterable[Any]
    @rtype: Any
    """
    return iter(iterable).next()
