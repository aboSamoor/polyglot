#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_polyglot
----------------------------------

Unit Tests for `polyglot` module.
"""

from polyglot.text import Text

def test_Text_words():
    text = Text("Hello and hi")
    print(text.words)

test_Text_words()