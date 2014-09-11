from __future__ import absolute_import
import unittest
import os


if __name__ == "__main__":
    from itemize.record_exceptions import RecordError, RecordDefaultError
    from itemize.chain import ChainRecord
    from itemize.basics import missing, has, get, get_all
    from itemize.interfaces import Record, MutableRecord, DiscreteRecord, DiscreteMutableRecord, _meets
    from itemize.shared import NotPassed
else:
    from .record_exceptions import RecordError, RecordDefaultError
    from .chain import ChainRecord
    from .basics import missing, has, get, get_all
    from .interfaces import Record, MutableRecord, DiscreteRecord, DiscreteMutableRecord, _meets
    from .shared import NotPassed


class BasicsTests(unittest.TestCase):
    def test_missing(self):
        # Sequences
        self.assertEquals(
            missing(['a','b','c'], [0, 1, 2]),
            []
        )
        self.assertEquals(
            missing(['a','b','c'], [0, 1, 2, 3, 4]),
            [3, 4]
        )
        # Mappings
        self.assertEquals(
            missing({'a':1,'b':2,'c':3}, ('a','b','c')),
            []
        )
        self.assertEquals(
            missing({'a':1,'b':2,'c':3,'d':4}, ('a','b','c')),
            []
        )
        self.assertEquals(
            missing({'a':1,'b':2,'c':3,'d':4,5:'55'}, ('a','b','c',5)),
            []
        )
        self.assertEquals(
            missing({'a':1,'b':2,'c':3,'d':4,5:'55'}, (12.0,'a','b','c',5,'ee')),
            [12.0, 'ee']
        )
        
        # Things that might raise TypeError from non-hashable keys
        self.assertEquals(
            missing({'a':1,'b':2,'c':3,'d':4,5:'55'}, (set(['a']), 'a','b','c',5)),
            [set(['a'])]
        )
    def test_has(self):
        # Sequences
        self.assertEquals(
            has(['a','b','c'], [0, 1, 2]),
            True
        )
        self.assertEquals(
            has(['a','b','c'], [0, 1, 2, 3, 4]),
            False
        )
        # Mappings
        self.assertEquals(
            has({'a':1,'b':2,'c':3}, ('a','b','c')),
            True
        )
        self.assertEquals(
            has({'a':1,'b':2,'c':3}, ('a','b','c','d')),
            False
        )
        self.assertEquals(
            has({'a':1,'b':2,'c':3,'d':4}, ('a','b','c')),
            True
        )
        self.assertEquals(
            has({'a':1,'b':2,'c':3,'d':4}, ('a','b','c',5)),
            False
        )
        self.assertEquals(
            has({'a':1,'b':2,'c':3,'d':4,5:'55'}, ('a','b','c',5)),
            True
        )
    
    
    def test_get(self):
        # Mappings
        defaults = {
            'driver':               'com.mysql.jdbc.Driver',
            'dburl':                'jdbc:mysql://localhost/drug_db',
            'proptable':            'testproptb',
            'login':                'user',
            'password':             'tsibetcwwi'
        }
        self.assertEquals(
            get(defaults, ('driver', 'dburl', 'nonexistant'), default=123),
            'com.mysql.jdbc.Driver'
        )
        self.assertEquals(
            get(defaults, ('nonexistant', 'dburl'), default=123),
            'jdbc:mysql://localhost/drug_db'
        )
        self.assertEquals(
            get(defaults, (u'kkaa', 123.43, 'nonexistant', 0), default=123),
            123
        )
        self.assertRaises(RecordError,
            lambda: get(defaults, (u'kkaa', 123.43, 'nonexistant', 0), default=NotPassed)
        )
        
        # Sequences
        sequence1 = ('s0', 's1', 's2')
        self.assertEqual(get(sequence1, 2), 's2')
        
        self.assertRaises(RecordError, lambda: get(sequence1, 3))
        self.assertRaises(RecordError, lambda: get(sequence1, ('0', 3)))
        self.assertEqual(get(sequence1, ['0', 3, 0]), 's0')
        self.assertEqual(get(sequence1, ('0', 3), 'AA'), 'AA')
        self.assertEqual(get(sequence1, ('0', 3), default='AA'), 'AA')
        self.assertEqual(get(sequence1, ('0', 3), default=None), None)

    def test_get_all(self):
        # Mappings
        defaults = {
            'driver':               'com.mysql.jdbc.Driver',
            'dburl':                'jdbc:mysql://localhost/drug_db',
            'proptable':            'testproptb',
            'login':                'user',
            'password':             'tsibetcwwi'
        }
        self.assertEquals(
            get_all(defaults, ('driver', 'dburl', 'nonexistant')),
            ['com.mysql.jdbc.Driver', 'jdbc:mysql://localhost/drug_db']
        )
        self.assertEquals(
            get_all(defaults, ('driver', 'dburl', 'nonexistant'), default=123),
            ['com.mysql.jdbc.Driver', 'jdbc:mysql://localhost/drug_db']
        )
        self.assertRaises(RecordError,
            lambda: get_all(defaults, (u'kkaa', 123.43, 'nonexistant', 0)),
        )
        self.assertEquals(
            get_all(defaults, (u'kkaa', 123.43, 'nonexistant', 0), default=123),
            [123]
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



# class CleverGetTests(unittest.TestCase):
#     def test_itemget(self):
#         pass
        

if __name__ == "__main__":
    unittest.main()