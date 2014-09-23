from __future__ import absolute_import
import unittest


from itemize import basics
from itemize.shared import NotPassed, RecordError, RecordDefaultError

from itemize.dispatcher import MethodDispatcher


class DispatcherTests(unittest.TestCase):

    
    def test_basic(self):
        @MethodDispatcher()
        def get(record, index, default=NotPassed):
            return basics.get(record, index, default)
        self.batch(get)

    def test_selector_argument(self):
        @MethodDispatcher(selector=lambda *args, **kwargs: (args[0], args[1:], kwargs))
        def get(record, index, default=NotPassed):
            return basics.get(record, index, default)
        self.batch(get)
    
    def test_selector_argument_factory(self):
        @MethodDispatcher(0)
        def get(record, index, default=NotPassed):
            return basics.get(record, index, default)
        self.batch(get)


    def batch(self, get):
        record1 = {'a':'a1','b':'b1'}
        
        class WeirdRecord(object):
            def __init__(self, value):
                self.value = value
            def get(self, index, default=NotPassed):
                return (self.value, index)
        weird = WeirdRecord('foo')        
        
        # Test on dict
        self.assertEqual(get(record1, 'b'), 'b1')
        self.assertEqual(basics.get(record1, 'b'), 'b1')
        self.assertEqual(get(record1, 0, 'baz'), 'baz')
        
        # Test on custom Record
        self.assertEqual(get(weird, 'b'), ('foo', 'b'))
        self.assertEqual(basics.get(weird, 'b'), ('foo', 'b'))        
        self.assertEqual(get(weird, 0, 'baz'), ('foo', 0))
        
        
if __name__ == "__main__":
    unittest.main()