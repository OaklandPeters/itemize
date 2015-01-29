

from __future__ import absolute_import

import unittest

from itemize.recursive import rec_eq

dicta = {'a':1, 'b':2}
dictb = {'a':1, 'b':2}
dictc = {'a':1, 'b':'2'}
lista = [1, 2]
listb = ['a','b']
listc = [('a',1), ('b',2)]
listd = [2, 1]
liste = (1, 2)

nesta = {'a':(1, 2), 'b':3}
nestb = {'b':3, 'a':(1, 2)}
nestc = {0:(1, 2), 1:3}
nestd = [(1, 2), 3]


class RecursionTests(unittest.TestCase):
    def test_rec_eq(self):
        self.assertTrue(rec_eq(dicta, dictb))
        self.assertFalse(rec_eq(dicta, dictc))
        self.assertFalse(rec_eq(dicta, lista))
        self.assertFalse(rec_eq(dicta, listb))
        self.assertFalse(rec_eq(dicta, listc))
        self.assertFalse(rec_eq(dicta, listd))
        self.assertFalse(rec_eq(dicta, liste))

        self.assertFalse(rec_eq(dictb, dictc))
        self.assertFalse(rec_eq(dictb, lista))
        self.assertFalse(rec_eq(dictb, listb))
        self.assertFalse(rec_eq(dictb, listc))
        self.assertFalse(rec_eq(dictb, listd))
        self.assertFalse(rec_eq(dictb, liste))

        self.assertFalse(rec_eq(dictc, lista))
        self.assertFalse(rec_eq(dictc, listb))
        self.assertFalse(rec_eq(dictc, listc))
        self.assertFalse(rec_eq(dictc, listd))
        self.assertFalse(rec_eq(dictc, liste))

        self.assertFalse(rec_eq(lista, listb))
        self.assertFalse(rec_eq(lista, listc))
        self.assertFalse(rec_eq(lista, listd))
        self.assertTrue(rec_eq(lista, liste))

        self.assertFalse(rec_eq(listb, listc))
        self.assertFalse(rec_eq(listb, listd))
        self.assertFalse(rec_eq(listb, liste))

        self.assertFalse(rec_eq(listc, listd))
        self.assertFalse(rec_eq(listc, liste))

        self.assertFalse(rec_eq(listd, liste))

    def test_rec_eq_nested(self):
        self.assertTrue(rec_eq(nesta, nestb))
        self.assertFalse(rec_eq(nesta, nestc))
        self.assertFalse(rec_eq(nesta, nestd))
        
        self.assertFalse(rec_eq(nestb, nestc))
        self.assertFalse(rec_eq(nestb, nestd))

        self.assertTrue(rec_eq(nestc, nestd))


if __name__ == "__main__":
    unittest.main()
