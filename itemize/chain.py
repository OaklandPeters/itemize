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
    """Adds ability to specify a collection-wide default (like defaultdict),
    
    """
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