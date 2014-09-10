"""
Core functions for the 'itemize' package.

Guiding Principles:
(1) Strictness: These should depend only on the Record having __getitem__
"""
from __future__ import absolute_import
# Local imports from this package
from .interfaces import Record, MutableRecord
# Local imports from external support libraries
from .extern.unroll import compr
from .record_exceptions import *

__all__ = [
    'missing',
    'has',
    'assertion',
    'get',
    'chain',
    'merge'
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
    return (len(missing(record, indexes)) > 0)

def assertion(record, indexes, name=None):
    pass

def get(record, indexes):
    pass

def chain(*records):
    pass

class ChainRecord(object):
    pass

def merge(*records):
    """combine(*records: Record) -> dict
    ... maybe -> SimpleChainRecord
    """
    # This is just the function rich_core.defaults
