"""
Core functions for the 'itemize' package.

Guiding Principles:
(1) Strictness: These should depend only on the Record having __getitem__


@todo: unittests for these functions.
    Unittests written:
        missing
        has

@todo: Consider making some/many of these into dispatch functions.
    ... of the Pythonic type, where they defer to methods on first argument,
        if one exists, and have default behavior otherwise.
    @todo: Example: get(mydict, 'value', default=) makes use of mydict.get() 
        ... requires special vectorizing handling if multiple keys passed in
            

"""
from __future__ import absolute_import
import collections
# Local imports from this package
from .interfaces import Record, MutableRecord
# Local imports from external support libraries
from .extern.unroll import compr, unroll
from .record_exceptions import RecordError
from .shared import NotPassed, _ensure_tuple
from .chain import ChainRecord

__all__ = [
    'missing',
    'has',
    'assertion',
    'get',
    'get_all',
    'chain',
    'merge',
    'pairs',
    'indexes',
    'elements',
    
    
    'iterget',
    
]
# Future: ChainObject




def missing(record, indexes):
    """Return list of indexes which are not present in record.

    Note: because this accepts Records, and not Mappings, it cannot
        simply check 'index in record'.
    Note #2: For Records with default values (such as defaultdict),
        this function will not report any values as missing.
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
    """Predicate. """
    return len(missing(record, indexes)) == 0

def assertion(record, indexes, name='object'):
    missing_indexes = missing(record, indexes)
    if len(missing_indexes) == 0:
        return record
    else:
        raise AssertionError(str.format(
            "'{0}' is missing required indexes: {1}",
            name, ", ".join(indexes)
        ))

# def get(record, indexes, default=NotPassed):
#     indexes = _ensure_tuple(indexes)
#     for index in indexes:
#         try:
#             return record[index]
#         except (LookupError, TypeError):
#             pass
#     if default is NotPassed:
#         raise RecordError("Indexes not found: '{0}'".format(
#             ", ".join(repr(index) for index in indexes))
#         )
#     else:
#         return default

def iterget(record, indexes, default=NotPassed):
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
            raise RecordError("Indexes not found: {0}".format(
                ", ".join(repr(index) for index in indexes))
            )
        else:
            yield default
        
@unroll(lambda iterable: iter(iterable).next()) # get first
def get(record, indexes, default=NotPassed):
    return iterget(record, indexes, default)

@unroll(list)
def get_all(record, indexes, default=NotPassed):
    return iterget(record, indexes, default)
#     @compr(list)
#     def results():
#         for index in indexes:
#             try:
#                 yield record[index]
#             except (LookupError, TypeError):
#                 pass
#         if default is NotPassed:
#             raise RecordError("Could not find any of indexes: '{0}'".format(
#                 ", ".join(indexes))
#             )
#         else:
#             yield default
#     return results


def merge(*records):
    return dict(
        (index, element)
        for record in reversed(records)
        for index, element in pairs(record)
    )

def chain(*records, **kwargs):
    return ChainRecord(*records, **kwargs)

def pairs(record):
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
    """Generalization of .keys(). Works on sequences or mappings."""
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
    """Generalization of .values(). Works on sequences or mappings."""
    if isinstance(record, collections.Mapping):
        if hasattr(record, 'values'):
            return record.values()
        else:
            return collections.Mapping.values(record)
    elif isinstance(record, collections.Sequence) and not isinstance(record, basestring):
        return list(elm for index, elm in enumerate(record))
    else:
        raise TypeError("'record' should be a Mapping or Sequence.")