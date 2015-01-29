TODO Lists
===================

Basics
-----------------
* Add type annotations, as per PEP 484


Needed Features
-----------------
* Setter: Recursive/chain iterset - parallel to iterget. probably contained in recursive.py (possibly in basics.py)
* Deleter: Recursive/chain iterdel - parallel to iterget.
* Provide easy adaptors to allow this to work for objects. Ex. 'get' applied to getting attributes (this is basically the same as the old _tryget) ~ get(vars(obj), names, default=None).
* Fill in examples in README.rst
* Add class description/doc for interfaces: Record, MutableRecord, Discrete, DiscreteRecord, DiscreteMutableRecord
* Add class description/doc for chain.py: SimpleChainRecord, DiscreteChainRecord, ChainRecord


Refactoring
-----------------
* Remove to seperate repoß: MethodDispatcher

Unittests
----------
* interfaces. Expanded, and refactored into test_interfaces
* Chain: refactor into test_chain.py
* For basics.assert_missing
* For basics.iterget
* For basics.merge
* For basics.pairs
* For basics.indexes
* For basics.elements

Packaging
-----------------
* Fill in README.rst - esp examples
* setup.py is ugly

Bugs
-----------

Advanced
----------
* recursive.py: function equivalents of __iter__, __setitem__, __getitem__, __delitem__, __eq__, and maybe __contains__, __len__, __missing__.
* Even more advanced: incorporate these methods (recursive versions of __iter__, __getitem__, etc) onto a class `Recursor`, which works like a recursive iterator/viewport around a record.
