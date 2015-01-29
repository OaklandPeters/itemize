"""
This is basically all recursive "paths" related stuff.
It really need a paths set of getters & setters
(and those will be different than itemize's iter_get, get functions)

The recursive versions are best structued in a module like itemize's:
recursor/
    basics.py
        iter_get()
        get()


Core functions are basically just the magic methods on recursive version
of Record
    __iter__
    __getitem__
    __setitem__
    __delitem__
    __eq__
    __missing__
    __contains__
    __len__

@todo: Turn recursive into its own package, themed on itemize

"""
import collections

from . import interfaces
from . import shared

def iter_walk(record):
	"""Recursive iterator, yielding paths.
	@type: record: interfaces.Record
	@returns: collections.Sequence
	"""
	# This is fairly complicated.
	# I've implemented it before in rich_recursion.py
	# ... but I'm not writing it here at the moment
	yield NotImplemented

class Mything(object):
	def __init__(self, data):
		self.data = data
	def append(self, thing):
		self.data += thing

def mystuff(thing):
	"""
	@type: thing: Mything
	"""
	



def iter_pairs(record, paths=NotPassed):
	"""
	Returns (path, element) for record
	Example use:
	pairs(record, iter_walk)

	@type: record: interfaces.Record
	@returns: tuple
	"""
	if isinstance(paths, shared.NotPassedType):
		paths = iter_walk(record)
	elif isinstance(paths, collections.Iterable) and not isinstance(paths, basestring):
		pass #paths is fine. Usually a sequence of paths
	else:
		paths = [paths]

	for path in paths:
		yield path, get(record, path)


def iter_find(record, predicate=bool, paths=NotPassed):
	"""
	@type: record: interfaces.Record
	@returns: 
	"""
	for path, element in iter_pairs(record, paths=NotPassed):
		if predicate(record):
			yield path
	for path in iter_walk(record, paths=paths):
		if predicate(record)

