from __future__ import absolute_import
import unittest
import os

# print('--')
# import pdb
# pdb.set_trace()
# print('--')
if __name__ == "__main__":
    from itemize.record_exceptions import RecordError, RecordDefaultError
    from itemize.chain import ChainRecord
    from itemize.basics import missing
    from itemize.interfaces import Record, MutableRecord, DiscreteRecord, DiscreteMutableRecord, _meets
else:
    from .record_exceptions import RecordError, RecordDefaultError
    from .chain import ChainRecord
    from .basics import missing
    from .interfaces import Record, MutableRecord, DiscreteRecord, DiscreteMutableRecord, _meets



class BasicsTests(unittest.TestCase):
    def test_missing(self):
        self.assertEquals(
            missing(['a','b','c'], [0, 1, 2]),
            []
        )
        self.assertEquals(
            missing(['a','b','c'], [0, 1, 2, 3, 4]),
            [3, 4]
        )   


class ChainTests(unittest.TestCase):
    """
    @todo: Add a test checking for raising RecordError for missing index
    """
    def setUp(self):
        pass
    def test_chainmap_behavior(self):
        """This is behavior shared with chainmaps."""
        d1 = {'a':1, 'b':2}
        d2 = {'a':3, 'd':4}
        cm = ChainRecord(d1, d2)

        self.assertEqual(
            (cm['a'],cm['b'],cm['d']),
            (1, 2, 4)
        )

        self.assertEqual(dict(cm), {'a':1, 'b':2, 'd':4})
        self.assertRaises(LookupError, lambda: cm['f'])
        self.assertEqual(cm.get('f', None), None)
        self.assertEqual(('f' in cm), False)
        self.assertEqual(cm.get('a', 10), 1)
        self.assertEqual(cm.get('f', 40), 40)
        
    def test_mixing_maps_and_sequences(self):
        map1 = {'a':'a1', 'b':'b2', 3:'33'}
        sequence2 = (1, 2, 3, 4)
        sequence3 = ['s1', 's2', 's3', 's4', 's5', 's6']
        
        cm12 = ChainRecord(map1, sequence2)
        cm21 = ChainRecord(sequence2, map1)
        cm23 = ChainRecord(sequence2, sequence3)
        cm123 = ChainRecord(map1, sequence2, sequence3)
        
        self.assertEqual(
            cm12,
            {'a':'a1', 'b':'b2', 3:'33', 0:1, 1:2, 2:3}
        )
        self.assertNotEqual(
            cm12,
            {'a':'a1', 'b':'b2', 0:1, 1:2, 2:3, 3:4}
        )
        self.assertEqual(
            ChainRecord(sequence2, map1),
            {'a':'a1', 'b':'b2', 0:1, 1:2, 2:3, 3:4}
        )
        
        self.assertEqual(
            cm23,
            {0: 1, 1: 2, 2: 3, 3: 4, 4: 's5', 5: 's6'}
        )
        self.assertEqual(
            cm123,
            {'a': 'a1', 0: 1, 2: 3, 3: '33', 4: 's5', 5: 's6', 1: 2, 'b': 'b2'}
        )
        
        
    def test_class(self):
        class SQLClass(object):
            defaults = {
                'driver':               'com.mysql.jdbc.Driver',
                'dburl':                'jdbc:mysql://localhost/drug_db',
                'proptable':            'testproptb',
                'login':                'user',
                'password':             'tsibetcwwi'
            }
            def __init__(self,table=None,**options):
                self.table = table
    
                self._parameters = ChainRecord(options,
                    self.defaults,
                    default=None
                )
                self.driver = self._parameters['driver']
                self.dburl = self._parameters['dburl']
                self.proptable = self._parameters['proptable']
                self.login = self._parameters['login']
                self.password = self._parameters['password']
                self.socket = self._parameters['socket']

        cxn = SQLClass(driver='stuff')
        self.assertEqual(cxn.driver, 'stuff')
        self.assertEqual(cxn.proptable, 'testproptb')
        self.assertEqual(cxn.socket, None)


class InterfacesTests(unittest.TestCase):
    def test_user_class(self):
        class OtherClass(object):
            __len__ = lambda : NotImplemented
            __contains__  = lambda : NotImplemented
            __iter__ = lambda : NotImplemented
            __getitem__ = lambda : NotImplemented
        self.assert_(_meets(OtherClass, Record))
        self.assert_(_meets(OtherClass(), Record))
        self.assert_(not _meets(OtherClass, MutableRecord))
        self.assert_(not _meets(OtherClass(), MutableRecord))
        
        self.assert_(_meets(OtherClass, DiscreteRecord))
        self.assert_(_meets(OtherClass(), DiscreteRecord))
        
        self.assert_(not _meets(OtherClass, DiscreteMutableRecord))
        self.assert_(not _meets(OtherClass(), DiscreteMutableRecord))
        
    def test_DiscreteMutableRecord(self):
        self.assert_(_meets(dict, DiscreteMutableRecord))
        self.assert_(_meets(dict(), DiscreteMutableRecord))
        self.assert_(not _meets(set, DiscreteMutableRecord))
        self.assert_(not _meets(set(), DiscreteMutableRecord))


if __name__ == "__main__":
    unittest.main()