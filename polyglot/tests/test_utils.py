#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test utility functions"""

import unittest
from ..utils import _decode

from six import text_type as unicode

class UtilsTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_decode(self):
    expected = unicode("foo")
    self.assertEqual(_decode( "foo"), expected)
    self.assertEqual(_decode(u"foo"), expected)
    self.assertEqual(_decode(b"foo"), expected)

if __name__ == "__main__":
  unittest.main()
