from __future__ import absolute_import
import collections
import sys

#from .basics import iterget, get, get_all
from . import basics
from .interfaces import Record, DiscreteRecord
from .shared import NotPassed, RecordError, RecordDefaultError, _ensure_tuple
from .extern.clsproperty import VProperty

__all__ = [
    'SimpleChainRecord',
    'DiscreteChainRecord',
    'ChainRecord'
]

# Experimental - trying for simplicity
class SimpleChainRecord(Record):
    """
    Very simple implementation of chainable Records.
    Does not allow index to be sequences.
    """
    def __init__(self, *records):
        """
        @type: records: Tuple[Record[Any, Any]]
        """
        self.records = self.validate(*records)
        
    def validate(self, *records):
        """
        @type: records: Tuple[Record[Any, Any]]
        @rtype: Tuple[Record[Any, Any]]
        """
        for i, rec in enumerate(records):
            assert(isinstance(rec, Record)), "record: "+str(i)
        return records

    def __repr__(self):
        """
        @rtype: str
        """
        return str.format(
            "{0}(records={1})",
            self.__class__.__name__, self._records
        )

    def __getitem__(self, index):
        """
        Look for a key in self.records. If not found, raise RecordError.
        @type: index: Any
        @rtype: Any
        @raises: RecordError
        """
        for record in self._records:
            try:
                return record[index]
            except LookupError:
                pass
        raise RecordError(index)

    def get(self, index, default=NotPassed):
        """
        As __getitem__, but allows specifying a default.
        @type: index; Any
        @type: default: Union[NotPassed, Any]
        """
        try:
            return self[index]
        except RecordError:
            if default is NotPassed:
                raise
            else:
                return default


class DiscreteChainRecord(SimpleChainRecord, DiscreteRecord):
    """
    Chain record of finite size. IE a ChainRecord, which also
    implements __len__ and __iter__.

    @todo: Consider using basics.indexes instead of local utiilty _indexes
    """
    def indexes(self):
        """List of all unique indexes from any record.
        A generalization of 'keys'.
        @todo: Should this be a property?

        @rtype: List[Any]
        """
        all_indexes = (index
            for record in self._records
            for index in _indexes(record)
        )
        return list(set(all_indexes)) #unique

    def __iter__(self):
        """
        @rtype: Iterator[Any]
        """
        return iter(self.indexes())

    def __contains__(self, index):
        """
        @type: index: Any
        @rtype: bool
        """
        return index in self.indexes()

    def __len__(self):
        """
        @rtype: int
        """
        return len(self.indexes())

    def __str__(self):
        """
        Important -- this can fail for _records with non-hashable indexes
        @rtype: str
        """
        try:
            str_form = dict(self)
        except (ValueError, TypeError):
            str_form = repr(self)
        return "{name}{asdict}".format(
            name=self.__class__.__name__, asdict=str_form
        )
            

class ChainRecord(DiscreteChainRecord, collections.Mapping):
    """Adds ability to specify a collection-wide default (like defaultdict),
    
    for .iterget(), .get(), .get_all():
        default passed in as argument takes priority over default
        passed into __init__

    """
    def __init__(self, *records, **kwargs):
        """
        @type: records: Tuple[Record[Any, Any]]
        @type: kwargs: Dict[str, Any]
        """
        self.records = records
        self.default = kwargs.get('default', NotPassed)

    @VProperty  # pylint: disable=invalid-name
    class records(object):  # type: Sequence[DiscreteRecord]
        """
        Mutable Property. Holds the records which will be chained.
        """
        def _get(self):
            """
            @rtype: Sequence[DiscreteRecord]
            """
            return self._records
        def _set(self, value):
            """
            Mutates, assigning value to self._records.
            This function assumes that VProperty._val(value) has already been run.
            @value: Sequence[DiscreteRecord]
            """
            self._records = value
        def _del(self):
            """
            Deletes records.
            """
            del self._records
        def _val(self, value):
            """
            Ensure that value is a nonstring Sequence of DiscreteRecord
            @value: Any
            @rtype: Sequence[DiscreteRecord]
            @raises: TypeError
            """
            if not isinstance(value, collections.Sequence) and not isinstance(value, basestring):
                raise TypeError("'records' must be a Sequence or basestring.")
            for i, rec in enumerate(value):
                if not isinstance(rec, DiscreteRecord):
                    raise TypeError("'records[{0}] must be a DiscreteRecord")
            return value
        
    def iterget(self, indexes, default=NotPassed):
        """
        default: can be provided by argument, or via property (fallback)
        @type: indexes: Union[Sequence[Any], Any]
        @type: default: Optional[Any]
        @rtype: Iterator[Any]
        @raises: RecordError
        """
        indexes = _ensure_tuple(indexes)
        yielded = False
        for record in self.records:
            for index in indexes:
                try:
                    yield record[index]
                    yielded = True
                except (LookupError, TypeError):
                    pass
        if not yielded:
            if default is NotPassed: #check argument
                if self.default is NotPassed: #check property
                    raise RecordError("Indexes not found: {0}".format(
                        ", ".join(repr(index) for index in indexes))
                        )
                else:
                    yield self.default
            else:
                yield default
        
    def get(self, indexes, default=NotPassed):
        """
        @type: indexes: Union[Sequence[Any], Any]
        @type: default: Optional[Any]
        @rtype: Any
        """
        return self.iterget(indexes, default=default).next()

    def get_all(self, indexes, default=NotPassed):
        """
        @type: indexes: Union[Sequence[Any], Any]
        @type: default: Optional[Any]
        @rtype: List[Any]
        """
        return list(self.iterget(indexes, default=default))

    def __getitem__(self, indexes):
        """
        @type: indexes: Union[Sequence[Any], Any]
        @rtype: Any
        """
        return self.get(indexes)


#==============================================================================
#    Local Utility Functions
#==============================================================================
def _indexes(record):
    """
    Generalization of .keys(). Works on sequences or mappings.
    @todo: Determine: is this different than basics.indexes() ?

    @type: record: Record[Any, Any]
    @rtype: Sequence[Any]
    @raises: TypeError
    """
    if hasattr(record, 'keys'):
        return record.keys()
    elif isinstance(record, collections.Iterable):
        return [ind for ind, elm in enumerate(record)]
    else:
        raise TypeError("'record' must have 'keys' or be Iterable.")
