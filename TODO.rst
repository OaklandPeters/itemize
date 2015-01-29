TODO Lists
===================

Needed Features
-----------------
* recursive.py core functions: setter, deleter, iter - parallel to basics.iterget
* Provide easy adaptors to allow this to work for objects. Ex. 'get' applied to getting attributes (this is basically the same as the old _tryget) ~ get(vars(obj), names, default=None).

Refactoring
-----------------

Unittests
----------
* interfaces. Expanded, and refactored into test_interfaces
* Chain: refactor into test_chain.py
* For basics.assert_missing
* For basics.iterget
* For basics.merge: complex. Should test nesting, overriding, etc. Sequences/Mappings, etc
* For basics.pairs
* For basics.indices
* For basics.elements

Packaging
-----------------
* Fill in README.rst - esp examples
* setup.py is ugly
* Add class description/doc for interfaces: Record, MutableRecord, Discrete, DiscreteRecord, DiscreteMutableRecord
* Add class description/doc for chain.py: SimpleChainRecord, DiscreteChainRecord, ChainRecord

Bugs
-----------
* rec_iter returns incorrect values (although correct paths) for some nested Records. Example: {'a':(1, 2), 'b':3} VS {'b':3, 'a':(1, 2)}
* Standardize handling of 'indexes', across functions. For example, `missing()` does not cast indexes to tuple, but `get()` does.
    * Standardize handling of 'indexes' in chain.ChainRecord
* Functions in basics.py should raise custom Exception types, not builtins.
* chain.ChainRecord: exceptions raised should be custom exception types.
* chain.ChainRecord.iterget: should raise: class RecordIndexError(RecordError, KeyError, IndexError)

Advanced
----------
* recursive.py: function equivalents of __iter__, __setitem__, __getitem__, __delitem__, __eq__, and maybe __contains__, __len__, __missing__.
* Even more advanced: incorporate these methods (recursive versions of __iter__, __getitem__, etc) onto a class `Recursor`, which works like a recursive iterator/viewport around a record.
