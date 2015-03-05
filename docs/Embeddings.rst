
.. code:: python

    from io import StringIO
    import sys
.. code:: python

    %load_ext autoreload
    %autoreload 2
.. code:: python

    polyglot_dir = u'/data/polyglot'
    
    if polyglot_dir not in sys.path:
      sys.path.insert(0, polyglot_dir)
.. code:: python

    from polyglot.mapping import OrderedVocabulary
    from polyglot.load import locate_resource, load_embeddings
.. code:: python

    v.words



.. parsed-literal::

    [u'the', u'book', u'Book', u'3234', u'upper', u'lower', u'cool', u'McCain']



.. code:: python

    from polyglot.mapping.expansion import DigitExpander, CaseExpander

.. code:: python

    v2 = CaseExpander(v)
    print
    v3 = DigitExpander(v)
    print
    v4 = DigitExpander(v2)

.. parsed-literal::

    
    


.. code:: python

    import unittest
    
    vocab = u"""
    the
    book
    Book
    3
    upper
    lower
    5
    cool
    McCain
    """.strip()
    
    class DigitExpanderTest(unittest.TestCase):
      def setUp(self):
        self.v = OrderedVocabulary.from_vocabfile(StringIO(vocab))
        
      def test_load(self):
        self.assertEqual(len(self.v), 9)
        
      def test_digit_expansion(self):
        v = DigitExpander(vocabulary=self.v, strategy='most_frequent')
        self.assertEqual(len(v), 10)
        
      def test_digit_membership(self):
        v = DigitExpander(vocabulary=self.v, strategy='most_frequent')
        self.assertTrue(u"8" in v)
        self.assertTrue(u"3" in v)
        self.assertFalse(u"71" in v)
        
      def test_digit_ids(self):
        v = DigitExpander(vocabulary=self.v, strategy='most_frequent')
        self.assertEqual(v["6"], 3)
        self.assertEqual(v["7"], v["2"])
        self.assertNotEqual(v["3"], v["5"])
        
    class CaseExpanderTest(unittest.TestCase):
      def setUp(self):
        self.v = OrderedVocabulary.from_vocabfile(StringIO(vocab))
        
      def test_load(self):
        self.assertEqual(len(self.v), 9)
        
      def test_case_expansion(self):
        v = CaseExpander(vocabulary=self.v, strategy='most_frequent')
        self.assertEqual(len(v), 21)
        
      def test_digit_membership(self):
        v = CaseExpander(vocabulary=self.v, strategy='most_frequent')
        self.assertTrue(u"3" in v)
        self.assertTrue(u"BOOK" in v)
        self.assertTrue(u"mccain" in v)
        
      def test_digit_ids(self):
        v = CaseExpander(vocabulary=self.v, strategy='most_frequent')
        self.assertEqual(v["THE"], 0)
        self.assertEqual(v["UPPER"], v["upper"])
        
    class MixedExpansionTest(unittest.TestCase):
      def setUp(self):
        self.v = OrderedVocabulary.from_vocabfile(StringIO(vocab))
        self.v1 = CaseExpander(vocabulary=self.v, strategy='most_frequent')
        self.v2 = DigitExpander(vocabulary=self.v1, strategy='most_frequent')
        
      def test_expansion(self):
        self.assertEqual(len(self.v2), 22)
        
      def test_membership(self):
        self.assertTrue(u"3" in self.v2)
        self.assertTrue(u"9" in self.v2)
        self.assertTrue(u"#" in self.v2)
        self.assertTrue(u"BOOK" in self.v2)
        self.assertTrue(u"mccain" in self.v2)
        
      def test_ids(self):
        self.assertEqual(self.v2["THE"], 0)
        self.assertEqual(self.v2["UPPER"], self.v2["upper"])    
        self.assertEqual(self.v2["3"], self.v2["7"])
        

.. code:: python

    suite = unittest.TestLoader().loadTestsFromTestCase(CaseExpanderTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(DigitExpanderTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(MixedExpansionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

.. parsed-literal::

    test_case_expansion (__main__.CaseExpanderTest) ... ok
    test_digit_ids (__main__.CaseExpanderTest) ... ok
    test_digit_membership (__main__.CaseExpanderTest) ... ok
    test_load (__main__.CaseExpanderTest) ... ok
    
    ----------------------------------------------------------------------
    Ran 4 tests in 0.004s
    
    OK
    test_digit_expansion (__main__.DigitExpanderTest) ... ok
    test_digit_ids (__main__.DigitExpanderTest) ... ok
    test_digit_membership (__main__.DigitExpanderTest) ... ok
    test_load (__main__.DigitExpanderTest) ... ok
    
    ----------------------------------------------------------------------
    Ran 4 tests in 0.004s
    
    OK
    test_expansion (__main__.MixedExpansionTest) ... ok
    test_ids (__main__.MixedExpansionTest) ... ok
    test_membership (__main__.MixedExpansionTest) ... ok
    
    ----------------------------------------------------------------------
    Ran 3 tests in 0.004s
    
    OK




.. parsed-literal::

    <unittest.runner.TextTestResult run=3 errors=0 failures=0>


