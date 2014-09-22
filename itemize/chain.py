from __future__ import absolute_import
import collections
import sys

from .basics import iterget, get, get_all
from .interfaces import Record, DiscreteRecord
from .shared import NotPassed, RecordError, RecordDefaultError
from .extern.clsproperty import VProperty






# Experimental - trying for simplicity
class SimpleChainRecord(Record):
    def __init__(self, *records):
        self.records = self.validate(*records)
        
    def validate(self, *records):
        for i, rec in enumerate(records):
            assert(isinstance(rec, Record)), "record: "+str(i)
    def __repr__(self):
        return "{0}(records={1})".format(self.__class__.__name__, self._records)
    def __getitem__(self, index):
        """Look for a key in self.records. If not found, raise RecordError."""
        for record in self._records:
            try:
                return record[index]
            except LookupError:
                pass
        raise RecordError(index)
    def get(self, index, default=NotPassed):
        """As __getitem__, but allows specifying a default."""
        try:
            return self[index]
        except RecordError:
            if default is NotPassed:
                raise
            else:
                return default

class DiscreteChainRecord(SimpleChainRecord, DiscreteRecord):
    def indexes(self):
        """List of all unique indexes from any record.
        A generalization of 'keys'."""
        all_indexes = (index
            for record in self._records
            for index in _indexes(record)
        )
        return list(set(all_indexes)) #unique
    def __iter__(self):
        return iter(self.indexes())
    def __contains__(self, index):
        return index in self.indexes()
    def __len__(self):
        return len(self.indexes())
    def __str__(self):
        # Importantly -- this can fail for _records with non-hashable indexes
        try:
            str_form = dict(self)
        except (ValueError, TypeError):
            str_form = repr(self)
        return "{name}{asdict}".format(
            name=self.__class__.__name__, asdict=str_form
        )
            

#------- Original ChainRecord:
# class ChainRecord(DiscreteChainRecord, collections.Mapping):
#     """Adds ability to specify a collection-wide default (like defaultdict),
#     
#     """
#     def __init__(self, *records, **kwargs):
#         self.records = records
#         self.default = kwargs.get('default', NotPassed)
#     def _getitem(self, index):
#         for record in self._records:
#             try:
#                 return record[index]
#             except (LookupError, TypeError):
#                 pass
#         raise RecordError(index)
#     def __getitem__(self, index):
#         """Look for a key in self.records. If not found, raise RecordError."""
#         try:
#             return self._getitem(index)
#         except RecordError:
#             if self.default is NotPassed:
#                 raise
#             else:
#                 return self.default
#     def get(self, index, default=NotPassed):
#         """Get index, but allows specifying a default via argument.
#         Default argument takes precedence over default attribute
#         (self.default) - usually specified during initialization.
#         """
#         try:
#             return self._getitem(index)
#         except RecordError:
#             if default is not NotPassed:
#                 return default
#             else:
#                 if self.default is not NotPassed:
#                     return self.default
#                 else:
#                     raise
# #     def _itergetitem(self, index):
# #         yielded = False
# #         for record in self._records:
#             
#     @VProperty
#     class records(object):
#         def _get(self):
#             return self._records
#         def _set(self, value):
#             self._records = value
#         def _del(self):
#             del self._records
#         def _val(self, value):
#             if not isinstance(value, collections.Sequence) and not isinstance(value, basestring):
#                 raise TypeError("'records' must be a Sequence or basestring.")
#             for i, rec in enumerate(value):
#                 if not isinstance(rec, DiscreteRecord):
#                     raise TypeError("'records[{0}] must be a DiscreteRecord")
#             return value

class ChainRecord(DiscreteChainRecord, collections.Mapping):
    """Adds ability to specify a collection-wide default (like defaultdict),
    
    for .iterget(), .get(), .get_all():
        default passed in as argument takes priority over default
        passed into __init__
    """
    def __init__(self, *records, **kwargs):
        self.records = records
        self.default = kwargs.get('default', NotPassed)
    @VProperty
    class records(object):
        def _get(self):
            return self._records
        def _set(self, value):
            self._records = value
        def _del(self):
            del self._records
        def _val(self, value):
            if not isinstance(value, collections.Sequence) and not isinstance(value, basestring):
                raise TypeError("'records' must be a Sequence or basestring.")
            for i, rec in enumerate(value):
                if not isinstance(rec, DiscreteRecord):
                    raise TypeError("'records[{0}] must be a DiscreteRecord")
            return value
        
    def iterget(self, indexes, default=NotPassed):
        yielded = False
        for record in self._records:
            for value in iterget(record, indexes):
                yield value
                yielded = True
        if not yielded:
            if default is NotPassed:
                if self.default is NotPassed:
                    raise RecordError("Indexes not found: {0}".format(
                        ", ".join(repr(index) for index in indexes))
                        )
                else:
                    yield self.default
            else:
                yield default
    def get(self, indexes, default=NotPassed):
        return self.iterget(indexes, default=default).next()
    def get_all(self, indexes, default=NotPassed):
        return list(self.iterget(indexes, default=default))
    def __getitem__(self, indexes):
        return self.get(indexes)








#==============================================================================
#    Local Utility Functions
#==============================================================================
def _indexes(record):
    """Generalization of .keys(). Works on sequences or mappings."""
    if hasattr(record, 'keys'):
        return record.keys()
    elif isinstance(record, collections.Iterable):
        return [ind for ind, elm in enumerate(record)]
    else:
        raise TypeError("'record' must have 'keys' or be Iterable.")



    

if __name__ == "__main__":
    unittest.main()