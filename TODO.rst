TODO Lists
===================


Needed Features
-----------------
 * Provide easy adaptors to allow this to work for objects. Ex. 'get' applied to getting attributes (this is basically the same as the old _tryget) ~ get(vars(obj), names, default=None).
 * Fill in examples in README.rst
 * Add class description/doc for interfaces: Record, MutableRecord, Discrete, DiscreteRecord, DiscreteMutableRecord
 * Add class description/doc for chain.py: SimpleChainRecord, DiscreteChainRecord, ChainRecord
 

Refactoring
-----------------
 * Migrate dispatcher (MethodDispatcher) to it's own little repo
 * Re-write most of the README.rst template. It is currently based on `README.md <https://gist.github.com/jxson/1784669/>`_ by `Jason Campbell <https://gist.github.com/jxson/>`_ on Github.

Bugs
-----------------
 * Do NOT copy the .git folder from the packge_template - that folder maintains 'package_template' as it's own repo
 * setup.py is ugly