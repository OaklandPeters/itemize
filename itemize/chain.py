from __future__ import absolute_import
import collections
import sys
# if __name__ == "__main__":
#     from interfaces import Record
#     from record_exceptions import RecordError, RecordDefaultError
# else:
#     from .interfaces import Record
#     from .record_exceptions import RecordError, RecordDefaultError

from .interfaces import Record, DiscreteRecord
from .record_exceptions import RecordError, RecordDefaultError

from .extern.clsproperty import VProperty



class NotPassed(object):
    """Represents non-passed arguments. Alternative to using None."""
    pass


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
            

class ChainRecord(DiscreteChainRecord, collections.Mapping):
    def __init__(self, *records, **kwargs):
        self.records = records
        self.default = kwargs.get('default', NotPassed)
    def _getitem(self, index):
        for record in self._records:
            try:
                return record[index]
            except (LookupError, TypeError):
                pass
        raise RecordError(index)
    def __getitem__(self, index):
        """Look for a key in self.records. If not found, raise RecordError."""
        try:
            return self._getitem(index)
        except RecordError:
            if self.default is NotPassed:
                raise
            else:
                return self.default
    def get(self, index, default=NotPassed):
        try:
            return self._getitem(index)
        except RecordError:
            if default is NotPassed:
                if self.default is NotPassed:
                    raise
                else:
                    return self.default
            else:
                return default
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



# 
# class StrictChainRecord(Record, collections.Mapping):
#     """Combine a number of Records for chained lookup.
#     
#     chain = StrictChainRecord(record1, record2)
#     chain['a']
#     
#     possible future:
#     keywords['default']
#     keywords['default_execute']
#     """
# 
#     def __init__(self, *records, **keywords):
#         """
#         
#         """
#         (self._records, self._default, self._default_execute
#             ) = self.validate(*records, **keywords)
#         
#     def validate(self, *records, **keywords):
#         for i, rec in enumerate(records):
#             if not isinstance(rec, Record):
#                 raise TypeError(
#                     "records[{0}] is not a an instance of Record.".format(i)
#                 )
#         default = keywords.get('default', NotPassed)
#         default_execute = keywords.get('default_execute', NotPassed)
#         if (default is not NotPassed) and (default_execute is not NotPassed):
#             raise ValueError("Only one keyword should be provided: "
#                 "'default' or 'default_execute'"
#             )
#         return records, default, default_execute
# 
#     def __repr__(self):
#         return "{0}(records={1})".format(self.__class__.__name__, self._records)
# 
#     def _get(self, index):
#         """Look for a key in self._records. If not found, raise RecordError."""
#         for record in self._records:
#             try:
#                 return record[index]
#             except (LookupError, TypeError): #list['string'] raises TypeError
#                 pass
#         raise RecordError(index)
#     
#     def _get_default(self, index, default):
#         try:
#             return self._get(index)
#         except RecordError:
#             return default
#             
#     def __getitem__(self, index):
#         """As __get(), except accounts for possibility of a default value."""
#         try:
#             return self._get(index)
#         except RecordError:
#             if self.default(index) is NotPassed:
#                 raise RecordError(index)
#             else:
#                 return self.default(index)
# 
#     def get(self, index, default=NotPassed):
#         """As self[index] (__getitem__), except allows for specifying
#         default value by parameter.
#         
#         Edge case: default passed in AND default specified via keyword into init
#         """
#         try:
#             return self._get(index)
#         except RecordError:
#             exc_info = sys.exc_info()
#             if default is NotPassed:
#                 try:
#                     return self.default(index)
#                 except RecordDefaultError:
#                     raise exc_info[0], exc_info[1], exc_info[2] #re-raise original
#             else:
#                 return default                
#                 
#     
#     def default(self, index):
#         """
#         If no default was provided (during init), then this should
#         raise a RecordDefaultError
#         """
#         if self._default is not NotPassed:
#             return self._default
#         elif self._default_execute is not NotPassed:
#             return self._default_execute(index)
#         else:
#             raise RecordDefaultError("No default found for index: "+str(index))
# 
# 
#     def append(self, record):
#         """Add a new mapping to the end of the mappings to be chained."""
#         assert(isinstance(record, Record)), ("New records must be instance of Record.")
#         
#         self._records = self._records + (record, )
#         
#     #--------------------------------------------------------------------------
#     #
#     #--------------------------------------------------------------------------
#     # Behavior not-strictly implied by Record (usually depends on iterability)
#     
# 
# 
# 
# class ChainRecord(StrictChainRecord, collections.Sized, collections.Iterable, collections.Container):
#     """Combine multiple records (~Mappings or Sequences) for sequential lookup.
#     StrictChainRecord depends on it's records ONLY having __getitem__
#     ChainRecord generalizes to assuming that it's records are Mapping or Sequence
#     (~Iterable and sized)
#     
#     Most 
#     """
# 
#     def indexes(self):
#         """List of all unique indexes from any record.
#         A generalization of 'keys'."""
#         all_indexes = (index
#             for record in self._records
#             for index in _indexes(record)
#         )
#         return list(set(all_indexes)) #unique
#     def keys(self):
#         """Allows ChainRecord to be mapping/dict -like."""
#         return self.indexes()
#     def __iter__(self):
#         return iter(self.indexes())
#     def __contains__(self, index):
#         return index in self.indexes()
#     def __len__(self):
#         return len(self.indexes())
#     def __str__(self):
#         # Importantly -- this can fail for _records with non-hashable indexes
#         try:
#             str_form = dict(self)
#         except (ValueError, TypeError):
#             str_form = repr(self)
#         return "{name}{asdict}".format(
#             name=self.__class__.__name__, asdict=str_form
#         )
            

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